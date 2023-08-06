#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import json
from datetime import datetime, timedelta
import pytz
import re
from collections import defaultdict
import math
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import zipfile

from .. import VISTA_DATA_BASE_DIR
BASE_LOCN_TEMPL = VISTA_DATA_BASE_DIR + "{}/"
DATAV1_LOCN_TEMPL = BASE_LOCN_TEMPL + "DataV1/"
DATA_LOCN_TEMPL = BASE_LOCN_TEMPL + "Data/"
DATARF_LOCN_TEMPL = BASE_LOCN_TEMPL + "DataRF/"
SCHEMA_LOCN_TEMPL = BASE_LOCN_TEMPL + "Schema/"
LOG_LOCN_TEMPL = BASE_LOCN_TEMPL + "Logs/"
TMPWORKING_LOCN_TEMPL = BASE_LOCN_TEMPL + "TmpWorking/"
DATAMETA_LOCN_TEMPL = BASE_LOCN_TEMPL + "DataMeta/"

PATIENT_NAME_TYPES = ["2", "9000001", "55", "63", "70", "631", "665", "690", "790", "38_1"]

"""
Really FMQL[Data]ReplyStore for DESCRIBE replies using afterien, the basic reply of the Cacher. Navigates choice of raw JSON or zip based storage

Implementation note - IEN ordering: 
- don't use split(".") when extracting afterien from file names as some IENs (3_081) are floats. Hence use of re.sub on file suffix.
- open question: any NON FLOAT/NON INTEGER IENs? Enforces none in 'flush'.

TODO: 
- Ability to reset replies for new LIMIT ie/ relimit replies of type
- FMQLSchemaStore to parallel FMQLReplyStore (may become FMQLDataStore)
- MOVE this and other utilities to just take 'stationNumber' ala other cacher utils - ie/ force the /.../Data[V1] structure
"""
class FMQLReplyStore:

    # useZip only applies to EMPTY or newly created
    def __init__(self, cacheLocation, useZip=False, makeDir=True):
    
        """
        Test for both type of cache (ZIP or RAW) and if good or not (BAD_)
        """
        def cacheType(cacheLocation):
            if sum(1 for f in os.listdir(cacheLocation)) == 0:
                return "EMPTY"
            zfs = set(zf for zf in os.listdir(cacheLocation) if re.search(r'\.zip', zf))
            if len(zfs):
                if sum(1 for zf in zfs if not re.match(r'[\d\_]+(\-S)?\-[\d\.]+\.zip$', zf)):
                    return "BAD_ZIP"
                return "ZIP"
            jfs = set(jf for jf in os.listdir(cacheLocation) if re.search(r'\.json', jf))
            if len(jfs):
                if sum(1 for bjf in jfs if not re.match(r'[\d\_]+(\-S)?\-[\d\.]+\.json$', bjf)):
                    return "BAD_RAW"
                return "RAW"
            return "BAD_NOTEMPTY"
    
        if not os.path.isdir(cacheLocation): 
            if not makeDir:
                logging.error("No cacheLocation {}".format(cacheLocation))
                raise Exception("No cacheLocation {}".format(cacheLocation))
            os.mkdir(cacheLocation)
            logging.info("Created location {} for Replies".format(cacheLocation))
            self.__isZip = useZip
        else:
            cType = cacheType(cacheLocation)
            if re.match(r'BAD', cType):
                raise Exception("Bad cache {} - {}".format(cacheLocation, cType))
            if cType == "EMPTY":
                self.__isZip = useZip
            else:
                self.__isZip = True if cType == "ZIP" else False 
        self.__cacheLocation = cacheLocation if re.search(r'\/$', cacheLocation) else cacheLocation + "/"
        
    def usesZip(self):
        return self.__isZip

    def availableTypes(self):
        return set(f.split("-")[0] for f in self.replyFiles())

    def stoppedTypes(self):
        return set(f.split("-")[0] for f in self.replyFiles() if re.search(r'\-S\-', f))
        
    """
    From SELECT TYPES - expected to be in {cacheLocation}/Schema
    
    Use [a] report on FM # vs real and [b] clump types based on size for 
    cacher strategy [c] see progress/ what's left (combine with
    _availableTypes_
    
    Note: any counts < 0 turned into -1
    """
    def expectedTypeCounts(self):
        schemaLocation = re.sub(r'[^\/]+\/$', '/', self.__cacheLocation)
        selectTypes = json.load(open("{}/Schema/SELECT_TYPES.json".format(schemaLocation)))
        expectedCountByType = {}
        for result in selectTypes["results"]:
            if "parent" in result:
                continue
            typ = re.sub(r'\.', '_', result["number"])
            if "count" not in result:
                expectedCountByType[typ] = {"label": result["name"], "count": 0}
                continue
            cnt = int(result["count"]) if not re.search(r'\-', result["count"]) else -1
            expectedCountByType[typ] = {"label": result["name"], "count": cnt}
        return expectedCountByType
        
    def replyFiles(self):
        suffix = "zip" if self.__isZip else "json"
        return [f for f in os.listdir(self.__cacheLocation) if os.path.isfile(os.path.join(self.__cacheLocation, f)) and re.search('\.' + suffix + '$', f)]
        
    """
    Only works if reply files follow IENs names (see below)
        format(reply["fmql"]["TYPE"], reply["fmql"]["AFTERIEN"], "zip") 
        
    Note: coming is related 'replyFileOfCreateDate'
    """
    def replyFileOfResource(self, resourceId):
        replyType = resourceId.split("-")[0]
        sreplyFiles = sorted([f for f in self.replyFiles() if re.match(replyType + "\-", f)], key=lambda x: float(re.sub(r'\.(json|zip)$', '', x.split("-")[-1])))
        if len(sreplyFiles) == 1:
            return sreplyFiles[0] # note: not checking inside so possible NOT!
        resourceIENF = float(resourceId.split("-")[1])
        if resourceIENF == 0:
            return sreplyFiles[0]
        for i, replyFile in sreplyFiles:
            afterIEN = float(re.sub(r'\.(json|zip)$', '', replyFile.split("-")[-1]))
            if resourceIENF <= afterIEN:
                return sreplyFiles[i-1]
        return "" # can't find
        
    """
    Assumption - date order is reply file/resource order. Hence 'create day'

    Use: process only resources made after a certain date.
    
    Note: 'day' is granularity, not time.
    
    Use in recipe for caching more from fresh image of semi-state types
    like 3.081 (just need close) or 2005. Get firstReplyFileOnOrAfterCreateDay
    and take the one before it as source of afterien
    """
    def firstReplyFileOnOrAfterCreateDay(self, replyType, dtProp, dayValue):
        if not isinstance(dayValue, datetime):
            dayValue = datetime.strptime(dayValue, "%Y-%m-%d")
        sreplyFiles = self.replyFilesOfType(replyType)
        if len(sreplyFiles) == 0:
            return ""
        lastReplyFileLoaded = ""
        def getDay(resource, dateProp):
            if dateProp not in resource:
                return ""
            # Allow for real date and a pointer who's label is a date!
            if isinstance(resource[dateProp], dict):
                if "value" in resource[dateProp]:
                    return resource[dateProp]["value"].split("T")[0]
                elif "label" in resource[dateProp]:
                    return resource[dateProp]["label"].split("T")[0]
            return ""
        while True:
            if len(sreplyFiles) == 0: # no reply at or above that date
                firstReplyFile = ""
                break
            midIndex = int(len(sreplyFiles)/2)
            if sreplyFiles[midIndex] == lastReplyFileLoaded:
                if midIndex == 0:
                    raise Exception("Stuck on 0 - should never happen")
                midIndex = midIndex - 1 # move down one (see below)
            lastReplyFileLoaded = sreplyFiles[midIndex]
            midReply = self.loadReplyFromFile(sreplyFiles[midIndex])
            lastDayValue = None
            for resource in reversed(midReply["results"]):
                lastDayValueStr = getDay(resource, dtProp)
                if lastDayValueStr == "":
                    continue
                try:
                    lastDayValue = datetime.strptime(lastDayValueStr, "%Y-%m-%d")
                except:
                    logging.info("Skipping resource of reply {} as bad date value {}".format(sreplyFiles[midIndex], lastDayValueStr))
                    continue
                break
            # For now insist all replies have at least one resource with prop
            if lastDayValue == None:
                # sreplyFiles.pop(midIndex)
                # continue
                firstReplyFile = ""
                break
            if lastDayValue < dayValue: # delete all before and inc this one
                sreplyFiles = sreplyFiles[midIndex+1:]
                continue
            # >= and first one! => this is it or as good as we get
            if midIndex == 0:
                firstReplyFile = sreplyFiles[midIndex]
                break
            # delete all ABOVE this one. If none above, the midIndex
            # check above that avoids repetition will catch it
            sreplyFiles = sreplyFiles[0:midIndex+1]
        return firstReplyFile           
                
    """
    Record both actual and compressed size if zip cache (zip supports it)
    """
    def replySizeByType(self):        
        sizeByFileTypeByFile = defaultdict(lambda: defaultdict(int))    
        for fl in self.replyFiles():
            flTyp = fl.split("-")[0]
            if self.usesZip():
                jfl = re.sub(r'zip$', 'json', fl)
                zfName = "{}/{}".format(self.__cacheLocation, fl)
                zf = zipfile.ZipFile(zfName, "r")   
                jflZInfo = zf.getinfo(jfl) 
                sizeByFileTypeByFile[flTyp][fl] = {"actual": jflZInfo.file_size, "compressed": jflZInfo.compress_size}
            else:
                sizeByFileTypeByFile[flTyp][fl] = {"actual": os.path.getsize(self.__cacheLocation + fl)}
        return sizeByFileTypeByFile

    """
    For cacher - allows it to hone in on LIMIT and AFTERIEN of last reply so can 
    issue next one
    """
    def lastReplyOfType(self, replyType): 
        filesSoFar = [f for f in self.replyFiles() if re.match(replyType + "\-", f)]   
        if len(filesSoFar):
            fl = sorted(filesSoFar, key=lambda x: float(re.sub(r'\.(json|zip)$', '', x.split("-")[-1])))[-1]
            if re.search(r'\.zip$', fl):
                jfl = re.sub(r'zip$', 'json', fl)
                zfName = "{}/{}".format(self.__cacheLocation, fl)
                zf = zipfile.ZipFile(zfName, "r")   
                lastReply = json.loads(zf.read(jfl))
                return lastReply
            else:
                return json.load(open(self.__cacheLocation + fl))
        return None 

    def replyFilesOfType(self, replyType):
        filesSoFar = sorted([f for f in self.replyFiles() if re.match(replyType + "\-", f)], key=lambda x: float(re.sub(r'\.(json|zip)$', '', x.split("-")[-1])))
        return filesSoFar
        
    def loadReplyFromFile(self, fl):
        if re.search(r'\.zip$', fl):
            zf = zipfile.ZipFile(self.__cacheLocation + fl, "r")
            jfl = re.sub(r'zip$', 'json', fl)
            flJSON = json.loads(zf.read(jfl))
        else:
            flJSON = json.load(open(self.__cacheLocation + "/" + fl))
        return flJSON
        
    def totalReplies(self):
        return len(self.replyFiles())
     
    """           
    Generally TYP-AFTERIEN. but if stopped (v1.3 on) then TYP-S-AFTERIEN.
    """
    def flush(self, reply):     
        # Expect FLOAT or INTEGER IEN so that sorting will work
        if not re.match(r'[\d\.]+$', str(reply["fmql"]["AFTERIEN"])):
            raise Exception("Ordering and processing of Replies in Cache rely on integer or float IENs - not {}".format(reply["fmql"]["AFTERIEN"]))
        if len(reply["results"]) == 0:
            raise Exception("Not allowed flush an empty reply - certain cache routines expect at least one result in each cached reply")
        stoppedDesignation = "-S" if ("stopped" in reply or "fmqlMaxStopped" in reply) else ""
        if self.__isZip:
            fl = "{}{}-{}.{}".format(reply["fmql"]["TYPE"], stoppedDesignation, reply["fmql"]["AFTERIEN"], "zip")    
            zfName = "{}/{}".format(self.__cacheLocation, fl)
            zf = zipfile.ZipFile(zfName, "w", zipfile.ZIP_DEFLATED, allowZip64=True) 
            jfl = re.sub(r'zip$', 'json', fl)
            zf.writestr(jfl, json.dumps(reply))       
        else:
            fl = "{}{}-{}.{}".format(reply["fmql"]["TYPE"], stoppedDesignation, reply["fmql"]["AFTERIEN"], "json")
            json.dump(reply, open(self.__cacheLocation + fl, "w"), indent=4)
        return fl # return the file name
        
    """
    Used to avoid recaching - note: .json or .zip independent. ie/ one or other there
    then that suffices.
    """
    def replyFileExists(self, replyFile): 
        suffix = "zip" if self.__isZip else "json"  
        fl = re.sub(r'(json|zip)$', suffix, replyFile)
        if fl in set(self.replyFiles()):
            return fl
        return ""
        
    """
    Records if another process is using/writing to a Reply file
    
    TODO: for parallel operations in multi-threaded operations
    """
    def replyFileInUse(self, replyFile):
        pass
        
    def iterator(self, onlyTypes=None, excludeRepliesFilter=None, startAtReply=""):
    
        class FMQLReplyIterator:
        
            def __init__(self, cacheLocation, onlyTypes, excludeRepliesFilter, startAtReply, isZip):
                
                self.__cacheLocation = cacheLocation
                self.__excludeRepliesFilter = excludeRepliesFilter 
                self.__startAtReply = startAtReply
                
                self.__currentReplyFile = ""
                
                suffix = "zip" if isZip else "json"     
                self.__flsByTyp = defaultdict(list)
                for fl in os.listdir(cacheLocation):
                    if not re.search(suffix + '$', fl):
                        continue
                    flTyp = fl.split("-")[0]
                    # distinguish [] and None
                    if onlyTypes != None and flTyp not in onlyTypes:
                        continue
                    self.__flsByTyp[flTyp].append(fl)
                    
                if len(self.__flsByTyp) == 0:
                    if len(onlyTypes):
                        raise Exception("Can't build iterator when no Replies of Type(s) {} exist".format(", ".join(list(onlyTypes))))
                    raise Exception("Can't build iterator when no Replies exist")
                    
            def currentReplyFile(self):
                return self.__currentReplyFile
                        
            """
            TODO: full iterator
            - startAtReply could be passed to iter optionally 
            - next takes over what iter does but must raise StopIteration() 
            """                
            def __iter__(self):
        
                for typ in sorted(self.__flsByTyp, key=lambda x: float(re.sub("_", ".", x))):

                    for fl in sorted(self.__flsByTyp[typ], key=lambda x: float(re.sub(r'\.(json|zip)$', '', x.split("-")[-1]))):
                                        
                        # Usually only used with one type being iterated
                        if self.__startAtReply != "":
                            if self.__startAtReply == fl:
                                self.__startAtReply = ""
                            else:
                                continue 

                        if self.__excludeRepliesFilter and self.__excludeRepliesFilter(fl):
                            continue # put here so in order
                            
                        self.__currentReplyFile = fl
                        
                        if re.search(r'\.zip$', fl):
                            try:
                                zf = zipfile.ZipFile(self.__cacheLocation + fl, "r")
                            except:
                                raise Exception("Can't handle bad reply ZIP file {}".format(fl))
                            jfl = re.sub(r'zip$', 'json', fl)
                            flJSON = json.loads(zf.read(jfl))
                        else:
                            flJSON = json.load(open(self.__cacheLocation + "/" + fl))            
                    
                        yield flJSON
              
        if startAtReply != "" and not (onlyTypes and len(onlyTypes) == 1):
            raise Exception("Cannot have iterate with 'startAtReply' if don't specify one and only one type")      
        return FMQLReplyIterator(self.__cacheLocation, onlyTypes, excludeRepliesFilter, startAtReply, self.__isZip)
        
"""
Simple resource iterator built over the FMQLReplyStore's iterator

Note on memory use:

    import psutil
    process = psutil.Process(os.getpid())
    print("Memory Use End", process.memory_info().rss, process.memory_percent())
    
can see 2.7% -> 3.5% just doing a no op iteration of a large file. GC has its own mind.
Using ORDERED is both slower and more memory intensive (6.5%).
"""
class FilteredResultIterator:
    
    def __init__(self, replyLocation, typId, filt=None, startAtReply=""):
    
        fmqlReplyStore = FMQLReplyStore(replyLocation)        
        self.__replyIter = fmqlReplyStore.iterator(onlyTypes=[typId], startAtReply=startAtReply)
        self.__filt = filt
            
        self._numberFiltered = 0
            
    @property
    def numberFiltered(self):
        return self._numberFiltered
            
    def __iter__(self):
        for reply in self.__replyIter:
            for resource in reply["results"]:
                if self.__filt and not self.__filt(resource):
                    self._numberFiltered += 1
                    continue
                yield resource
                
    def currentReplyFile(self):
        return self.__replyIter.currentReplyFile()

"""
File by file, cache data and will restart. Checks what's already in store.

TODO: may move into an FMQLCacher that provides caching utilities (as opposed
to the reading of FMQL[Data|Reply]Store.
    
Mandatory arguments:
- fmqlIF
- fmqlReplyStore
- fileType: ex/ 2, 120_5

Optional/defaulted arguments:
- limit for query: defaults to 1000
- cstop for query: defaults to 10
- filter for query: default is none
- maxNumber: maximum number to retrieve. Default is no limit (-1)
- afterIEN (for restart if necessary and for doing LIMIT at a time)
- epWord: query used in CSP and node; Apache uses "fmql"

To make FMQLIF:
    
    from ..fmqlIF.fmqlIF import FMQLRESTIF, FMQLBrokerIF
    
        fmqlIF = FMQLRESTIF(fmqlEP, epWord="fmqlQuery")
                            or
        fmqlIF = FMQLBrokerIF(hostname, port, access, verify, osehraVISTA=False)

Returns:
    COMPLETE
    HITMAX
    NO_SUCH_FILE
    EMPTY_FILE
"""                
def cacheFileToStore(fmqlIF, fmqlReplyStore, fileType, limit=500, cstop=1000, maxNumber=-1):

    queryTempl = "DESCRIBE " + fileType + " LIMIT %(limit)s AFTERIEN %(afterien)s CSTOP " + str(cstop)
    
    # Three cases for AFTERIEN:
    # - no reply => afterien is 0
    # - last reply is the last (# results < limit of its query)
    # - last reply's last result supplies afterien
    # ... note that Cache depends on float or integer IENs and enforces that form
    lastReply = fmqlReplyStore.lastReplyOfType(fileType)
    if not lastReply:
        afterien = 0
        numberOfTypeCachedOverall = 0
    else:
        # REM: limit for next go may not be the same so not overriding limit
        lastLimit = int(lastReply["fmql"]["LIMIT"])
        if lastLimit > len(lastReply["results"]):
            logging.info("Got all of {} already - moving on".format(fileType))
            return "COMPLETE"
        if maxNumber != -1:
            repliesSoFar = fmqlReplyStore.replyFilesOfType(fileType)
            cachedSoFar = len(repliesSoFar) * lastLimit
            if cachedSoFar >= maxNumber:
                logging.info("Cached so far of {} already exceeds max number of {} - moving on".format(cachedSoFar, maxNumber))
                return "HITMAX"
        lastResult = lastReply["results"][-1]
        afterien = (lastResult["_id"] if "_id" in lastResult else lastResult["uri"]["value"]).split("-")[1]
        numberOfTypeCachedOverall = lastLimit * len(fmqlReplyStore.replyFilesOfType(fileType))
        logging.info("Filetype {}, Cached {:,} already, some left to get. Restarting with AFTERIEN {}".format(fileType, numberOfTypeCachedOverall, afterien))

    # queryNo and afterIEN are usually 0 but can start again    
    # Loop until there is no more or we reach the maximum
    numberOfTypeCached = 0
    start = datetime.now()
    stopped = False
    queryNo = 0
    while True:

        queryNo += 1
        query = queryTempl % {"limit": limit, "afterien": afterien}
        noCachedMU = "{:,}".format(numberOfTypeCached) if numberOfTypeCachedOverall == numberOfTypeCached else "{:,}/{:,}".format(numberOfTypeCached, numberOfTypeCachedOverall)
        logging.info("Sending query number {} after {} cached, taking {} so far - {}".format(queryNo, noCachedMU, datetime.now() - start, query))

        queryStart = datetime.now()
        jreply = fmqlIF.invokeQuery(query)
        if "error" in jreply:
            # Shouldn't happen for Cacher as it walks Schema but for some VistAs (FOIA)
            # definitions may be there though files are not?
            if jreply["error"] == "No such file": # will treat like a "Zero file"
                if queryNo != 1:
                    raise Exception("Expect 'no such file' error with first query")
                logging.info("Bailing on {} query as no such file".format(fileType))
                return "NO_SUCH_FILE"
            logging.error("Received error reply: {}".format(jreply["error"]))
            raise Exception(jreply["error"])

        # Special case - first call (afterien=0) and no results => don't cache
        # ... REM: doing TOPONLY in case POPONLY is wrong. Means more queries but safer.
        # Ex for CHCS Synth: ['3_081', '66', '52'] not in POP but have "data"
        # ... REM: afterien != 0 and no results then still cache as it means the case of
        # second to last LIMITED query filled up and then the last just returns none.
        # Note: alt is do a COUNT and then DESCRIBE if need be but largely the same cost.
        if afterien == 0 and len(jreply["results"]) == 0:
            logging.info("Empty {} - 0 replies afterien 0".format(fileType))
            return "EMPTY_FILE" 

        # Don't return False (<=> empty file) - but no results left ... happens in rare 
        # case of LIMIT coinciding with end of previous reply
        if len(jreply["results"]) == 0:
            break

        queryTook = str(datetime.now() - queryStart)
        jreply["queryTook"] = queryTook # time taken (queryCached time is set in store)
        # note time as UTC (can change to local times in a display)
        jreply["queryCached"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if "fmqlMaxStopped" in jreply or "stopped" in jreply:
            stopped = True
        try:
            fmqlReplyStore.flush(jreply)
        except:
            logging.error("Failed to serialize {}/{} - backing out".format(fileType, afterien))
            raise
        logging.info("Queried and flushed {} afterien {} in {} with {} resources, any stopped {}".format(fileType, str(afterien), queryTook, len(jreply["results"]), "**TRUE**" if stopped else "FALSE"))
        
        numberOfTypeCached += len(jreply["results"])
        numberOfTypeCachedOverall += len(jreply["results"])
        if len(jreply["results"]) != int(limit):
            break

        # TODO: properly reset limit at the start to make sure maximum never exceeded
        if maxNumber != -1 and numberOfTypeCached >= maxNumber:
            logging.debug("Breaking as got or exceeded maximum requested - {} - for {}".format(maxNumber, fileType))
            break
        lastResult = jreply["results"][-1]
        afterien = (lastResult["_id"] if "_id" in lastResult else lastResult["uri"]["value"]).split("-")[1]
        if (queryNo % 100) == 0:
            logging.debug("So far this has taken {}".format(datetime.now() - start))

    noCachedMU = "{:,}".format(numberOfTypeCached) if numberOfTypeCachedOverall == numberOfTypeCached else "{:,}/{:,}".format(numberOfTypeCached, numberOfTypeCachedOverall)
    logging.info("Finished - cached {}, stopped {}, took {}".format(noCachedMU, "TRUE" if stopped else "FALSE", datetime.now() - start))
    
    return "COMPLETE"
   
"""
Inside [cacheLocation], will zip all replies of type [fileType] AND remove the unzipped replies. Allows retroactive zipping
... could be simpler - type then reply file just to do the work in order
""" 
def zipAllReplies(cacheLocation):

    def zipRepliesOfType(fileType, cacheLocation):
        start = datetime.now()
        if cacheLocation[-1] != "/":
            cacheLocation += "/"
        filesOfType = [f for f in os.listdir(cacheLocation) if os.path.isfile(os.path.join(cacheLocation, f)) and re.search('\.json$', f) and re.match(fileType + "\-", f)]
        if len(filesOfType) == 0:
            logging.info("No files of type {} to archive - exiting".format(fileType))
            return
        for i, f in enumerate(filesOfType, 1):
            qf = os.path.join(cacheLocation, f)
            with zipfile.ZipFile(cacheLocation + re.sub(r'json$', 'zip', f), "w", zipfile.ZIP_DEFLATED, allowZip64=True) as typeZip:
                typeZip.write(qf, f)
                os.remove(qf)
        logging.info("Wrote {} files of type {} to archives in {}".format(i, fileType, str(datetime.now() - start)))
        
    start = datetime.now()
    
    flTyps = set()
    for fl in os.listdir(cacheLocation):
        if not re.search(r'\.json$', fl):
            continue
        flTyp = fl.split("-")[0]
        flTyps.add(flTyp)
    for i, flTyp in enumerate(flTyps, 1):
        zipRepliesOfType(flTyp, cacheLocation)
        
    logging.info("Wrote {} types to archives in {}".format(i, str(datetime.now() - start)))
    
"""
Or
   for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return num
"""
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
   
"""
Deprecated: older V2 from V1 FMQL. V3 FMQL now largely embeds the form created here. Here for old dataset transformation
leveraging fmqlV2er
"""
class V1RecordToV2:

    # actualTimeZone from "for tz in pytz.all_timezones" ex/ US/Mountain
    def __init__(self, forMongo=False, actualTimeZone=""):

        ID = "V1RecordToV2"
        DESCRIPTION = "From DM V1 to DM V2 - DM in 1 was client-side"
        
        self.__idProp = "id" if not forMongo else "_id"
        self.__transformedByTypeCount = defaultdict(int)
        
    def transform(self, record):
        nrecord = self.__reframe(record)
        self.__transformedByTypeCount[nrecord[self.__idProp].split("-")[0]] += 1
        return nrecord
        
    def __newType(self, record):
    
        typV2 = record["uri"]["label"].split("/")[0] + "-" + record["uri"]["value"].split("-")[0]

        TYP_MAP = {
            "STATION NUMBER TIME SENSITIVE-389_9": "STATION NUMBER (TIME SENSITIVE)-389_9",
            "ICD OPERATION_PROCEDURE-80_1": "ICD OPERATION/PROCEDURE-80_1",
            "USR AUTHORIZATION_SUBSCRIPTION-8930_1": "USR AUTHORIZATION/SUBSCRIPTION-8930_1",
            "OE_RR REPORT-101_24": "OE/RR REPORT-101_24",
            "OE_RR EPCS PARAMETERS-100_7": "OE/RR EPCS PARAMETERS-100_7",
            "NDC_UPN-50_67": "NDC/UPN-50_67",
            "SERVICE_SECTION-49": "SERVICE/SECTION-49",
            "SIGN_SYMPTOMS-120_83": "SIGN/SYMPTOMS-120_83"
        }
        if typV2 in TYP_MAP:
            typV2 = TYP_MAP[typV2]
            
        return typV2 
        
    def __newProp(self, prop, propValue):
        RESERVED_PROPS = ["id", "_id", "type", "value", "parent", "label", "ien"]
        if prop in RESERVED_PROPS:
            return "{}_{}".format(prop, re.sub(r'\.', '_', propValue["fmId"]))
        # Issue: NCName ::= (Letter | '_') (NCNameChar)* in http://www.w3.org/TR/1999/REC-xml-names-19990114/#NT-NCName BUT JSON allows a number etc first. We insert a _ if there is a number first. TBD: best done in FMQL to be consistent.
        if re.match(r'\d', prop):
            return "_" + prop
        return prop
                
    def __reframe(self, record, isMultiple=False):

        if isMultiple == False:
            nrecord = {
                self.__idProp: record["uri"]["value"],
                "type": self.__newType(record)
            }
            self.__topRecord = nrecord # for ref back up of cnodes
        else:
            ien = record["uri"]["value"].split("-")[1].split("_")[0]
            nrecord = {"ien", ien}
            
        """
        Issue: until uses VistA time zone settings, FMQL "Z" (nominally UTC time)
        is actually local time, stampled as UTC. UTC is ideal - GUIs can go local
        but DB should be UTC. But must be real UTC
        
        Using: http://pytz.sourceforge.net/
    
        Ex/ "US/Mountain" ... pytz can list all
        
        TODO:
        - more on daylight savings: is_dst (see docs ... seems to be ambiguity in October)
        - take all logic from toMongoDate ie/ the 24:00:00 to 00:00:00 plus day
        - apply to V2 (over V1) based on passed in time zone
        """
        def fixBadUTCTime(badDTValue, realTZName):
            dt = datetime.strptime(badDTValue, "%Y-%m-%dT%H:%M:%SZ") # Z ignored
            tzinfo=pytz.timezone(realTZName)
            dttzed = tzinfo.localize(dt)
            dtutc = dttzed.astimezone(pytz.utc)
            return dtutc.strftime("%Y-%m-%dT%H-%M-%SZ")

        for prop in record:

            if prop in ["uri"]:
                continue

            propValue = record[prop]            
            nprop = self.__newProp(prop, propValue)

            if propValue["type"] == "cnodes": # fmType == "9"
                # Record stops inline but not they exist in top level (and reply)
                if "stopped" in propValue:
                    # FMQL 1.1 didn't record fmCount so allow for that.
                    try:
                        fmCount = int(propValue["fmCount"])
                    except:
                        fmCount = -1
                    # Note: missing subTypeId in V3 as not available
                    if "fmqlStopped" not in nrecord:
                        nrecord["fmqlStopped"] = {}
                        if "fmqlMaxStopped" not in self.__topRecord:
                            self.__topRecord["fmqlMaxStopped"] = -1
                    # v1.3 added fmCount but can be BAD ie/ <= REPLY CSTOP
                    nrecord["fmqlStopped"][nprop] = {"count": fmCount}
                    # Ensure top record has maximum list size
                    if self.__topRecord["fmqlMaxStopped"] < fmCount:
                        self.__topRecord["fmqlMaxStopped"] = fmCount
                    logging.info("Stopped property {} of {}, count {}".format(prop, record["uri"]["value"], fmCount))
                    continue
                nrecord[nprop] = []
                for i, srecord in enumerate(propValue["value"], 1):
                    nrecord[nprop].append(self.__reframe(srecord, True))
                continue
                        
            # Note: no time zone proper yet -- leaving for V2 FMQL
            if propValue["fmType"] == "1": # datetime
                if re.search(r'T00:00:00Z$', propValue["value"]):
                    nvalue = {"value": propValue["value"].split("T")[0], "type": "xsd:date"}
                else:
                    nvalue = {"value": fix24DateTime(propValue["value"]), "type": "xsd:dateTime"}
            elif propValue["fmType"] == "2": # treat numeric as literal just in case
                nvalue = propValue["value"]
            # or could just 'ivalue' in record[prop]
            elif propValue["fmType"] == "3": # type is literal
                nvalue = "{}:{}".format(propValue["ivalue"], propValue["value"])
            elif propValue["fmType"] == "4": # literal
                nvalue = propValue["value"]
            # 'datatype': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral too
            elif propValue["fmType"] == "5": 
                nvalue = re.sub(r'\r', '\n', propValue["value"])
            # 6: COMPUTED
            elif propValue["fmType"] in ["7", "8"]:
                nvalue = {"id": propValue["value"], "label": propValue["label"].split("/")[1]}
            # 9: MULTIPLE (above)
            elif propValue["fmType"] == "12": # Boolean, datetype == xsd:boolean
                # Fall back to literal (may revisit and suppress)
                if propValue["value"] not in ["true", "false"]:
                    nvalue = propValue["value"]
                else:
                    nvalue = True if propValue["value"] == "true" else False
            # Q C***, K VISTA
            # "10": "MUMPS",
            # "11": "IEN", # IEN match in .001
            else:
                raise Exception("UNEXPECTED TYPE {}".format(propValue["fmType"]))
                
            # Top level record has label <=> first prop (may drop)
            if len(nrecord) == 2 and "type" in nrecord:
                # 8989_5 and  8930_3 have ptr as .01
                if isinstance(nvalue, dict): # pter or date
                    nrecord["label"] = nvalue["label"] if "label" in nvalue else nvalue["value"]
                else: 
                    nrecord["label"] = nvalue
                
            nrecord[nprop] = nvalue
                            
        return nrecord
        
    def getTransformedByTypeCount(self):
        return self.__transformedByTypeCount
                
"""
Recache any stopped resources - exceptions if can't - and restore in a rebuilt
reply.

This ONLY works if DESCRIBING one at a time (top level) can safely get a broad node. From v3, see 'fmqlContainsTotal' (total number of contained elements seen apart from stopping) as well as 'fmqlMaxStopped' at the global level of a Reply
"""
def recacheForCSTOPs(stationNo, typId, fmqlIF, flushToRF=False):

    start = datetime.now()
    logLocn = re.sub(r'Data\/', 'Logs/', DATA_LOCN_TEMPL).format(stationNo)
    configLogging(stationNo, "REMOVECSTOP")
    logging.info("Begin removal of cstops from {}".format(typId))
    dataLocn = DATA_LOCN_TEMPL.format(stationNo)
    dataReplyStore = FMQLReplyStore(dataLocn)  
    # TMP: just to be careful 
    destDataLocn = DATARF_LOCN_TEMPL.format(stationNo) if flushToRF else dataLocn
    rfReplyStore = FMQLReplyStore(destDataLocn, useZip=True)     
    replyIter = dataReplyStore.iterator(onlyTypes=[typId])
    noRecachedStoppedResources = 0
    noRepliesWithStoppedResources = 0
    for i, reply in enumerate(replyIter, 1):
        replyFile = replyIter.currentReplyFile()
        if not re.search(r'\-S', replyFile):
            logging.info("Leaving {} as had NO stops".format(replyFile))
            continue # relies on Marker
        replyHasStoppedResources = False
        nresults = []
        for resource in reply["results"]:
            if "fmqlStopped" in resource:
                replyHasStoppedResources = True
                logging.info("Encountered stopped resource {} in {} - recaching individually".format(resource["_id"], replyFile))
                query = "DESCRIBE {} CSTOP {}".format(resource["_id"], 1000000)
                queryStart = datetime.now()
                resourceReply = fmqlIF.invokeQuery(query)
                logging.info("Re-cache took {}".format(str(datetime.now() - queryStart)))
                if "fmqlMaxStopped" in resourceReply: 
                    raise Exception("Re-query Stopped too {} - exiting".format(resource["_id"])) 
                nresource = resourceReply["results"][0]
                if "fmqlStopped" in nresource: # "legacy" check
                    raise Exception("Internal V3 Error: shouldn't happen as fmqlMaxStopped should stop it")
                noRecachedStoppedResources += 1
                nresults.append(nresource)
            else:
                nresults.append(resource)
        if not replyHasStoppedResources:
            raise Exception("V3 Internal Error: reply file marked with an -S but no stopped resources")
        reply["results"] = nresults
        del reply["fmqlMaxStopped"] # no need any more
        noRepliesWithStoppedResources += 1
        if not flushToRF: # only done if not flushing to RF
            logging.info("Deleting obsolete stopped reply file {}".format(replyFile))
            os.remove("{}{}".format(dataLocn, replyFile))
        logging.info("Reflushing {} w/o stops".format(re.sub(r'\-S', '', replyFile)))
        rfReplyStore.flush(reply)
    finish = datetime.now()
    if noRepliesWithStoppedResources:
        logging.info("FINISHED at {} in {}: recached {:,} resources from {:,} replies after seeing {:,} replies".format(
            finish,
            finish - start,
            noRecachedStoppedResources,
            noRepliesWithStoppedResources,
            i
        ))
    else:  
        logging.info("FINISHED at {} in {} after seeing NO STOPPED RESOURCEs in {:,} replies".format(
            finish,
            finish - start,
            i
        ))
        
"""
metaOfVistA for cutTime and key KSP ids including name - requires 8989_3 and 
PostMaster user needs to be cached first.

Naming:
- name | KSP domain name (first part of URL)
- longName | KSP default institution name
and notes (as expected), default institution IEN matches station number 

Note: older version used last 3.081, 409.84 too and they could be added
optionally later and from Data location.

TODO:
- KSP/production (PROD^XUPROD - prod info in KSP)
  - https://github.com/caregraf/fmqlutils/issues/4 ... about Entity extractors built in now to run to check my results with those
- Last 3.081,
- Build etc DESCRIBE LAST
- Last Exp DESCRIBE LAST 757_01 
- Parameters: any global settings worth (can be) taken? 
  ... S SYS=$S($D(VPRSYS):VPRSYS,1:$$GET^XPAR("SYS","VPR SYSTEM NAME"))
and
> Every Fileman installation has a SITE name and number. These values are
established when initializing Fileman, and are stored in the ^DD("SITE") and
^DD("SITE",1) nodes.
... need to go back to a DESCRIBE SYSTEM?
"""
def metaOfVistA(stationNo):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "metaOfVistA.json"
    try:
        metaInfo = json.load(open(jsnFl))
    except:
        pass
    else: 
        return metaInfo 

    fmqlReplyStore = FMQLReplyStore(DATAMETA_LOCN_TEMPL.format(stationNo))
    kspReply = fmqlReplyStore.lastReplyOfType("8989_3")
    postMasterReply = fmqlReplyStore.lastReplyOfType("200")
    installReply = fmqlReplyStore.lastReplyOfType("9_7")
    if not (kspReply and postMasterReply and installReply):
        raise Exception("Haven't run fmqlcacher ... META so can't see metaInfo")
    kspResource = kspReply["results"][0]
    postMasterResource = postMasterReply["results"][0]
    firstInstallResource = installReply["results"][0]

    metaInfo = {"stationNo": stationNo}    
    metaInfo["longName"] = kspResource["default_institution"]["label"]
    # ex/ PALO-ALTO.MED.VA.GOV
    metaInfo["domainName"] = kspResource["domain_name"]["label"]
    dnlMatch = re.match(r'([^\.]+)\.MED\.VA\.GOV$', kspResource["domain_name"]["label"])
    if dnlMatch:
        metaInfo["name"] = re.sub(r'-', ' ', dnlMatch.group(1)).title()
    defaultInstitutionIEN = kspResource["default_institution"]["id"].split("-")[1]
    if defaultInstitutionIEN == stationNo:
        metaInfo["isSNODefaultInstitutionIEN"] = True # ie/ 668 Spokane etc and name Spokane taken for long_name
    if "dns_ip" in kspResource:
        metaInfo["dnsIP"] = kspResource["dns_ip"]
    if "production" in kspResource:
        metaInfo["isProduction"] = kspResource["production"]
    for pprop in [("facility_iso", "iso"), ("facility_cio", "cio")]:
        if pprop[0] in kspResource:
            metaInfo[pprop[1]] = kspResource[pprop[0]]

    if "date_entered" in postMasterResource:
        metaInfo["dateEnteredPostMaster"] = postMasterResource["date_entered"]["value"]
    metaInfo["lastSignonPostMaster"]  = postMasterResource["last_signon_date_time"]["value"]
    metaInfo["cutDate"] = metaInfo["lastSignonPostMaster"].split("T")[0]
    
    # probably KERNEL - VIRGIN INSTALL 8.0 ... let's see (and may be very common across
    # VistA's.
    metaInfo["nameFirstInstall"] = firstInstallResource["name"] 
    if "date_loaded" in firstInstallResource:
        metaInfo["dateLoadedFirstInstall"] = firstInstallResource["date_loaded"]["value"]
        
    json.dump(metaInfo, open(jsnFl, "w"), indent=4)
                
    return metaInfo
        
"""
Accounts for 24:00:00 - moves to next day

TMP: will move to V2er
"""
def fix24DateTime(dtStr):
    if not re.search(r'T24:00:00Z?$', dtStr):
        return dtStr
    try:
        dt = datetime.strptime(dtStr.split("T")[0], "%Y-%m-%d")
    except: # don't fix - may be issue as leads to problem above or bad time TODO
        return dtStr
    dt = dt + timedelta(days=1)
    dtStr = datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")
    return dtStr
    
"""
FM's trailing number implies 0 for time so .1 = 10 o clock or
.101 == 10:10 and NOT 01 or 10.01. It also allows 24 ie/ 24:00:00.
For Python etc use, this should become 00:00:00 of the next day

(Off: S Y=3180304.1 X ^DD("DD") W Y)

Tests:
- 3180323 -> 2018-03-23
- 3180323.2 -> 2018-03-23T20:00:00
- 3180323.20 -> 2018-03-23T20:00:00 (FM doesn't have this)
- 3180323.203 -> 2018-03-23T20:30:00 
- 3180323.20304 -> 2018-03-23T20:30:40
- 3180323.02030499 -> 2018-03-23T02:03:04 (shortens)
- 3180323.235959 -> 2018-03-23T23:59:59 
- 3180323.240000 -> 2018-03-24T00:00:00 (start next day)
"""    
def mapFMDateTime(fmDateTime):
    dt = re.sub(r'^3', '20', fmDateTime.split(".")[0])
    if not re.search(r'\.', fmDateTime):
        dt = datetime.strptime(dt, "%Y%m%d")
        return datetime.strftime(dt, "%Y-%m-%d")
    tm = fmDateTime.split(".")[1][0:6]
    if tm == "":
        tm = "000000"
    if len(tm) == 1:
        tm = "{}0".format(tm)
    elif len(tm) == 3:
        tm = "{}{}0".format(tm[0:2], tm[2])
    elif len(tm) == 5:
        tm = "{}{}0".format(tm[0:4], tm[4])
    tm = tm.ljust(6, "0")
    if tm == "240000":
        dt = datetime.strptime(dt, "%Y%m%d")
        dt = dt + timedelta(days=1)
        return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")
    return datetime.strptime("{}.{}".format(dt, tm), "%Y%m%d.%H%M%S").strftime("%Y-%m-%dT%H:%M:%S") 
    
"""
EXPERIMENTAL (V2 Form now - will move to FMQL V2's base form/stop support)

Simple V2-based flipping Alg:
- RF == Reframe, DataRF 
- will Exception if CSTOP in ANY reply being walked - expect to be on full replies
- splits off [1] mresources and prop from parent reply (ie/ reflushes from
  original V2) and [2] makes a new mresources reply 
- mresources ID'ed in order seen in resource walk which won't be create
  order. 
- explicitInheritProps so container properties flow down. Example is appt create
date of 44.001 to 44.003; also inherits any container pter/parent pter properties
to cover multiples in multiples.
  
Invoke:
    fmqlIF = FMQLBrokerIF(config["hostname"], config["port"], config["access"], 
config["verify"])
    flip(stationNo, "38_1", "date_time_record_accessed", "38_11", "Date_Time_Record_Accessed", fmqlIF, 

TODO:
  * [ ] multipleProp as container name explicitly (issue of keeping hierarchy inherited?)
  * [ ] want 'multiple label prop' ie/ put label into multiple based on its .01 so just like others and then order of load in python etc won't matter
  * [ ] parent rezip too (right now too many) in RF
  * [ ] use prop name like 'patient' etc for parent (allow pass in)
  * [ ] ease of analysis: add in "count children" property ie/ {property}_count in parent
  * [ ] order - make children create ordered or fix typer create date calc logic <---- can't do Typer "after" reply

Ex/ 38.1 holds lot's of access logs 38.11. Some lead to CSTOPs and need
to be recached. Flip will end up with 38.11-less 38.1's and distinct, 5000
clumped 38.11's in DataRF
"""
def flip(stationNo, typId, multipleProp, multipleTypId, multipleTypName, explicitInheritProps=[], mlimit=7500, useRF=False):

    startFlip = datetime.now()
    logLocn = re.sub(r'Data\/', 'Logs/', DATA_LOCN_TEMPL).format(stationNo)
    configLogging(stationNo, "FLIP")
    logging.info("Begin flipping {} of {}".format(typId, multipleProp))
    sourceDataLocn = DATARF_LOCN_TEMPL.format(stationNo) if useRF else DATA_LOCN_TEMPL.format(stationNo)
    dataReplyStore = FMQLReplyStore(sourceDataLocn)        
    destDataLocn = DATARF_LOCN_TEMPL.format(stationNo)
    rfReplyStore = FMQLReplyStore(destDataLocn, useZip=True)
    replyIter = dataReplyStore.iterator(onlyTypes=[typId])
    includeParentLabel = True if typId not in PATIENT_NAME_TYPES else False
    mIEN = 0 # Note: only works if walk all multiples so each gets unique no
    noMReplies = 0
    noMResources = 0
    mreply = {"results": [], "fmql": {"TYPE": multipleTypId, "AFTERIEN": str(mIEN), "LIMIT": str(mlimit)}}
    ptUpProp = "{}_container_".format(multipleProp)
    cntMultipleProp = "{}_count_".format(multipleProp) # adding in counter to parent for mult
    noResourcesWOMultiple = 0
    for i, reply in enumerate(replyIter, 1):
        replyFile = replyIter.currentReplyFile()
        reply["lessResults"] = []
        for resource in reply["results"]:
            if multipleProp not in resource:
                if "fmqlStopped" in resource and multipleProp in resource["fmqlStopped"]:
                    raise Exception("Didn't expect to run against stopped for multiple {} but resource {} of {} stopped".format(multipleProp, resource["_id"], replyFile))
                noResourcesWOMultiple += 1
                reply["lessResults"].append(resource) # still add
                continue # legitimate (unusual but ...)
            # container_ hierarchy properties in resource 
            # ie/ if resource in resource, pull in (ex/ 44_003 in 44_001 and want 44
            cprops = set(prop for prop in resource if re.search(r'_container_$', prop))
            for mresource in resource[multipleProp]:
                if ptUpProp in mresource:
                    raise Exception("'{}' in source data as a property - reserved".format(ptUpProp))
                if "fmqlStopped" in mresource: # simple for now
                    raise Exception("Don't expect STOP within multiple of {}".format(replyFile))
                mIEN += 1 # doing simple IENs from complete walk 
                mId = "{}-{}".format(multipleTypId, mIEN)
                mresource["_id"] = mId
                del mresource["ien"] # NOT KEEPING THIS
                mresource[ptUpProp] = {"id": resource["_id"]}
                if includeParentLabel and "label" in resource:
                    mresource[ptUpProp]["label"] = resource["label"]
                for rprop in resource:
                    if not (re.search(r'_container_', rprop) or rprop in explicitInheritProps):
                        continue
                    if rprop in mresource:
                        raise Exception("Name clash between prop {} of multiple and of those of its containers".format(rprop))
                    mresource[rprop] = resource[rprop]
                mreply["results"].append(mresource)
                noMResources += 1
                if len(mreply["results"]) == mlimit:
                    noMReplies += 1
                    mReplyFile = rfReplyStore.flush(mreply)
                    logging.info("MReply {} - {:,} w/{:,} flushed, total mresources now {:,}".format(mReplyFile, noMReplies, mlimit, noMResources))
                    mreply = {"results": [], "fmql": {"TYPE": multipleTypId, "AFTERIEN": str(mIEN), "LIMIT": str(mlimit)}}
            # logging.debug("Removing another processed {} of {:,} from parent".format(multipleProp, len(resource[multipleProp])))
            if cntMultipleProp in resource:
                raise Exception("counter for multiple prop {} is already in resource so can't reset - name clash".format(cntMultipleProp))
            resource[cntMultipleProp] = str(len(resource[multipleProp]))
            del resource[multipleProp] # will reflush w/o multiple prop
            reply["lessResults"].append(resource)
        # Flushing mprop-less source reply
        reply["results"] = reply["lessResults"]
        del reply["lessResults"]
        rfReplyStore.flush(reply)
        logging.info("Finished and reflushed source reply {} with its {:,} results but removed {} if present".format(replyFile, len(reply["results"]), multipleProp))
    if len(mreply["results"]) > 0:
        noMReplies += 1
        rfReplyStore.flush(mreply)
        logging.info("Last MReply of {:,} flushed".format(noMReplies)) 
    logging.info("Finished flipping in {} - {:,} replies processed and reflushed, {:,} multiple replies flushed with {:,} records, {:,} never had the multiple".format(str(datetime.now() - startFlip), i, noMReplies, noMResources, noResourcesWOMultiple))

"""
Basic Data Location setup - Cache Locations (Data x 3, Schema, Log)

VISTA_DATA_BASE_DIR/{stationNo}/...

3 Data Directories (DataV1, Data, DataRF (flipped/Reframe), Schema, Logs, TmpWorking
"""
def ensureCacheLocations(stationNo):
    baseLocation = VISTA_DATA_BASE_DIR
    if not os.path.isdir(baseLocation):
        raise Exception("Base Location {} doesn't exist".format(baseLocation))
    if not os.access(baseLocation, os.W_OK):
        raise Exception("No Write Permission for Base Location {}".format(baseLocation))
    cacheLocation = baseLocation + stationNo + "/"
    if not os.path.isdir(cacheLocation):
        os.mkdir(cacheLocation)
    for dataDir in ["DataV1", "Data", "DataRF"]:
        dloc = cacheLocation + dataDir + "/"
        if not os.path.isdir(dloc):
            os.mkdir(dloc)
    schemaLocation = cacheLocation + "Schema/"
    if not os.path.isdir(schemaLocation):
        os.mkdir(schemaLocation)
    logLocation = cacheLocation + "Logs/"
    if not os.path.isdir(logLocation):
        os.mkdir(logLocation)
    tmpLocation = cacheLocation + "TmpWorking/"
    if not os.path.isdir(tmpLocation):
        os.mkdir(tmpLocation)
    metaDataLocation = cacheLocation + "DataMeta/"
    if not os.path.isdir(metaDataLocation):
        os.mkdir(metaDataLocation)
           
"""
configure logging

ex/ logName="cacherLog"
""" 
def configLogging(stationNo, logName, logLevel="DEBUG"):

    log = logging.getLogger('')
    
    try: 
        mlogLevel = {"DEBUG": logging.DEBUG, "INFO": logging.INFO}[logLevel]
        log.setLevel(mlogLevel)
    except:
        log.setLevel(logging.DEBUG)

    logDir = LOG_LOCN_TEMPL.format(stationNo)
    fh = handlers.RotatingFileHandler("{}{}".format(logDir, "{}.out".format(logName)), maxBytes=(1048576*5), backupCount=7)
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(format)
    log.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    format = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(format)
    log.addHandler(ch)

# ############################# Test Driver ####################################

import os
import sys

def main():

    # zipAllRepliesByType("/data/vista/999/DataV1/")
    # return
    
    replyStore = FMQLReplyStore("/data/vista/999/Data/")
    flTyp = "80"
    iter = replyStore.iterator(onlyTypes=["80"])
    for flJSON in iter:
        print("First {}".format(len(flJSON["results"])))
        break
    lastReplyOfType = replyStore.lastReplyOfType("80")
    print("Last Reply of Type {}, {}".format(len(lastReplyOfType["results"]), lastReplyOfType["fmql"]))
    print(json.dumps(lastReplyOfType["results"][0], indent=4))
        
if __name__ == "__main__":
    main()
    

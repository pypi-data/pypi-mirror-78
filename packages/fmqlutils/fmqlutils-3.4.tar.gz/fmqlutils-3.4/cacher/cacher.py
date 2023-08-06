#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2015-2020 caregraf

import os
import re 
import sys
import json
from datetime import datetime
from collections import defaultdict
import logging

from .fmqlIF import FMQLRESTIF, FMQLBrokerIF
from .cacherUtils import FMQLReplyStore, cacheFileToStore, ensureCacheLocations, V1RecordToV2, configLogging, DATAV1_LOCN_TEMPL, DATA_LOCN_TEMPL, SCHEMA_LOCN_TEMPL, LOG_LOCN_TEMPL, DATAMETA_LOCN_TEMPL
from .EXPLICIT_LS_CONFIGS import DEFAULT_LIMIT, DEFAULT_CSTOP, EXPLICIT_LIMITs, EXPLICIT_CSTOPs, FLIPs

"""
Basic FileMan data and schema cacher using FMQL.

TODO: FMQLSchemaStore to parallel FMQLReplyStore (may become FMQLDataStore)

Background: FileMan doesn't have enough indexes to support analytics. To fully analyze
data must first be cached. It can then be processed in a different DB (ex/ Mongo) or just
from disk.

Cache to "/data/vista/{stationNumber}/Data/" which it will create if it is absent

To test:
- du -h /data/{SYSTEM}/Data and /Schema
- old 2 download has 'File 2, limit 500 : all 1032150 of file 2 in 4:49:22.820342'

Invoke: 

    > nohup python -u cacher.py config/nv.json 8989_3 > cache.out & and tail -f cache.out; monitor with ps -aux, kill with kill -9 {pid}

See comment in main below for exact argument options.

ForCount is useful

    > fmqlcacher nconfigs/nv.json FORCOUNT10-20 
    
getting files with a count between 10 and 20
"""

# ########################## Data #########################

def cacheData(config):

    start = datetime.now()
            
    systemId = config["stationNumber"] if "name" not in config else "{} [{}]".format(config["name"], config["stationNumber"])
    logging.info("Caching Data of VistA {} [PID {}]".format(systemId, os.getpid()))
    
    fmqlIF = makeFMQLIF(config)
    jreply = fmqlIF.invokeQuery("ABOUT")
    if "error" in jreply:
        locn = DATAV1_LOCN_TEMPL.format(config["stationNumber"])
        logging.info("Older FMQL - caching in {}".format(locn))
        isV1 = True
    else:
        locn = DATA_LOCN_TEMPL.format(config["stationNumber"])
        logging.info("Using FMQL {} - caching in {}".format(jreply["version"], locn))
        isV1 = False
    useZip = config["useZip"] if "useZip" in config else True
    fmqlReplyStore = FMQLReplyStore(locn, useZip=useZip, makeDir=False)
    
    """
    Tracking Cache State
    - zeros is key to avoid trying and retrying the empty
    - partials arises with FORCOUNT where actual count >> FM's #.
    - TODO: complete now is NOT filled in
    ... These actual #'s can also be used in reports to replace FM's estimates.
    """
    def migrateOlderZeroAndPartials(stationNumber, trackFilesCached): # tmp til all migrated
        trackZeroFile = "{}trackZeroFiles.json".format(LOG_LOCN_TEMPL.format(stationNumber))
        try:
            zeroFiles = json.load(open(trackZeroFile))
        except:
            pass
        else:
            trackFilesCached["zeros"] = zeroFiles
            os.remove(trackZeroFile)
        trackMaxedFile = "{}trackForCountMaxedFiles.json".format(LOG_LOCN_TEMPL.format(stationNumber))
        try:
            hitMaxFiles = json.load(open(trackMaxedFile))
        except:
            pass
        else:
            trackFilesCached["partials"] = hitMaxFiles 
            os.remove(trackMaxedFile)
    trackFilesCachedFile = "{}trackFilesCached.json".format(LOG_LOCN_TEMPL.format(config["stationNumber"]))
    try:
        trackFilesCached = json.load(open(trackFilesCachedFile))
    except: # note: not yet noting/counting completes
        trackFilesCached = {"zeros": [], "partials": {}}
        migrateOlderZeroAndPartials(config["stationNumber"], trackFilesCached)
    originalZeroFilesCount = len(trackFilesCached["zeros"])
    originalPartialFilesCount = len(trackFilesCached["partials"])
    
    excludeTypes = set(config.get("excluded", []))
    includeTypes = set(config.get("included", [])) 
    includeCountMax = config.get("includeCountMax", -1)
    includeCountMin = config.get("includeCountMin", -1)  

    #
    # Option of Count Order or Id Order
    #
    # ... may retire: ala FMQLReplyStore, support a Schema Store
    # 
    def filesFromSchema(fmqlEP, schemaCacheLocation, typeOrder=False):
        """
        From SELECT TYPES - if in cache just load and read. Otherwise cache and
        then load and read.
        """
        query = "SELECT TYPES TOPONLY" # doing TOPONLY and not POPONLY in case POP is wrong
        cacheFile = re.sub(r' ', "_", query) + ".json"
        try:
            reply = json.load(open(schemaCacheLocation + cacheFile))
        except Exception:
            logging.info("First time through - must (re)cache {} to {} ...".format(query, schemaCacheLocation))
            reply = fmqlEP.invokeQuery(query)
            json.dump(reply, open(schemaCacheLocation + cacheFile, "w"))
        if typeOrder: # used if included explicit - otherwise order biggest first
            oresults = sorted(reply["results"], key=lambda res: float(re.sub(r'\_', '.', res["number"])))
        else:      
            oresults = sorted(reply["results"], key=lambda res: int(res.get("count", "0")), reverse=True)
        filesInOrder = []
        for i, result in enumerate(oresults, 1):
            fileId = re.sub(r'\.', '_', result["number"])
            filesInOrder.append({"id": fileId, "count": int(result.get("count", "0"))})
        logging.info("Returning {} top files - not all will have data".format(len(filesInOrder)))
        return filesInOrder

    defaultLimit = config["defaultLimit"]
    defaultCStop = config["defaultCStop"]
    problem = False
    cacheUpdated = False
    # cache in type order if list is explicit - otherwise count order (will
    # apply to typeSizeGroup too
    typeOrder = True if len(includeTypes) else False 
    schemaCacheLocation = SCHEMA_LOCN_TEMPL.format(config["stationNumber"])
    for i, fli in enumerate(filesFromSchema(fmqlIF, schemaCacheLocation, typeOrder=typeOrder), 1):

        if fli["id"] in excludeTypes:
            logging.debug("{}. File {} expecting count of {} - EXCLUDED SO SKIPPING".format(i, fli["id"], fli["count"]))
            continue

        if fli["id"] in trackFilesCached["zeros"]:
            logging.debug("{}. File {} expecting count of {} - KNOWN ZERO SO SKIPPING".format(i, fli["id"], fli["count"]))
            continue

        if includeTypes and fli["id"] not in includeTypes:
            logging.debug("{}. File {} expecting count of {} - NOT IN EXPLICIT INCLUDE LIST SO SKIPPING".format(i, fli["id"], fli["count"]))
            continue
                    
        if not (includeCountMax == -1 or includeCountMin == -1):
            try:
                fliCount = int(fli["count"])
            except:
                pass
            else:
                if fli["count"] < 0:
                    logging.debug("{}. File {} has invalid count of {} which we are treating as zero".format(i, fli["id"], fli["count"])) # second check below handles this
                if fli["count"] > includeCountMax:
                    logging.debug("{}. File {} has expected count of {:,} which exceeds max count {:,} so skipping".format(i, fli["id"], fli["count"], includeCountMax)) 
                    continue
                if includeCountMin != 0 and fli["count"] < includeCountMin:            
                    logging.debug("{}. File {} has expected count of {:,} which is below min count {:,} so skipping".format(i, fli["id"], fli["count"], includeCountMin)) 
                    continue
                # don't keep caching if actually bigger than threshold despite FM count
                maxNumber = includeCountMax
        else:
            maxNumber = -1 # turn off
                            
        logging.info("{}. File {} expecting count of {}{}".format(i, fli["id"], fli["count"], " ** Note POP says 0 but trying anyhow" if fli["count"] == 0 else ""))
            
        if "explicitLimits" in config and fli["id"] in config["explicitLimits"]:
            limit = config["explicitLimits"][fli["id"]]
        else:
            limit = defaultLimit
        if isV1:
            limit = int(limit/2) # size is for FMQL V10 - ~ 2x V1

        if "explicitCStops" in config and fli["id"] in config["explicitCStops"]:
            cstop = config["explicitCStops"][fli["id"]]
        else:
            cstop = defaultCStop

        try: # may get license error - make sure save zero files first
            cacheResult = cacheFileToStore(fmqlIF, fmqlReplyStore, fli["id"], limit=limit, cstop=cstop, maxNumber=maxNumber)
            if cacheResult == "HITMAX":
                trackFilesCached["partials"][fli["id"]] = maxNumber
                cacheUpdated = True # not saving result of complete
            elif cacheResult != "COMPLETE": # NO_SUCH_FILE, EMPTY_FILE 
                # will include 'no such files' and 'zero files'
                trackFilesCached["zeros"].append(fli["id"])
                cacheUpdated = True
            # not (yet) tracking completes (# is available by walking cache)
        except Exception as e:
            logging.exception(e)
            problem = True
            break

    timeTaken = str(datetime.now() - start)
    
    zeroFileMU = ""
    partialFileMU = ""
    if cacheUpdated:
        json.dump(trackFilesCached, open(trackFilesCachedFile, "w"))
        if len(trackFilesCached["zeros"]) > originalZeroFilesCount:
            zeroFileMU = " - zero file count went from {:,} to {:,}".format(originalZeroFilesCount, len(trackFilesCached["zeros"]))
        if len(trackFilesCached["partials"]) > originalPartialFilesCount:
            partialFileMU = " - hit max file ('partials') count went from {:,} to {:,}".format(originalPartialFilesCount, len(trackFilesCached["partials"]))

    if problem:
        logging.info("Caching finished UNSUCCESSFULLY at {} and took {}".format(datetime.now(), timeTaken))
    else:
        logging.info("Caching finished successfully at {} and took {}{}{}".format(datetime.now(), timeTaken, zeroFileMU, partialFileMU))
        
# ####################### Schema #####################
    
def cacheSchemas(config):

    start = datetime.now()
    
    systemId = config["stationNumber"] if "name" not in config else "{} [{}]".format(config["name"], config["stationNumber"])
    logging.info("Caching Schema of VistA {} [PID {}]".format(systemId, os.getpid()))

    fmqlIF = makeFMQLIF(config)
    
    schemaCacheLocation = SCHEMA_LOCN_TEMPL.format(config["stationNumber"])
    query = "SELECT TYPES"
    try:
        jreply = json.load(open(schemaCacheLocation + "SELECT_TYPES.json"))
    except:
        logging.info("First time through - must (re)cache {} to {} ...".format(query, schemaCacheLocation))
        jreply = fmqlIF.invokeQuery(query)
        json.dump(jreply, open(schemaCacheLocation + "SELECT_TYPES.json", "w"))

    fileIds = [re.sub(r'\.', "_", result["number"]) for result in jreply["results"]]
    logging.info("Must cache schema of {} files".format(len(fileIds)))

    alreadyCached = [re.match(r'SCHEMA\_([^\.]+)', f).group(1) for f in os.listdir(schemaCacheLocation) if os.path.isfile(os.path.join(schemaCacheLocation, f)) and re.search('\.json$', f) and re.match("SCHEMA_", f)]
    for i, fileId in enumerate(fileIds, 1):
        if fileId in alreadyCached:
            logging.info("{}. Schema of {} Already Cached".format(i, fileId))
            continue
        logging.info("{}. Caching Schema of {}".format(i, fileId))
        query = "DESCRIBE TYPE " + fileId
        queryStart = datetime.now()
        jreply = fmqlIF.invokeQuery(query)
        json.dump(jreply, open(schemaCacheLocation + "SCHEMA_" + fileId + ".json", "w"))

    # Phase 2 - cache SELECT TYPE REFS
    alreadyCached = [re.match(r'REFS\_([^\.]+)', f).group(1) for f in os.listdir(schemaCacheLocation) if os.path.isfile(os.path.join(schemaCacheLocation, f)) and re.search('\.json$', f) and re.match("REFS\_", f)]
    for i, fileId in enumerate(fileIds, 1):
        if fileId in alreadyCached:
            logging.info("{}. Refs of {} Already Cached".format(i, fileId))
            continue
        logging.info("{}. Caching Refs of {}".format(i, fileId))
        query = "SELECT TYPE REFS " + fileId
        queryStart = datetime.now()
        jreply = fmqlIF.invokeQuery(query)
        json.dump(jreply, open(schemaCacheLocation + "REFS_" + fileId + ".json", "w"))
        
    timeTaken = str(datetime.now() - start)
    logging.info("Caching SCHEMA/REF finished successfully at {} for {} files and took {}".format(datetime.now(), len(fileIds), timeTaken))
    
# ######################## DataMeta ##########################
    
"""
Cache the Meta Data needed to make a Meta Declaration for a VistA. Decoupled from
the creation of the meta record which is a separate function.

ADD?: may add other key files such as the code schemes, patient created first
etc. See what the following does first. This is ONLY meant to be cursory and
necessary (last sign on) data.
- LASTS:
  - http://localhost:9100/fmqlEP?fmql=DESCRIBE+LAST+757_01 --> last code added
  - last 3.081 or vital or ...
- parameters 8989_3 ... key global ones
- KSP: isProduction 
"""
def cacheDataMeta(config):
  
    fmqlIF = makeFMQLIF(config)
    fmqlReplyStore = FMQLReplyStore(DATAMETA_LOCN_TEMPL.format(config["stationNumber"]))
    v1ToV2 = V1RecordToV2(forMongo=True)

    if fmqlReplyStore.lastReplyOfType("8989_3") == None:
        cacheFileToStore(fmqlIF, fmqlReplyStore, "8989_3", 1, 0, 1)
        kspReply = fmqlReplyStore.lastReplyOfType("8989_3")
        kspResource = kspReply["results"][0]
        if "_id" not in kspResource:
            kspResource = v1ToV2.transform(kspResource) 
            kspReply["results"] = [kspResource]
            fmqlReplyStore.flush(kspReply)
        logging.info("Cached KSP for Meta for first time")
    else:
        logging.info("KSP Already Cached")
    
    # Using for 'last sign on' as PostMaster is daily and for first user
    # as always the first created
    if fmqlReplyStore.lastReplyOfType("200") == None:
        cacheFileToStore(fmqlIF, fmqlReplyStore, "200", 1, 0, 1) 
        postMasterReply = fmqlReplyStore.lastReplyOfType("200")
        postMasterResource = postMasterReply["results"][0]
        if "_id" not in postMasterResource:
            postMasterResource = v1ToV2.transform(postMasterResource)
            if postMasterResource["_id"] != "200-.5":
                raise Exception("cacheDataMeta assumption wrong - .5 is not first 200")
            postMasterReply["results"] = [postMasterResource]
            fmqlReplyStore.flush(postMasterReply)
        logging.info("Cached Post Master User for Meta for first time")
    else:
        logging.info("Post Master User Already Cached")
    
    # Always KERNEL - VIRGIN INSTALL 8.0 ?
    if fmqlReplyStore.lastReplyOfType("9_7") == None:
        cacheFileToStore(fmqlIF, fmqlReplyStore, "9_7", 1, 0, 1) 
        firstInstallReply = fmqlReplyStore.lastReplyOfType("9_7")
        firstInstallResource = firstInstallReply["results"][0]
        if "_id" not in firstInstallResource:
            firstInstallResource = v1ToV2.transform(firstInstallResource)
            firstInstallReply["results"] = [firstInstallResource]
            fmqlReplyStore.flush(firstInstallReply)
        logging.info("Cached First Install for Meta for first time")
    else:
        logging.info("First Install for Meta Already Cached")
    
# #################### FMQLIF wrapper (schema and data) #######################
    
def makeFMQLIF(config):
    # Should work for CSP and 'regular' REST endpoint
    if "fmqlEP" in config:
        fmqlIF = FMQLRESTIF(config["fmqlEP"], epWord=config.get("fmqlQuery", "fmql"))
        logging.info("Using REST Interface {}".format(config["fmqlEP"]))
    else:
        if "broker" not in config:
            raise Exception("Exiting - invalid 'config': neither 'broker' nor REST ('fmqlEP') settings available")
        # Must a/c for cypher in OSEHRA being different than Cypher in regular production VISTA (or maybe not if Vagrant VISTA is changed!)
        osehraVISTA = config["broker"].get("osehraVISTA", False) 
        fmqlIF = FMQLBrokerIF(config["broker"]["hostname"], config["broker"]["port"], config["broker"]["access"], config["broker"]["verify"], osehraVISTA=osehraVISTA)
        logging.info("Using RPC Broker Interface {}:{}".format(config["broker"]["hostname"], config["broker"]["port"]))
    return fmqlIF

# ############################# Driver ####################################

"""
./cacher.py {SYSTEM CONFIG FILE} META|SCHEMA|{TYP}|FORCOUNT{MIN\d+-MAX\d+}|{TYPE GROUP CONFIG FILE}

Always pass in "system config" and then can do one type or meta or schema or have a specific configuration override defaults and cover > one type.

- system config file is always needed to allow remote access. It defines
  - stationNumber (and [name])
  - end point/addressing parameters
  - [default cstop and limit settings for the system] (defaultCStop, defaultLimit)
  - [forcount min and max will cache types whose count (per the schema) fits into a range
    ... this is useful for caching smaller files (0-9, 10-49, 50-... etc. and note
    that FLIPs are excluded from such range caching to avoid problems.
  - [logLevel]
  - [explicitLimits, explicitCStops that override built in defaults for a specific system]
  ... it will NOT have 'included' as this goes in cross system type group files.
  
- type list config allows sets of types to be specified: typical example would be 
sets for certain report types. Format is
    {
        "name": "my group",
        "included": [... types
    }
  note that if a system doesn't have a file (per its schema), the cacher won't ask for it.
  This allows us to have generic type group files.
  
The role of EXPLICT_LS_SETTINGS: this sets type limit and cstop based on previous runs
against VistA. The default's may be overridden in the System Config file. Where there is
no setting for a type, the defaults are used.
"""
def main():

    assert sys.version_info >= (3, 4)
    
    try:
        sysConfigName = sys.argv[1].split(".")[0]
        arg2 = sys.argv[2]
    except IndexError:
        raise SystemExit("Usage _EXE_ {SYSTEM CONFIG FILE} META|SCHEMA|{TYP}|FORCOUNT{MIN-MAX}|explicit type list file}")
    
    if not os.path.isfile("{}.json".format(sysConfigName)):
        raise SystemExit("No system config file {}.json - exiting".format(sysConfigName))
    try:
        config = json.load(open("{}.json".format(sysConfigName)))
        if not ("stationNumber" in config and re.match(r'\d{3}$', config["stationNumber"])):
            raise SystemExit("Need three digit station number in config")
 
    except:
        raise SystemExit("Invalid system config {}.json - can't parse".format(sysConfigName))

    ensureCacheLocations(config["stationNumber"])
        
    configLogging(config["stationNumber"], "cacherLog", config["logLevel"] if "logLevel" in config else "INFO")
                
    if arg2 == "META":
        try:
            cacheDataMeta(config)
        except Exception as e:
            raise SystemExit("Can't cache meta: {}".format(str(e)))
        else:
            return
    
    if arg2 == "SCHEMA": 
        try:
            cacheSchemas(config)
        except Exception as e:
            raise SystemExit("Can't cache schema: {}".format(str(e)))
        else:
            return
            
    # Two constants - if no explicit setting then these rule
    if "defaultLimit" not in config:
        config["defaultLimit"] = DEFAULT_LIMIT
    if "defaultCStop" not in config:
        config["defaultCStop"] = DEFAULT_CSTOP 
            
    # Merging default explicit limits and superseeding with any set in system config
    if "explicitLimits" in config:
        EXPLICIT_LIMITs.update(config["explicitLimits"])
    config["explicitLimits"] = EXPLICIT_LIMITs
    if "explicitCStops" in config:
        EXPLICIT_CSTOPs.update(config["explicitCStops"])
    config["explicitCStops"] = EXPLICIT_CSTOPs
    
    if re.match(r'FORCOUNT', arg2):
        try:
            mtch = re.match(r'FORCOUNT(\d+)\-(\d+)$', arg2)
            config["includeCountMax"] = int(mtch.group(2))
            config["includeCountMin"] = int(mtch.group(1))
            # As a safety measure, FLIPs are excluded
            if "excluded" in config:
                config["excluded"].extend(FLIPs)
            else:
                config["excluded"] = FLIPs
        except:
            raise SystemExit("FORCOUNT Setting wrong")
    elif re.match(r'[\d\_]+$', arg2):
        typ = arg2
        config["included"] = [typ]
    else: # May override anything AND add an firstAFTERIENs
        typesConfigName = arg2.split(".")[0]
        if not os.path.isfile("{}.json".format(typesConfigName)):
            raise SystemExit("No types config file {}.json - exiting".format(typesConfigName))
        try:
            typesConfig = json.load(open("{}.json".format(typesConfigName)))
        except:
            raise SystemExit("Invalid types config {}.json - can't parse".format(typesConfigName))
        if "included" not in typesConfig:
            raise SystemExit("Expect 'included' to be set in types configuration files")
        config["included"] = typesConfig["included"]
        
    try:
        cacheData(config)
    except Exception as e:
        raise SystemExit("Can't cache data: {}".format(str(e)))

if __name__ == "__main__":
    main()


#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import sys
import json
import shutil
from datetime import datetime
import re
from collections import defaultdict
from statistics import median

from ..cacher.cacherUtils import FMQLReplyStore, convert_size, DATAV1_LOCN_TEMPL, DATA_LOCN_TEMPL

"""
TODO: 
- ZERO files -- tied that in (and compare with reports of 0 but not etc)
  - already reports < 0!
- PARTIAL FILES AS MAX HIT 
  - tie that in
- CUT down and just have cache completelness report
- hone as "mu's" and consider what should be in "reusable" utils
- store time in replies --- use ... median time taken as well as size!
        jreply["queryTook"] = queryTook # time taken (queryCached time is set in store)
        # note time as UTC (can change to local times in a display)
        jreply["queryCached"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


Report state of data in DataV1 | Data Cache to:
- Note degree of completeness: first thing to run ie/ all to do 
- Suggest better LIMIT settings
  - LIMIT to get maximum reply size of ~8.5M
  - median << biggest => cstops in there so very "peaky"
"""
def reportCacheHealth(stationNumber, isV1):

    print("# Reporting Cache Health for {}\n".format(stationNumber))

    reportCompleteness(stationNumber, isV1)   
    reportLimitToSize(stationNumber, isV1)

    print("")
    
"""
Using ReplyStore basic methods, report on its completeness
"""
def reportCompleteness(stationNumber, isV1): # based on FM numbers

    """
    Clinical PATIENT+ (not audits or a/cs etc) - overlap with VPR's source files
    but has extras like 601_85 (Mental Health) and Appointments isn't explicit
    as 2.98 is a multiple of 2
    
    Note: 702 may NOT be one but it is referenced by VPR file VPRDMC.m
    """
    CLINPATIENTTYPES = [
        
        "100", "9000010", "9000010_18", "8925", "409_68", "120_5", "9000010_06", "9000010_07", "9000010_23", "52", "601_85", "27_11", # top 40 (majority not)
        
        "2", "120_8", "9000011", "63", "68", "55", "70", "74", "75_1", "9000010_11", "9000010_12", "704_117", "405", "130", "123", "26_13", "702"
                
    ]

    dm1Location = DATAV1_LOCN_TEMPL.format(stationNumber) if isV1 else DATA_LOCN_TEMPL.format(stationNumber)
    fmqlReplyStore = FMQLReplyStore(dm1Location, makeDir=False)
    availableTypes = fmqlReplyStore.availableTypes()
    stoppedTypes = fmqlReplyStore.stoppedTypes()
    countByType = fmqlReplyStore.expectedTypeCounts()
    
    MAXTHRESHOLDLABEL = "MORE THAN TEN MILLION"
    currentThreshold = MAXTHRESHOLDLABEL
    typByThreshold = defaultdict(list)
    thresholds = [[10000000, "< TEN MILLION", False], [1000000, "< ONE MILLION", False], [100000, "< ONE HUNDRED THOUSAND", False], [50000, "< FIFTY THOUSAND", False], [10000, "< TEN THOUSAND", False], [1000, "< ONE THOUSAND", False], [100, "< ONE HUNDRED", False], [10, "< TEN", False], [2, "SINGLETONS", False], [1, "ZERO", False], [0, "LESS THAN ZERO (WRONG)", False]]
    print("\n## Completeness\n")
    totalRecords = sum(countByType[typ]["count"] for typ in countByType if countByType[typ]["count"] > 0)
    cachedSoFar = 0
    mu = "\# | Type | Expected Size | DONE?\n--- | --- | --- | --- \n"
    for i, typ in enumerate(sorted(countByType, key=lambda x: countByType[x]["count"], reverse=True), 1):
        for thresInfo in thresholds:
            if not thresInfo[2]:
                if countByType[typ]["count"] < thresInfo[0]:
                    mu += "&nbsp; | &nbsp; | __{}__ | &nbsp;\n".format(thresInfo[1])
                    thresInfo[2] = True  
                    currentThreshold = thresInfo[1]
                break
        typByThreshold[currentThreshold].append(typ)
        if typ in availableTypes:
            doneMU = "__YES__" if typ not in stoppedTypes else "__YES (STOPPED)__"
            cachedSoFar += countByType[typ]["count"] # crude as only partial counts as whole
        else:
            doneMU = ""
        labelMU = countByType[typ]["label"] if typ not in CLINPATIENTTYPES else "__{}__".format(countByType[typ]["label"])
        countMU = "{:,}".format(countByType[typ]["count"])
        if countByType[typ]["count"] > 0:
            percCount = float(countByType[typ]["count"])/float(totalRecords) * 100
            if percCount > 0.009:
                countMU += "/{:.2f}%".format(percCount)
        mu += "{} | {} ({}) | {} | {}\n".format(i, labelMU, typ, countMU, doneMU)
    mu += "\n"
    mu += "__Cached so far:__ < {:,} out of {:,} records (fileman count)\n\n".format(cachedSoFar, totalRecords)
    print(mu)
    print("")
    print("Types by threshold (can use in configs)")
    print("")
    thresholds.insert(0, [-1, MAXTHRESHOLDLABEL])
    for i, thresInfo in enumerate(thresholds, 1):
        thresId = thresInfo[1]
        cntRecordsInThreshold = sum(countByType[typ]["count"] for typ in typByThreshold[thresId])
        cntRecordsInThresholdC = cntRecordsInThreshold if cntRecordsInThreshold > 0 else 0
        percRecordsInThreshold = float(cntRecordsInThresholdC)/float(totalRecords) * 100
        print("{}. {} ({}/{:,}/{:.2f}%) - {}".format(i, thresId, len(typByThreshold[thresId]), cntRecordsInThresholdC, percRecordsInThreshold, json.dumps(typByThreshold[thresId])))
        print("")
    print("")
    print("")
    
def reportLimitToSize(stationNumber, isV1):

    print("## Limit to Size Issues ({} Form)".format("V1" if isV1 else "V10"))
    print("")
    
    dm1Location = DATAV1_LOCN_TEMPL.format(stationNumber) if isV1 else DATA_LOCN_TEMPL.format(stationNumber)
    fmqlReplyStore = FMQLReplyStore(dm1Location, makeDir=False)
            
    sizeByFileTypeByFile = fmqlReplyStore.replySizeByType()
                    
    TARGET_MAX_REPLY_IN_BYTES = 8900000 # 8.5MB - raw or actual, not zipped
    
    typsWithNewLimits = {}
    amu = "Type | Limit | \# Replies | Median | Average | Biggest | Fraction | New Limit\n--- | --- | --- | --- | --- | ---\n"
    for flTyp in sorted([flTyp for flTyp in sizeByFileTypeByFile], key=lambda x: float(re.sub(r'\_', '.', x))):
        sys.stdout.write('..{}'.format(flTyp))
        sys.stdout.flush()
        sizes = [sizeByFileTypeByFile[flTyp][fl]["actual"] for fl in sizeByFileTypeByFile[flTyp]]
        mdian = median(sizes)
        biggest = max(sizes)
        avg = sum(sizes)/float(len(sizes))
        noReplies = len(sizeByFileTypeByFile[flTyp])
        fraction = round((float(biggest) / float(TARGET_MAX_REPLY_IN_BYTES)), 1)
        """
        Don't be too exact - within 0.9 to 1.1 of the size is fine
        and if only one reply that's small - then that's fine
        """
        if (noReplies > 1 and (fraction > 1.1 or fraction < 0.9)) or (noReplies == 1 and fraction > 1.1):
            # get limit from last reply
            lastReply = fmqlReplyStore.lastReplyOfType(flTyp)
            limit = int(lastReply["fmql"]["LIMIT"])
            newLimit = int(round(limit / fraction, 0)) 
            mu = "{flTyp} | {limit} | {noReplies} | {mdian} | {avg} | {biggest} | {fraction} | {newLimit}\n".format(flTyp=flTyp, limit=limit, noReplies=noReplies, mdian =convert_size(mdian), avg=convert_size(avg), biggest=convert_size(biggest), fraction=fraction, newLimit=newLimit)
            amu += mu
            typsWithNewLimits[flTyp] = str(newLimit)
            
    print("")
    print("Total Files: {} - One Reply Files: {} - Need new Limit Files: {}".format(len(sizeByFileTypeByFile), sum(1 for flTyp in sizeByFileTypeByFile if len(sizeByFileTypeByFile[flTyp]) == 1), len(typsWithNewLimits)))
    print("Cache uses Zip (size is actual so no effect): {}".format(fmqlReplyStore.usesZip()))
    print("Size threshold: {}".format(convert_size(TARGET_MAX_REPLY_IN_BYTES)))
    print("")
    print(amu)
    print("")
    print("List of types with new limits: {}".format(json.dumps(typsWithNewLimits)))
    print("... add to Cacher config LIMIT setting")
    print("")
    print("")

# ############################# Driver ####################################

def main():

    assert sys.version_info >= (3, 3)

    USAGE = "Usage _EXE_ STATIONNO [V1]"
    try:
        stationNumber = sys.argv[1]
    except IndexError:
        raise SystemExit(USAGE)

    isV1 = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "V1":
            isV1 = True
        else:
            raise SystemExit(USAGE)

    reportCacheHealth(stationNumber, isV1)
    
if __name__ == "__main__":
    main()

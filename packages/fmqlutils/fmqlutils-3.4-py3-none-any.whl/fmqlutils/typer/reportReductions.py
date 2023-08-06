#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import sys
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date
import logging

from ..reporter.reportUtils import reportAbsAndPercent

from .reduceType import DEFAULT_MAX_NOMINAL_VALUES
    
# ################################## REPORT ##################################
                    
def reportReductions(typeDatas, outputFileName): # may get big
    try:
        os.remove(outputFileName) 
    except:
        pass
    if len(typeDatas) == 0:
        return # nothing to report
    flOut = open(outputFileName, "a")
    if len(typeDatas) == 1:
        flOut.write(reportReduction(typeDatas[0]))
        flOut.close()
        return
    allTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" not in typeData]
    if len(allTypeDatas):
        if len(allTypeDatas) != 1:
            raise Exception("Expect one and only one ALL type data in a type data list")
        flOut.write("# All/Summary Report\n\n")
        flOut.write(reportReduction(allTypeDatas[0]))
    subTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" in typeData]
    subTypeProp = subTypeDatas[0]["_subTypeId"].split(":")[0]
    flOut.write("\n\n# {:,} Sub Reports split by property \"{}\"\n\n".format(len(subTypeDatas), subTypeProp))
    for typeData in subTypeDatas:
        flOut.write(reportReduction(typeData))
    flOut.write("\n\n")
    flOut.close()
    
def reportReduction(typeData): # can use for a pass 2 as self contained

    def dtDelta(first, then): # Crude now - TODO more on timedelta, divmod and total_seconds 
        # delta = datetime.strptime(re.sub(r'Z$', '', then), "%Y-%m-%dT%H:%M:%S" ) - datetime.strptime(re.sub(r'Z$', '', first), "%Y-%m-%dT%H:%M:%S" )
        delta = int(then.split("-")[0]) - int(first.split("-")[0])
        return delta

    idMU = typeData["_id"] if "_label" not in typeData else "{} ({})".format(typeData["_id"], typeData["_label"])
    
    if "_subTypeId" in typeData:
        subTypeProp = typeData["_subTypeId"].split(":")[0]
        subTypeValue = typeData["_subTypeId"][len(subTypeProp) + 1:] # allow ':' prop val
        idMU += " property \"{}\" value \"{}\"".format(subTypeProp, subTypeValue)
        
    mu = "## {} Report\n\n".format(idMU)
    
    total = typeData["_total"]
    if "_numberFiltered" in typeData:
        filtered = typeData["_numberFiltered"]
        complete = total + filtered
        mu += "Total Selected: {}\n".format(reportAbsAndPercent(typeData["_total"], complete))
        mu += "Filtered: {}\n".format(reportAbsAndPercent(filtered, complete))
    else:
        mu += "Total: {:,}\n".format(total)
        
    if "_firstIEN" in typeData:
        mu += "First IEN: {}\n".format(typeData["_firstIEN"])  
              
    if "_createDateProp" in typeData:
        mu += "Create Date Property: {}\n".format(typeData["_createDateProp"])
        if typeData["_createDateProp"] in typeData:
            createDatePropInfo = typeData[typeData["_createDateProp"]]
            if "firstCreateDate" in createDatePropInfo:
                mu += "First Create Date: {}\n".format(createDatePropInfo["firstCreateDate"])
                mu += "Last Create Date: {}\n".format(createDatePropInfo["lastCreateDate"])
                delta = dtDelta(createDatePropInfo["firstCreateDate"], createDatePropInfo["lastCreateDate"])
                if delta != 0:
                    mu += "Span: {} years\n".format(delta)
                
    # prop that is the first or last date can vary
    if "_firstDateProps" in typeData:
        mu += "Order of Date Values (first/last dates):\n"
        mu += "\tFirsts:\n"
        for dp in sorted(typeData["_firstDateProps"], key=lambda x: typeData["_firstDateProps"][x], reverse=True):
            mu += "\t\t{} - {:,}\n".format(dp, typeData["_firstDateProps"][dp])  
        mu += "\tLasts:\n"
        for dp in sorted(typeData["_lastDateProps"], key=lambda x: typeData["_lastDateProps"][x], reverse=True): 
            mu += "\t\t{} - {:,}\n".format(dp, typeData["_lastDateProps"][dp])
            
    mu += "Properties:\n"
    atThreshold = 0 
    # .99999 (as using 'in between thresholds' is a bit of a kludge but ...) - can use in pass 2 reasoning for filter out edge edge
    thresholds = [1.0, 0.9999999999999, 0.99, 0.95, 0.9, 0.8, 0.5, 0.25, 0.1, 0.05]
    currentThresholdIndex = 0
    for j, prop in enumerate(sorted([key for key in typeData if not re.match(r'\_', key)], key=lambda x: typeData[x]["count"], reverse=True), 1):
    
        level = float(typeData[prop]["count"])/float(total)
        thresholdIndex = [i for i, t in enumerate(thresholds) if level <= t][-1] 
        if thresholdIndex != currentThresholdIndex:
            currentThresholdIndex = thresholdIndex
            mu += "\n\t------------- {}% cut off ------------------------\n".format(int(thresholds[thresholdIndex] * 100) if thresholdIndex > 1 else 100)
        propTypeMU = typeData[prop]["type"]
        
        propTimeSpanMU = ""
        if "firstCreateDate" in typeData[prop]:
            propTimeSpanMU = " - {} - ".format(typeData[prop]["firstCreateDate"].split("T")[0])
            firstYear = typeData[prop]["firstCreateDate"].split("-")[0]
            lastYear = typeData[prop]["lastCreateDate"].split("-")[0]
            if firstYear == lastYear:
                propTimeSpanMU += firstYear
            else:
                propTimeSpanMU += "{} --> {}".format(firstYear, lastYear)            
        
        mu += "\t{}. {} - {} - {:,} ({:.0%}){}{}\n".format(
            j, 
            prop, 
            propTypeMU, 
            typeData[prop]["count"], 
            float(typeData[prop]["count"])/float(total), 
            (" - " + ", ".join(typeData[prop]["rangeTypes"]) if "rangeTypes" in typeData[prop] else ""), 
            propTimeSpanMU
        )
        
        if "badLiteralValues" in typeData[prop]:
            mu += "\t\t** Bad Literal Values: {}\n".format(typeData[prop]["badLiteralValues"])
            
        # enum | pointer | date | list - order by key if int - otherwise by value
        if "byValueCount" in typeData[prop]:  
            for j, enumValue in enumerate(sorted(typeData[prop]["byValueCount"], key=lambda x: x if isinstance(x, int) else typeData[prop]["byValueCount"][x], reverse=True), 1):
                if j > DEFAULT_MAX_NOMINAL_VALUES:
                    mu += "\t\t... only showing top {} of {}\n".format(DEFAULT_MAX_NOMINAL_VALUES, len(typeData[prop]["byValueCount"]))
                    break
                mu += '\t\t{}. {} - {:,} ({:.1%})\n'.format(j, enumValue, typeData[prop]["byValueCount"][enumValue], float(typeData[prop]["byValueCount"][enumValue])/float(typeData[prop]["count"]))
        elif "rangeCount" in typeData[prop]: # big range pointer
            mu += "\t\tRange Count: {}\n".format(typeData[prop]["rangeCount"])
            
        if typeData[prop]["type"] == "LIST":
            FLIP_CANDIDATE_VARIETY = 50 # ie/ variability of size
            FLIP_CANDIDATE_SIZE = 10 # absolute size
            if "cstopped" in typeData[prop]: # only LIST
                mu += "\t\t**CSTOPed [FLIP CANDIDATE]: {:,} ({:.1%})\n".format(typeData[prop]["cstopped"], float(typeData[prop]["cstopped"])/float(typeData[prop]["count"]))
            elif len(typeData[prop]["byValueCount"]) > FLIP_CANDIDATE_VARIETY and sum(1 for listLen in typeData[prop]["byValueCount"] if int(listLen) > FLIP_CANDIDATE_SIZE):
                mu += "\t\t**FLIP CANDIDATE based on variety of lengths and size\n"
                
        if typeData[prop]["type"] == "DATE" and "byWeekDay" in typeData[prop]:
            wdMap = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            mu += '\t\t------------------------------------------\n'
            for i, wd in enumerate(sorted(typeData[prop]["byWeekDay"]), 1): # from 0 Monday
                mu += '\t\t{}. {} - {}\n'.format(i, wdMap[wd], reportAbsAndPercent(typeData[prop]["byWeekDay"][wd], typeData[prop]["count"]))
                
    mu += "\n\n"
    return mu


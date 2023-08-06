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

"""
Using data, defines a type according to the presence and (selectively) the frequency distribution of the values of properties. Optionally splits on the values of one or more nominal properties to distinguish finer 'subtypes'.

REM: VistA typing/files/collections n enums etc often too broad, too narrow or muddy.
(Sub)Typing pictures VistA but often needs better categorization/groupings, things
refined from reframing the data first and this utility does allow for that.
  
Arguments:
- subTypeProps: one or more properties used to subtype by. Note that
pointer label is used for pointer properties
- createDateProp: isolates the property that designates the creation date of a record
  ... may change to be 'recordDateProp' as for scheduling, making this the 
  start time of an appt and not the time an appt is created.
- maxNominalValues: for pointer or literals - by default won't be counted once
distinct value count exceeds this threshold. Ensures type reduction doesn't become
a large restatement of the records 
- countDateType: by default only counts dates by year but MONTH, WEEK, DAY are other options
- forceCountPointerTypes: these pointer values are counted even if they exceed the maxNominalValues threshold.
- forceCountProperties: applies to both POINTER and LITERAL (usually enums) properties. Usually just for enums but may be used for variable pointer pointers too
- deidentifyPointerTypes: remove label from these (PATIENT set by default)

Note that there is a default set of FORCE_COUNTED PTER TYPEs covering user (200),
locations and patient.
"""
DEFAULT_MAX_NOMINAL_VALUES = 60 # maxNominalValues=60 as 55 is # dialogs of 100
DEFAULT_FORCE_COUNT_PTER_TYPES = ["4", "44", "200"] # user, location, patient
USER_NAME_TYPES = ["220_5"]
DEFAULT_FORCE_COUNT_PTER_TYPES.extend(USER_NAME_TYPES)
PATIENT_NAME_TYPES = ["2", "9000001", "55", "63", "70", "631", "665", "690", "790", "38_1", "354_7"] # mainly dinumed, 2005 as its label has id info
DEFAULT_FORCE_COUNT_PTER_TYPES.extend(PATIENT_NAME_TYPES)

class SubTypeReducer():
    
    def __init__(self, typId, subTypeProps, createDateProp="", maxNominalValues=DEFAULT_MAX_NOMINAL_VALUES, countDateType="YEAR", forceCountPointerTypes=DEFAULT_FORCE_COUNT_PTER_TYPES, forceCountProperties=[], deidentifyPointerTypes=PATIENT_NAME_TYPES):
    
        self.__typId = typId
        self.__subTypeProps = subTypeProps
        self.__createDateProp = createDateProp
        self.__maxNominalValues = maxNominalValues
        self.__countDateType = countDateType
        self.__forceCountPointerTypes = set(forceCountPointerTypes)
        self.__forceCountProperties = set(forceCountProperties)
        self.__deidentifyPointerTypes = set(deidentifyPointerTypes)
        
        self.__typeReducers = {}
        # minimal for 'all' option as sub types have details
        self.__allTypeReducer = TypeReducer(
            self.__typId, 
            createDateProp=self.__createDateProp, 
            maxNominalValues=self.__maxNominalValues, 
            countDateType="YEAR", # no nuance - subtypes get nuance 
            forceCountPointerTypes=[], 
            forceCountProperties=[],
            deidentifyPointerTypes=self.__deidentifyPointerTypes
        ) 
                    
    def transform(self, resource):
        # for all
        self.__allTypeReducer.transform(resource)  
        
        # will create a (Sub)TypeReducer for any combos seen - REM: pointer label used
        pieces = ["-".join(self.__subTypeProps)]
        for stp in self.__subTypeProps:    
            if re.match(r'\#', stp): # allows presence/absence vs counting
                stpv = "*PRESENT*" if stp.split("#")[1] in resource else "*ABSENT*"
            elif stp not in resource:
                stpv = "**NOVALUE**"
            else:
                if isinstance(resource[stp], list):
                    stpv = "**HASMEMBERS**"
                elif isinstance(resource[stp], dict):
                    if "value" in resource[stp]: # will only split by year
                        stpv = resource[stp]["value"].split("-")[0]
                    elif "label" in resource[stp]:
                        # PY2 -> 3: removed .encode("ascii", "ignore") for label
                        stpv = "{} [{}]".format(resource[stp]["label"], resource[stp]["id"])
                    else: # should never happen
                        raise Exception("Expect structured value of sub type property {} to be a POINTER or DATE (Year)".format(stp))
                elif isinstance(resource[stp], bool):
                    stpv = str(resource[stp])
                elif len(resource[stp].split(":")) == 2: # enum (allows more complex : to stay)
                    stpv = resource[stp].split(":")[1]
                else:
                    stpv = resource[stp]
            pieces.append(re.sub(r' ', '_', stpv))
        subTypeId = ":".join(pieces)
        typeReducer = self.__lookupSubTypeReducer(subTypeId)
        typeReducer.transform(resource)
        
    def subTypeReducerCount(self):
        return len(self.__typeReducers)
        
    def reductions(self):
        results = []
        allReduction = self.__allTypeReducer.reduction()
        allReduction["_reductionEndDay"] = datetime.now().strftime("%Y-%m-%d")
        results.append(allReduction)
        allTotal = allReduction["_total"]
        for subTypeId in self.__typeReducers:
            reduction = self.__typeReducers[subTypeId].reduction()
            reduction["_subTypeId"] = subTypeId
            reduction["_numberFiltered"] = allTotal - reduction["_total"]
            results.append(reduction)
        return results
        
    def __lookupSubTypeReducer(self, subTypeId):
    
        if subTypeId not in self.__typeReducers:
            self.__typeReducers[subTypeId] = TypeReducer(
                self.__typId, 
                createDateProp=self.__createDateProp, 
                maxNominalValues=self.__maxNominalValues, 
                countDateType=self.__countDateType,
                forceCountPointerTypes=self.__forceCountPointerTypes, 
                forceCountProperties=self.__forceCountProperties, 
                deidentifyPointerTypes=self.__deidentifyPointerTypes
            )
            
        return self.__typeReducers[subTypeId]
                            
class TypeReducer():

    def __init__(self, typId, reductionLabel="", createDateProp="", maxNominalValues=DEFAULT_MAX_NOMINAL_VALUES, countDateType="YEAR", forceCountPointerTypes=DEFAULT_FORCE_COUNT_PTER_TYPES, forceCountProperties=[], deidentifyPointerTypes=PATIENT_NAME_TYPES):
        
        self.__typId = typId
        self.__createDateProp = createDateProp
        self.__maxNominalValues = maxNominalValues
        self.__countDateType = countDateType
        self.__forceCountPointerTypes = set(forceCountPointerTypes)
        self.__forceCountProperties = set(forceCountProperties)
        self.__deidentifyPointerTypes = set(deidentifyPointerTypes)

        self.__dontCountLiteralProp = set()
        self.__distinctPointerValuesByProp = defaultdict(lambda: set())
        self.__typeData = {"_total": 0, "_id": typId}
        if reductionLabel: # REM: filter can make a different subset
            self.__typeData["_reductionLabel"] = reductionLabel
        if createDateProp and not callable(createDateProp):
            self.__typeData["_createDateProp"] = createDateProp

    def transform(self, resource):
        self.__reduce(resource, self.__typeData)
        
    def subTypeReducerCount(self):
        return 0
        
    def reductions(self):
        return [self.__typeData]

    def reduction(self):
        return self.__typeData

    """
    Works for both contained resources and resources
    """
    def __reduce(self, resource, typeData, parentPropPath=""):

        def isPointer(value):
            if len(value) == 0:
                return False # shouldn't happen but some synthesized has {} value
            if len(set(value) - set(["id", "sameAs", "sameAsLabel", "label"])):
                return False
            return True
        
        def typeProp(value): # WHAT ABOUT BOOLEAN?
            if isinstance(value, bool):
                return "BOOLEAN"
            if isinstance(value, int):
                return "INTEGER"
            if isinstance(value, dict):
                if "value" in value:
                    return "DATE"
                elif isPointer(value):
                    return "POINTER"
                else: # assuming - and needn't have an 'id'
                    return "OBJECT"
            if isinstance(value, list):
                return "LIST" # TODO - simple list work ie/ not {"x": y ...} but [y ...]
            return "LITERAL"

        # allows for label based date value (ie/ pter to visit etc)
        def getCreateDate(resource, createDateProp):
            if not createDateProp:
                return None
            if callable(createDateProp):
                return createDateProp(resource)
            # Allow for real date and a pointer who's label is a date!
            if createDateProp not in resource:
                return None
            if not isinstance(resource[createDateProp], dict):
                return None
            if not ("value" in resource[createDateProp] or "label" in resource[createDateProp]):
                return None
            if "value" in resource[createDateProp]:
                dtValue = resource[createDateProp]["value"]
            elif "label" in resource[createDateProp]:
                dtValue = resource[createDateProp]["label"]
            if not validDayDT(dtValue.split("T")[0]): 
                return None
            return dtValue
    
        # at start, assume all literals are enums AND handle booleans here too
        def countByLiteralValue(qprop, propInfo, litValue): 
            if qprop in self.__dontCountLiteralProp:
                return
            # First exclusion: if long then a real literal and not just a value 
            # (NOTE: bool's fall in here too)
            if isinstance(litValue, str) and qprop not in self.__forceCountProperties and len(litValue.split(" ")) > 5:
                self.__dontCountLiteralProp.add(qprop)
                if "byValueCount" in propInfo:
                    del propInfo["byValueCount"]
                return
            if "byValueCount" not in propInfo:
                propInfo["byValueCount"] = { litValue: 1 }
                return
            if litValue not in propInfo["byValueCount"]:
                # second exclusion - too many but can force a pass 
                if qprop not in self.__forceCountProperties and len(propInfo["byValueCount"]) == self.__maxNominalValues:
                    self.__dontCountLiteralProp.add(qprop)
                    del propInfo["byValueCount"]
                    return 
                propInfo["byValueCount"][litValue] = 0
            propInfo["byValueCount"][litValue] +=1

        def countByPointerValue(qprop, propInfo, ptrValue):
            """
            Either 
            - count distinct values (if large number) OR
            - count by if:
              - small as acts as enum (ie/ <= enum threshold)
              - forced to count (usually for 200/2)
            - accounts for multiple prop and parent prop having same name by using
            qprop to track size
              
            TODO: 
            - distinct pointer values by prop could get big for self references of
            big types (2005 to 2005 etc). May need cut off there too
            - reconsider vptr with other overwhelming 200 or 4 etc (may never happen)
            """
            sptrValue = ptrValue
            if re.search(r'\[', ptrValue):
                sptrValue = re.search(r'\[([^\]]+)', ptrValue).group(1)
            MAX_RANGE_COUNT = 1000000 # for 2005 to 2005 etc.
            if qprop in self.__distinctPointerValuesByProp:
                if "rangeCount" in propInfo:
                    self.__distinctPointerValuesByProp[qprop].add(sptrValue)
                    if len(self.__distinctPointerValuesByProp[qprop]) == MAX_RANGE_COUNT:
                        logging.debug("Property {} has too big a range - >={:,} - so not even counting that".format(qprop, MAX_RANGE_COUNT))
                        del propInfo["rangeCount"]
                        self.__distinctPointerValuesByProp[qprop] == None
                    else: 
                        propInfo["rangeCount"] = len(self.__distinctPointerValuesByProp[qprop])
                return
            if "byValueCount" not in propInfo:
                propInfo["byValueCount"] = { ptrValue: 1 }
                return
            if ptrValue not in propInfo["byValueCount"]:
                ptrType = sptrValue.split("-")[0]
                """ 
                VPTRs present difficulties - if just a few of forced pointer then will
                fail to count em unless appear in first set
                
                TODO: may renew and simply record those forced - effected 442096
                """
                if not (qprop in self.__forceCountProperties or ptrType in self.__forceCountPointerTypes) and len(propInfo["byValueCount"]) == self.__maxNominalValues:
                    self.__distinctPointerValuesByProp[qprop] = set([
                        re.search(r'\[([^\]]+)', ptrValue).group(1) if re.search(r'\[', ptrValue) else ptrValue for ptrValue in propInfo["byValueCount"]])
                    propInfo["rangeCount"] = len(self.__distinctPointerValuesByProp[qprop])
                    del propInfo["byValueCount"]
                    logging.debug("Property {} is too big for byValueCount - just measure range".format(qprop))
                    return 
                propInfo["byValueCount"][ptrValue] = 0
            propInfo["byValueCount"][ptrValue] +=1
            
        # as opposed to reduction of all sresources, this establishes number per parent
        def countListValueByLength(propInfo, listValue):
            if "byValueCount" not in propInfo:
                propInfo["byValueCount"] = {}
            if len(listValue) in propInfo["byValueCount"]:
                propInfo["byValueCount"][len(listValue)] += 1
                return
            propInfo["byValueCount"][len(listValue)] = 1

        """
        Compromise that gives data for graphing, trending
        time including weekday/weekend splits and per day
        creation graphs but which doesn't collect too much 
        for types with many dates.
        """
        def countDateValue(prop, propInfo, dtValue):
            dayValue = dtValue.split("T")[0]
            dayDT = validDayDT(dayValue)
            if not dayDT:
                return
            dtps = dayValue.split("-")
            monthValue = "{}-{}".format(dtps[0], dtps[1])
            # Not doing WEEK as WEEK in what year?
            #     dtToCount = dayDT.isocalendar()[1]                
            if self.__countDateType == "MONTH":
                dtToCount = monthValue
            elif self.__countDateType == "DAY":
                # May downstep all but createProp no matter what
                # if self.__createDateProp != prop:
                #    dtToCount = monthValue
                # else:
                dtToCount = dayValue
            else: # "YEAR" is default
                dtToCount = dtps[0]            
            if "byValueCount" not in propInfo:
                propInfo["byValueCount"] = Counter()
            propInfo["byValueCount"][dtToCount] += 1
            if self.__createDateProp != prop: # only weekday for this
                return
            try:
                propInfo["byWeekDay"]
            except:
                propInfo["byWeekDay"] = Counter()
            propInfo["byWeekDay"][dayDT.weekday()] += 1     
                        
        typeData["_total"] += 1
        
        if "_firstIEN" not in typeData and len(set(resource).intersection(["_id", "id"])):
            idProp = "id" if "id" in resource else "_id"
            self.__typeData["_firstIEN"] = resource[idProp].split("-")[1]
                    
        # only applies to LIST props - full ones filled in below
        if "fmqlStopped" in resource:
            for propStopped in resource["fmqlStopped"]:
                if propStopped not in typeData:
                    typeData[propStopped] = { "count": 0, "type": "LIST"}
                typeData[propStopped]["count"] += 1
                if "cstopped" not in typeData[propStopped]:
                    typeData[propStopped]["cstopped"] = 1
                else:
                    typeData[propStopped]["cstopped"] += 1
                    
        createDate = getCreateDate(resource, self.__createDateProp)
        dateValues = []
        for prop in [key for key in resource if key not in ["id", "_id", "type", "label", "ien", "fmqlStopped"]]: 

            value = resource[prop] 

            if prop not in typeData:
                typeData[prop] = { "count": 0, "type": typeProp(value) }
            info = typeData[prop]
            info["count"] += 1

            if createDate: # add per property including for create property itself
                if "firstCreateDate" in info:
                    if info["firstCreateDate"] > createDate:
                        info["firstCreateDate"] = createDate
                    if info["lastCreateDate"] < createDate:
                        info["lastCreateDate"] = createDate
                else:
                    info["firstCreateDate"] = createDate
                    info["lastCreateDate"] = createDate
            
            qprop = prop if parentPropPath == "" else parentPropPath + "/" + prop
                
            # If info type not same as value type:
            # - [TODO] neither LITERAL
            # - info type is not LITERAL - skip and record bad literal
            # - info type is LITERAL - reset info with bad literal
            typ = typeProp(value)
            if typ != info["type"]:
                if info["type"] != "LITERAL":
                    if "badLiteralValues" not in info:
                        info["badLiteralValues"] = 0
                    info["badLiteralValues"] += 1
                    continue
                info = { "count": 1, "type": typ, "badLiteralValues": info["count"] }
                typeData[prop] = info
                
            if typeData[prop]["type"] in ["LITERAL", "BOOLEAN", "INTEGER"]:
                countByLiteralValue(qprop, typeData[prop], value)
                continue
                
            if typeData[prop]["type"] == "POINTER":
                if "rangeTypes" not in typeData[prop]:
                    typeData[prop]["rangeTypes"] = [] # Allow variable ptr
                rangeType = value["id"].split("-")[0]
                if rangeType not in typeData[prop]["rangeTypes"]:
                    typeData[prop]["rangeTypes"].append(rangeType)
                ptrType = value["id"].split("-")[0]
                if "label" in value and ptrType not in self.__deidentifyPointerTypes:
                    ptrValue = '{} [{}]'.format(value["label"], value["id"])
                else:
                    ptrValue = value["id"]
                countByPointerValue(qprop, typeData[prop], ptrValue)
                continue
                
            if typeData[prop]["type"] == "LIST":
                countListValueByLength(typeData[prop], value)
                if "reduction" not in typeData[prop]:
                    typeData[prop]["reduction"] = {"_total": 0}
                spropPath = prop if parentPropPath == "" else parentPropPath + "/" + prop
                for sresource in resource[prop]:
                    self.__reduce(sresource, typeData[prop]["reduction"], spropPath)
                continue
                
            if typeData[prop]["type"] == "DATE":
                countDateValue(prop, typeData[prop], value["value"])
                dateValues.append((prop, value["value"]))

        # Post 1: first and last date values seen
        if len(dateValues) > 1: # capture which date property is first/last. Can vary. (effects Orders etc)
            if "_firstDateProps" not in typeData:
                typeData["_firstDateProps"] = {}
                typeData["_lastDateProps"] = {}
            dateValues = sorted(dateValues, key=lambda x: x[1])
            if dateValues[0][0] not in typeData["_firstDateProps"]:
                typeData["_firstDateProps"][dateValues[0][0]] = 0 
            typeData["_firstDateProps"][dateValues[0][0]] += 1
            if dateValues[-1][0] not in typeData["_lastDateProps"]:
                typeData["_lastDateProps"][dateValues[-1][0]] = 0
            typeData["_lastDateProps"][dateValues[-1][0]] += 1
            
# ISO‑8601 form allow fast lexical comparison - datetime comparison is orders
# of magnitude slower. This isn't an exact day validity checker but its good
# enough - split on lex is faster than regexp '(20|19)\d\d-[01]\d-[0-3]\d$
def validDayDT(dayValue, minYear=1980, maxYear=2030):
    try:
        dayDT = datetime.strptime(dayValue, "%Y-%m-%d")
    except:
        return None
    yr = int(dayValue.split("-")[0])
    if yr > maxYear or yr < minYear:
        return None
    return dayDT

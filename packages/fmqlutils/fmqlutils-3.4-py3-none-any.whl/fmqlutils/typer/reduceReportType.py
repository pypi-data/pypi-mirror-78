#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import sys
import re
import json
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

from ..cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, BASE_LOCN_TEMPL, DATA_LOCN_TEMPL, DATARF_LOCN_TEMPL, metaOfVistA
from .reduceType import TypeReducer, SubTypeReducer, DEFAULT_FORCE_COUNT_PTER_TYPES, validDayDT
from .reportReductions import reportReductions
from .DEFAULT_TYPE_CONFIGS import TYPE_CONFIGS

TYPER_LOCN_TEMPL = BASE_LOCN_TEMPL + "Typer/"
TYPER_REDUCTIONS_LOCN_TEMPL = TYPER_LOCN_TEMPL + "Reductions/"
TYPER_REDUCTIONS_REPORTS_LOCN_TEMPL = TYPER_LOCN_TEMPL + "ReductionsReports/"
TYPER_REPORTS_LOCN_TEMPL = TYPER_LOCN_TEMPL + "Reports/"

"""
As command, fmqltyper

> fmqltyper {SNO} {TYP} {PERIODBACK From Cut} [overrideConfig file name]

So ex

> fmqltyper 442 2 YR1 myconfigFor2

where the override config is optional and there to allow typing evolve beyond
the per type settings in DEFAULT_TYPE_CONFIGS with ex/
{
        "subTypeProps": ["status ...
        "createDate": "... different create date"
etc.
}

Key items:
- onAndAfterDay/upToDay rely on create property and if set, want a "reductionLabel" to differentiate them. In the typical case, Period leads to settings for these.
- replyEfficiency (create property used to cut down reply walking) won't apply to flipped (RF) types (ex/ 44_003) or where create is not resource create (ex/ 409_84)
- 'countDateType' [YEAR|MONTH|WEEK|DAY] which decides the granularity of a date
counting. Usually its YEAR but shorter periods like DAY90 etc use DAY. This allows per
day activity tracking from type reductions.

TODO:
- try yaml config https://pyyaml.org/wiki/PyYAMLDocumentation as can embed code 
easily ie/ include custom filters/enhancers inline so no need for custom ie/ can't
now invoke dynamically in command line
"""
def reduceReportType(
    stationNumber, 
    typ, 
    period="ALL", 
    overrideConfig=None, 
    reductionLabelExplicit="", 
    customEnhancer=None
    ):
        
    # ###################### Make Configuration from sources ##########
        
    meta = metaOfVistA(stationNumber) # for cut date and annotations

    # Config is made to allow a loaded configuration to override all defaults
    config = {}
    
    if reductionLabelExplicit:
        config["reductionLabel"] = reductionLabelExplicit
    elif period != "ALL":
        config["reductionLabel"] = period
                    
    config["forceRedo"] = True
    
    """
    Map YR\d, DAY\d, MTH\d to date range, reductionLabel and default count date type
    """
    def enhanceConfigFromPeriod(config, vistaCutDate, period):

        if period == "ALL":
            config["countDateType"] = "YEAR"
            return
        
        vistaCutDay = vistaCutDate.split("T")[0]
        config["upToDay"] = vistaCutDay
    
        vistaCutDayDT = datetime.strptime(vistaCutDay, "%Y-%m-%d")
        lastDayDT = vistaCutDayDT - relativedelta(days=1)
        lastDay = datetime.strftime(lastDayDT, "%Y-%m-%d")
        
        relDelta = None
        for mtchRE, keyword, defaultCountDateType in [
            (r'YR(\d+)', "years", "YEAR"),
            (r'MTH(\d+)', "months", "MONTH"),
            (r'WK(\d+)', "weeks", "DAY"),
            (r'DAY(\d+)', "days", "DAY")
        ]:
            mtch = re.match(mtchRE, period)
            if not mtch:
                continue
            args = { keyword: int(mtch.group(1)) }
            relDelta = relativedelta(**args)
            onAndAfterDayDT = vistaCutDayDT - relDelta
            config["onAndAfterDay"] = datetime.strftime(onAndAfterDayDT, "%Y-%m-%d")
            config["countDateType"] = defaultCountDateType
            break
    
    # in config to allow overrides
    enhanceConfigFromPeriod(config, meta["cutDate"], period)

    if typ in TYPE_CONFIGS:
        config.update(TYPE_CONFIGS[typ])
    
    if overrideConfig: # as override allowed, must QA below
        config.update(overrideConfig) 
        
    config["dataLocnTempl"] = DATA_LOCN_TEMPL if not ("isRF" in config and config["isRF"]) else DATARF_LOCN_TEMPL
    if "replyWalkEfficiencyOff" not in config:
        config["replyWalkEfficiencyOff"] = True if "isRF" in config and config["isRF"] else False 
        
    # ####################### QA Settings ###############################
    # ... mainly needed for bugs in overrideConfig
        
    if "onAndAfterDay" in config:
        if not validDayDT(config["onAndAfterDay"]):
            raise Exception("Invalid 'on and after day': {}".format(config["onAndAfterDay"]))

    if "upToDay" in config:
        if not validDayDT(config["upToDay"]):
            raise Exception("Invalid 'up to day': {}".format(config["upToDay"]))
            
    if ("upToDay" in config or "onAndAfterDay" in config):
        if "reductionLabel" not in config:
            raise Exception("You must name the reduction ('reductionLabel') for time limited ('onAndAfterDay'/'upToDay') reductions")
        if "createDate" not in config:
            raise Exception("You must identify a 'create property' for time limited ('onAndAfterDay'/'upToDay') reductions")
            
    if "countDateType" in config and config["countDateType"] not in ["YEAR", "MONTH", "WEEK", "DAY"]:
        raise Exception("'countDateType' must be YEAR | MONTH | WEEK | DAY")
            
    # ################### Setup Env and See if Necessary ####################
                
    start = datetime.now()
    
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)    
    ch = logging.StreamHandler(sys.stdout)
    format = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(format)
    log.addHandler(ch)
        
    # Used to ensure 
    def ensureLocation(locn):
        if not os.path.isdir(locn):
            os.mkdir(locn)
        return locn
    ensureLocation(TYPER_LOCN_TEMPL.format(stationNumber))
    reductionLocn = ensureLocation(TYPER_REDUCTIONS_LOCN_TEMPL.format(stationNumber))
    reportLocn = ensureLocation(TYPER_REPORTS_LOCN_TEMPL.format(stationNumber))        

    dataLocn = config["dataLocnTempl"].format(stationNumber)  
    redFFL = "{}/{}{}Reduction.json".format(reductionLocn, typ, config.get("reductionLabel", ""))
        
    if config["forceRedo"] == False and os.path.isfile(redFFL):
        logging.info("Not reducing (and reporting) {} as already exists and NOT forceredo".format(typ))
        return
        
    # ###################### Walk the Type and Reduce ####################
        
    if "reductionLabel" not in config:
        logging.info("About to reduce (and report) on {}, starting at {} [PID {}]".format(typ, start, os.getpid()))
    else:
        logging.info("About to reduce (and report) on {}, starting at {} [PID {}] - {} for onAndAfterDay {}, upToDay {}".format(typ, start, os.getpid(), config["reductionLabel"], config.get("onAndAfterDay", "-"), config.get("upToDay", "-"))) 
    
    fcpts = DEFAULT_FORCE_COUNT_PTER_TYPES
    if "forceCountPointerTypesExtra" in config:
        fcpts.extend(config["forceCountPointerTypesExtra"])
    if "subTypeProps" in config:
        logging.info("Subtyping by '{}'".format("-".join(config["subTypeProps"])))
        rtr = SubTypeReducer(
            typ, 
            createDateProp=config.get("createDate", ""), 
            subTypeProps=config["subTypeProps"], 
            forceCountPointerTypes=fcpts, 
            forceCountProperties=config.get("forceCountProperties", []), 
            countDateType=config.get("countDateType", "YEAR")
        )
    else:
        rtr = TypeReducer(
            typ, 
            createDateProp=config.get("createDate", ""), 
            forceCountPointerTypes=fcpts, 
            forceCountProperties=config.get("forceCountProperties", []), 
            countDateType=config.get("countDateType", "YEAR")
        )
        
    startAtReply = ""
    efficientWalked = False
    if "onAndAfterDay" in config:
        if config["replyWalkEfficiencyOff"]:
            logging.debug("No Start Efficiency: starting with first Reply and ignoring onAndAfterDay for skipping as either [1] walking reformed (RF) data which is usually from out of order multiples or [2] forced to walk all as property for onAndAfterDay is not create property (one in IEN order) ex/ appt start time or [3] no create date spec'ed")
        else:
            store = FMQLReplyStore(dataLocn)
            startAtReply = store.firstReplyFileOnOrAfterCreateDay(typ, config["createDate"], config["onAndAfterDay"])
            if startAtReply == "":
                logging.info("** Exiting: can't find Reply to start at on and after day {}, create property {}".format(onAndAfterDay, typesAndDates[typ]))
                return
            logging.debug("Start Efficiency: configuring Iterator for on and after time: on or after day {}, create property {}, starting at reply {}".format(config["onAndAfterDay"], config["createDate"], startAtReply))
            efficientWalked = True
    resourceIter = FilteredResultIterator(dataLocn, typ, startAtReply=startAtReply)
                                
    def getCreateDay(resource, createDateProp):
        value = resource[createDateProp]["value"] if "value" in resource[createDateProp] else resource[createDateProp]["label"]
        dayValue = value.split("T")[0] # using lex comp on ISO‑8601 form as fastest
        if not validDayDT(dayValue):
            log.debug("Can't get create day as its date has invalid value: {}".format(dayValue))
            return None
        return dayValue  
        
    msgThres = 50000 
    upToDayStopped = False
    count = 0 
    filtered = Counter()  
    for i, resource in enumerate(resourceIter, 1):
        count += 1
        filteredSoFar = sum(filtered[c] for c in filtered)
        if i % msgThres == 0:
                logging.debug("Checked {} more resources for total of {:,}, sub type reducers {:,}, so far filtered {:,}, now in reply {} - {}".format(msgThres, i, rtr.subTypeReducerCount(), filteredSoFar, resourceIter.currentReplyFile(), datetime.now() - start))
        idProp = "id" if "id" in resource else "_id"
        if customEnhancer:
            resource = customEnhancer.enhance(resource)
            if not resource:
                filtered["CUSTOM"] += 1
                continue
        # Allows for out of order too
        if "onAndAfterDay" in config or "upToDay" in config:
            if config["createDate"] not in resource:
                filtered["NOCREATEDATE"] += 1
                continue
            createDay = getCreateDay(resource, config["createDate"])
            if not createDay:
                filtered["BADCREATEDATE"] += 1
                continue
            if "onAndAfterDay" in config and createDay < config["onAndAfterDay"]:
                filtered["LTONAFTER"] += 1
                continue
            if "upToDay" in config and createDay >= config["upToDay"]:
                filtered["GTEUPTO"] += 1
                continue 
        rtr.transform(resource)
            
    pattData = rtr.reductions()
    # Add more meta to ALL Reduction
    allReds = [typeData for typeData in pattData if "_subTypeId" not in typeData]
    if len(allReds) != 1:
        raise Exception("Internal Error - expected one and only one ALL reduction")
    allRed = allReds[0]
    allRed["_stationNumber"] = stationNumber
    allRed["_vistaName"] = meta.get("name", "UNKNOWN")
    allRed["_vistaCut"] = meta["cutDate"]
    if efficientWalked:
        allRed["_efficientWalked"] = True
    allRed["_label"] = config.get("reductionLabel", "ALL")
    if "onAndAfterDay" in config:
        allRed["_onAndAfterDay"] = config["onAndAfterDay"]
    if "upToDay" in config:
        allRed["_upToDay"] = config["upToDay"]
                            
    json.dump(pattData, open(redFFL, "w")) 
     
    reportLocn = ensureLocation(TYPER_REPORTS_LOCN_TEMPL.format(stationNumber))
    reportReductions(pattData, "{}/{}{}Report.txt".format(reportLocn, typ, config.get("reductionLabel", "")))
        
    if len(filtered):
        filteredMU = "/".join(["{} [{}]".format(reason, filtered[reason]) for reason in filtered])
        logging.info("Finished after {:,} resources of {} in {} at {}, {:,} explicitly filtered with {}".format(count, typ, datetime.now() - start, datetime.now(), sum(filtered[c] for c in filtered), filteredMU))
    else:
        logging.info("Finished after {:,} resources of {} in {} at {}".format(count, typ, datetime.now() - start, datetime.now()))
        
# ############################# Driver ####################################

def main():

    assert sys.version_info >= (3, 4)
    
    try:
        stationNumber = sys.argv[1]
        typ = sys.argv[2]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO TYP [PERIOD] [OVERRIDE CONFIG]")
    
    if not re.match(r'\d{3}$', stationNumber):
        raise SystemExit("Need three digit station number")
        
    if len(sys.argv) == 4:
        period = "ALL"
    else:
        period = sys.argv[3]
        if not re.match(r'(ALL|YR|MTH|WK|DAY)', period):
            raise SystemExit("Invalid period {}".format(period))
        
    # For this specific type - can override all but SNO and typ itself
    overrideConfig = None
    if len(sys.argv) == 5:
        overrideConfigName = sys.argv[4].split(".")[0] 
        if not os.path.isfile("{}.json".format(overrideConfigName)):
            raise SystemExit("No override config file {}.json - exiting".format(overrideConfigName))
        overrideConfig = json.load(open("{}.json".format(overrideConfigName)))
    
    reduceReportType(stationNumber, typ, period, overrideConfig=overrideConfig)
        
if __name__ == "__main__":
    main()
    

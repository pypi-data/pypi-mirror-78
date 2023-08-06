#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from fmqlutils.cacher.cacherUtils import recacheForCSTOPs
from fmqlutils.cacher.cacher import makeFMQLIF

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
        
    configLogging(config["stationNumber"], "cacherLog", config["logLevel"] if "logLevel" in config else "INFO")
                
    if not re.match(r'[\d\_]+$', arg2):
        raise SystemExit("Expect a type id as the second argument but got {}".format(arg2))

    typ = arg2
        
    try:
        fmqlIF = makeFMQLIF(config)
        recacheForCSTOPs(config["stationNumber"], typ, fmqlIF)
    except Exception as e:
        raise SystemExit("Can't recache stopped data: {}".format(str(e)))

if __name__ == "__main__":
    main()


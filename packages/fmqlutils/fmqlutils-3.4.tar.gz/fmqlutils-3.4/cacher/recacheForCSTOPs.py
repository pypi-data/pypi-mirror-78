#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2019-2020 caregraf

import sys
import os
import json
from fmqlutils.cacher.cacher import makeFMQLIF
from fmqlutils.cacher.cacherUtils import configLogging, recacheForCSTOPs

def main():

    assert sys.version_info >= (3, 4)
    
    try:
        sysConfigName = sys.argv[1].split(".")[0]
        typ = sys.argv[2]
    except IndexError:
        raise SystemExit("Usage _EXE_ {SYSTEM CONFIG FILE} {typ}")
    
    if not os.path.isfile("{}.json".format(sysConfigName)):
        raise SystemExit("No system config file {}.json - exiting".format(sysConfigName))
    try:
        config = json.load(open("{}.json".format(sysConfigName)))
    except:
        raise SystemExit("Invalid system config {}.json - can't parse".format(sysConfigName))

    configLogging(config["stationNumber"], "cacherLog", config["logLevel"] if "logLevel" in config else "INFO")

    try:
        recacheForCSTOPs(config["stationNumber"], typ, makeFMQLIF(config))
    except:
        raise SystemExit("Can't recache")

if __name__ == "__main__":
    main()

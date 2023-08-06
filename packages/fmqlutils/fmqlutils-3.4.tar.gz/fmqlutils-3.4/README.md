# fmqlutils

Utilities for caching, transforming (reframe & reduce) and reporting on data extracted from FileMan systems using FMQL. There are also "bonus" utilities for using the VistA RPC interface.

Published to _https://pypi.org/project/fmqlutils/_

## Details of Station-based Data/Schema/Report Locations

From fmqlutils.cacher.cacherUtils

  * DATAV1_LOCN_TEMPL
  * DATA_LOCN_TEMPL
  * SCHEMA_LOCN_TEMPL
  * TMPWORKING_LOCN_TEMPL

From fmqlutils.typer.reduceReportTypes

  * DATAREDUCTION_LOCN_TEMPL
  * TYPEREDUCE_LOCN_TEMPL
  * REPORTS_LOCN_TEMPL
  * TYPEREPORT_LOCN_TEMPL

The locations appear under VISTA_DATA_BASE_DIR. _station numbers_ appear under this ...

  /data/vista/{stationNumber}/...

The default VISTA_DATA_BASE_DIR is /data/vista/ but it can be reset using an environment variable, _FMQL_VISTA_DATA_BASE_DIR_.
Alternatively, you can _ln -s_ the default location to the actual location you want to use.

Note that the base location must exist and must be writable or an import of fmqlutils will yield ...

> Exception: fmqlutils module and submodules can't work - VISTA_DATA_BASE_DIR "/data/vistafmqlutilstest/" doesn't exist. Either _ln -s_ a real location to this directory OR set the environment variable "FMQL_VISTA_DATA_BASE_DIR" to the desired location


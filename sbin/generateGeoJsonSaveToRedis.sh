#! /bin/bash

SBIN_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
TAXIINFO_DIR="$(dirname "$SBIN_DIR")"

cd $TAXIINFO_DIR
python demo/libs/dataprocessing/queryMySQLSaveGeoJsonInRedisByHour.py


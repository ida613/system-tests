#!/bin/bash

set -eu

BINARIES_DIR=$1 #/binaries

current_dir=$(pwd)
cd $BINARIES_DIR

if [ -e "dd-trace-rb" ]; then
    echo "Install from local folder ${BINARIES_DIR}/dd-trace-rb"
fi

cd $current_dir

#!/bin/bash

DOCKNAME=hsm2

# ==========================================================
# ==========================================================
# Change this to change the default port on which the 
# simulator runs
PORT=9999

while getopts ":p:" opt; do
    case "$opt" in
    p)
        PORT=$OPTARG 
        ;;
    esac
done
# ==========================================================
# ==========================================================

if [[ "$@" != "--help" ]]; then
    echo "=============================================================================="
    echo "IMPORTANT NOTE:"
    echo "=============================================================================="
    echo "Simulator will run on 0.0.0.0:$PORT. Use '-p' to change this (e.g., '-p 1234')"
    echo "Parameter '-b' will have no effect in the dockerized version"
    echo "Change the '$0' script to change the default port"
    echo "=============================================================================="

    SIM_ARGS="-b 0.0.0.0 -p $PORT"
fi

docker images|grep -q $DOCKNAME && BQUIET=-q

docker build --platform linux/x86_64 -t $DOCKNAME $BQUIET .

docker run --platform linux/x86_64 -ti --rm -p $PORT:$PORT -v "`pwd`:/hsm2" -w "/hsm2" -u "`id -u`:`id -g`" $DOCKNAME ./sim $@ $SIM_ARGS

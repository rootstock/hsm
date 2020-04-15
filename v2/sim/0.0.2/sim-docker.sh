#!/bin/bash

DOCKNAME=hsm2

# ==========================================================
# ==========================================================
# Change this to change the port on which the simulator runs
PORT=9999
# ==========================================================
# ==========================================================

if [[ "$@" != "--help" ]]; then
    echo "IMPORTANT NOTE:"
    echo "==============="
    echo "Simulator will run on 0.0.0.0:$PORT. Parameters '-p' and '-b' will have no effect in the dockerized version."
    echo "Change the '$0' script to change the port"

    SIM_ARGS="-b 0.0.0.0 -p $PORT"
fi

docker images|grep -q $DOCKNAME && BQUIET=-q

docker build -t $DOCKNAME $BQUIET .

docker run -ti --rm -p $PORT:9999 $DOCKNAME ./sim $@ $SIM_ARGS

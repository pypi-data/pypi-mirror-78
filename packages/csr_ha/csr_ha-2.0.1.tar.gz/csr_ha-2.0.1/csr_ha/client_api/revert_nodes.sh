#!/bin/sh

# Set up the path to python scripts
source ~/.bashrc

# Call the python script to revert all nodes
if [[ "$(python3 -V)" == *"Python 3"* ]]; then
    export PYTHON=$(which python3)
    export SITE=$($PYTHON -m site --user-site)
    if [[ ! -d "$SITE" ]]; then
        export PYTHON=$(which python)
        export SITE=$($PYTHON -m site --user-site)
    fi
else
    export PYTHON=$(which python)
    export SITE=$($PYTHON -m site --user-site)
fi

$PYTHON $SITE/csr_ha/client_api/node_event.py -i all -e revert

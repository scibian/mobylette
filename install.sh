#!/bin/bash

MOBYLETTE_HOME=`pwd`
export PATH=$MOBYLETTE_HOME/bin:$PATH
export PYTHONPATH=$MOBYLETTE_HOME:$PYTHONPATH

# Creates mobylette.conf
CONF_FILE=mobylette.conf
CONF_PATH=`eval echo ~$USER`/.mobylette

if [ -d "$CONF_PATH" ]; then
    read -p "$CONF_PATH already exists. Overwrite (y/n)? " ANSWER

    if [ "$ANSWER" = "n" ]; then
        echo "mobylette ready"
        return
    fi

    if [ "$ANSWER" = "y" ]; then

        rm -r $CONF_PATH
        mkdir $CONF_PATH

        echo "[CLUSTER]"                       > $CONF_PATH/$CONF_FILE
        echo "log_path=$MOBYLETTE_HOME/"      >> $CONF_PATH/$CONF_FILE
        echo "name=phoenix"                   >> $CONF_PATH/$CONF_FILE
        echo "nodes="                         >> $CONF_PATH/$CONF_FILE
        echo "patterns=dataset"               >> $CONF_PATH/$CONF_FILE
        echo "prefix=sample"                  >> $CONF_PATH/$CONF_FILE

        echo "mobylette ready"
        return
    fi
fi

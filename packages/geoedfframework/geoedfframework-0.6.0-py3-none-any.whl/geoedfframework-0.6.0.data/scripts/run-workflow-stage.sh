#!/bin/bash

#arguments:
#workflow_fname: workflow filepath
#workflow_stage: stage to be executed; encoded as : separated list (for connectors)
#plugin_type: type of plugin to be executed; helps with validation of inputs
#target_path: either path where outputs are to be stored or filepath for filter outputs

#### the next three arguments need to be specified; use explicit 'none' in case no value
#var_bindings: JSON string containing one set of variable bindings (only for connectors)
#stage_bindings: JSON string containing one set of bindings for stage references
#overridden_args: comma separated list of args that need to be overridden
####

#optional list of file paths to input files corresponding to overridden_args

#simple validation on the minimum number of arguments required
#this script is invoked for both connectors and processors
#further validation needs to be performed in the respective scripts
if [ "$#" -lt 6 ]; then
   echo "At least six arguments need to be provided"
   exit 1
fi

# if this is a connector plugin
if [ "$3" == "Input" ] || [ "$3" == "Filter" ]; then
    python3 /usr/local/bin/run-connector-plugin.py "$@"
else # processor
    python3 /usr/local/bin/run-processor-plugin.py "$@"
fi

#!/bin/sh

# Shell wrapper function that will prompt for and save your JIRA password in environment variable.
#
# Options:
#     -p  force prompt, even when the password environment variable is already set

function jbranch {
    if [[ -z ${JBRANCH_PATH} ]]; then
        echo "Error: JBRANCH_PATH not specified"
        return 1
    fi
    if [[ -z ${JBRANCH_JIRA_PASSWORD} ]] || [[ "$1" == "-p" ]]; then
        read -s -p "JIRA Password: " JBRANCH_JIRA_PASSWORD
        echo
        export JBRANCH_JIRA_PASSWORD
    fi
    if [[ "$1" == "-p" ]]; then
        python "$JBRANCH_PATH/jbranch.py" $2
    else
        python "$JBRANCH_PATH/jbranch.py" $1
    fi
}

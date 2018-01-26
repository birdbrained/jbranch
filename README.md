# jbranch

Create local git branches based on a JIRA issue

Latest version: **0.1.0**
see [CHANGELOG.md](CHANGELOG.md) for changes from previous versions

## Description

This script will query a JIRA server for the given issue key and create a git branch based on the issue type, key, and summary in the form of:

`issuetype/ISSUE-1_issue_summary`

Also included is an optional shell wrapper function that will prompt for your JIRA password and export it to an environment variable so you don't have to enter it every time within the same shell session.

## Installation

`pip install -r requirements.txt`

### Shell wrapper function installation

In your .profile (or equivalent):

`export JBRANCH_PATH="/path/to/jbranch`
`source "$JBRANCH_PATH/jbranch.sh"`

## Usage

`python jbranch.py ISSUE-1`

### With shell wrapper function

`jbranch ISSUE-1`

Force re-prompt for password:

`jbranch -p ISSUE-1`

## Options

There are a number of environment variables that can be set to control how jbranch functions.

`JBRANCH_JIRA_URL` - the full url to the JIRA server

- example: `JBRANCH_JIRA_URL="https://my_jira.atlassian.net"`

`JBRANCH_JIRA_USERNAME` - the JIRA username with which to authenticate

- example: `JBRANCH_JIRA_USERNAME="me@mydomain.net"`

`JBRANCH_JIRA_PASSWORD` - the JIRA password with which to authenticate

- example: `JBRANCH_JIRA_PASSWORD="mysupersecret"`

  Please use common sense and don't set this in your .profile

`JBRANCH_TRANSITION` - an optional JIRA transition to trigger on the issue

- example: `JBRANCH_TRANSITION="Start Progress"`

`JBRANCH_NO_COLOR` - don't use colors in output

- example: `JBRANCH_NO_COLOR=1`

`JBRANCH_LC_SUMMARY` - lowercase the JIRA issue summary in the branch name

- example: `JBRANCH_LC_SUMMARY=1`

`JBRANCH_LC_FIRST` - lowercase only the first letter of the JIRA issue summary in the branch name

- example: `JBRANCH_LC_FIRST=1`

`JBRANCH_NO_SWITCH` - don't switch to the branch after it is created

- example: `JBRANCH_NO_SWITCH=1`

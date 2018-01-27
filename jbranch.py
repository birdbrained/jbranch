#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
import subprocess
import sys
from colorama import Fore, Style
from getpass import getpass
from jira import JIRA, JIRAError
from prompt_toolkit.shortcuts import prompt


def bold(text):
    if os.environ.get('JBRANCH_NO_COLOR'):
        return text
    return Style.BRIGHT + text + Style.NORMAL


def action(message):
    sys.stdout.write(message + ' ... ')
    sys.stdout.flush()


def success(message='✓'):
    if os.environ.get('JBRANCH_NO_COLOR'):
        print message
    else:
        print Fore.GREEN + message + Style.RESET_ALL


def error(message):
    if os.environ.get('JBRANCH_NO_COLOR'):
        print 'Error: ' + message
    else:
        print Fore.RED + 'Error: ' + message + Style.RESET_ALL
    sys.exit()


if len(sys.argv) < 2:
    error('must provide a JIRA issue key')

key = sys.argv[1]

if os.environ.get('JBRANCH_JIRA_URL'):
    url = os.environ.get('JBRANCH_JIRA_URL')
else:
    url = raw_input('JIRA URL: ')

if os.environ.get('JBRANCH_JIRA_USERNAME'):
    username = os.environ.get('JBRANCH_JIRA_USERNAME')
else:
    username = raw_input('JIRA Username: ')

if os.environ.get('JBRANCH_JIRA_PASSWORD'):
    password = os.environ.get('JBRANCH_JIRA_PASSWORD')
else:
    password = getpass('JIRA Password: ')

action('Authenticating to {0} as {1}'.format(bold(url), bold(username)))

try:
    jira = JIRA(server=url, basic_auth=(username, password), max_retries=0)
except requests.exceptions.MissingSchema:
    error('JIRA URL ' + bold(url) + ' is invalid')
except requests.exceptions.ConnectionError:
    error('could not connect to JIRA Server at ' + bold(url))
except JIRAError as e:
    error(requests.status_codes._codes[e.status_code][0])
else:
    success()

action('Getting info for ' + bold(key))

try:
    issue = jira.issue(key)
except JIRAError as e:
    error(e.text)
else:
    success()

if not issue.fields.issuetype.name:
    error('could not get issue type')

if not issue.fields.summary:
    error('could not get summary')

branch_type = issue.fields.issuetype.name.lower()

if os.environ.get('JBRANCH_LC_SUMMARY'):
    summary = issue.fields.summary.lower()
elif os.environ.get('JBRANCH_LC_FIRST'):
    summary = issue.fields.summary[:1].lower() + issue.fields.summary[1:]
else:
    summary = issue.fields.summary

branch = '{0}/{1}_{2}'.format(branch_type, key, summary)
branch = re.sub(r'\s+', '_', branch)
branch = re.sub(r'[^\w\-\/]', '', branch)

if os.environ.get('JBRANCH_ALLOW_EDIT'):
    branch = prompt(u'Branch name: ', default=branch.decode('utf-8'))

action('Creating branch ' + bold(branch))

try:
    if os.environ.get('JBRANCH_NO_SWITCH'):
        subprocess.check_output(
            ['git', 'branch',  branch],
            stderr=subprocess.STDOUT
        )
    else:
        subprocess.check_output(
            ['git', 'checkout', '-b',  branch],
            stderr=subprocess.STDOUT
        )
except OSError as e:
    error(e)
except subprocess.CalledProcessError as e:
    error(e.output.rstrip())
else:
    success()

transition = os.environ.get('JBRANCH_TRANSITION')
if transition:
    action('Triggering transition: ' + bold(transition))
    transition_id = jira.find_transitionid_by_name(issue, transition)
    if transition_id is None:
        error(
            'the transition {0} is not available for this issue'.format(
                bold(transition)
            )
        )
    try:
        jira.transition_issue(issue, transition_id)
    except JIRAError as jira_error:
        error(jira_error.text)
    else:
        success()

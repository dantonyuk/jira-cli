from jira import jira_client
from utils import content_from_editor

import tempfile, os, re
from subprocess import call


_initial = """
# Provide work log description here if needed.
# All the lines followed by empty line define issue description.
"""

def parser(build):
    parser = build('worklog', help='Add a worklog to an issue')
    parser.add_argument('issue', help='Parent issue')
    parser.add_argument('time', help='Log time')
    parser.add_argument('--comment', '-c', default=None, help='Worklog comment')
    parser.add_argument('--skip-comment', '-s', action='store_true', help='Do not ask for comment')
    return parser


def execute(issue, time, comment, skip_comment, *args, **kwargs):
    client = jira_client()

    if comment is None and not skip_comment:
        comment = content_from_editor('edit worklog comment', _initial)

    client.issue(issue).worklog(time, comment)

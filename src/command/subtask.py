from jira import jira_client
from config import rest_config
from utils import content_from_editor, open_in_browser

import tempfile, os, re
from subprocess import call


_initial = """Summary: 

# Line starting with 'Summary:' defines the summary of the issue
# All the lines followed by empty line define issue description.
"""

def parser(build):
    parser = build('subtask', help='Add a subtask to an issue')
    parser.add_argument('issue', help='Parent issue')
    parser.add_argument('-o', '--open', action='store_true', help='Open subtask after adding')
    return parser


def execute(issue, open, *args, **kwargs):
    client = jira_client()

    details = content_from_editor("edit subtask", _initial)
    lines = list(filter(lambda l: not l.startswith('#'), details.split(os.linesep)))
    fields = {}
    description = []
    is_description = False
    for line in lines:
        if is_description:
            description.append(line)
        else:
            if line == "":
                is_description = True
            else:
                splitted = re.compile(": ?").split(line, 1)
                if len(splitted) != 2:
                    print(f"Warning: cannot split {line}")
                else:
                    fields[splitted[0]] = splitted[1]

    if not fields.get('Summary', '').strip():
        print("There is no summary specified.")
        exit(0)

    description = os.linesep.join(description)
    if not description.strip():
        print("There is no description specified.")
        exit(0)

    json = client.issue(issue).subtask(fields['Summary'], description)

    if open:
        url = rest_config()['url']
        link = f'{url}browse/{json.key.value}'
        open_in_browser(link)
    else:
        print(f"To open this subtask in a browser run: jira open {json.key.value}")

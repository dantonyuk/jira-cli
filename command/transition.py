from jira import jira_client


_transition_ids = {
    "todo": "11",
    "inprogress": "21",
    "inqa": "71",
    "inuat": "81",
    "done": "101",
}

_resolution_names = {
    "fixed": "Fixed",
    "wontfix": "Won't Fix",
    "duplicate": "Duplicate",
    "incomplete": "Incomplete",
    "cannotreproduce": "Cannot Reproduce",
    "completed": "Completed",
    "done": "Done",
    "wontdo": "Won't Do",
    "dataissue": "Data Issue",
    "knownissue": "Known Issue",
}

def parser(build):
    parser = build('transition', aliases=['trans', 'move'], help='Do an issue transition')
    parser.add_argument('issue')
    parser.add_argument('status')
    parser.add_argument('-r', '--resolution', default='')
    parser.add_argument('-c', '--comment', default='')
    return parser


def execute(issue, status, resolution, comment, *args, **kwargs):
    client = jira_client()

    if not _transition_ids.get(status):
        print(f"There is no such transition: {status}.")
        print("Available transitions are: " + ", ".join(_transition_ids.keys()))
        exit(1)

    client.issue(issue).transit(_transition_ids[status],
            resolution=resolution and _resolution_names[resolution], comment=comment)

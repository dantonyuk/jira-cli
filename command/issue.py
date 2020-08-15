from jira import jira_client


def parser(build):
    parser = build('issue', aliases=['show'], help='Show issue information')
    parser.add_argument('issue')
    return parser


def execute(issue, *args, **kwargs):
    client = jira_client()
    issue_object = client.issue(issue)
    print("Summary: ", issue_object.fields.summary)
    print("Assignee: ", issue_object.fields.assignee.displayName)
    print("Priority: ", issue_object.fields.priority.name)
    print("Status: ", issue_object.fields.status.name)
    print("Description: \n", issue_object.fields.description)

from jira import jira_client


def parser(build):
    parser = build('subtasks', help='Search for issue subtasks')
    parser.add_argument('parent', help='parent issue')
    return parser


def execute(parent, *args, **kwargs):
    issues = jira_client().search('parent=' + parent)
    for issue in issues:
        print("{: <10}{: <12}{}".format(
            issue.key, 
            issue.fields.status.name, 
            issue.fields.summary))

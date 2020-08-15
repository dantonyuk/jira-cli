from jira import jira_client


def parser(build):
    parser = build('search', help='Search for issues')
    parser.add_argument('query')
    return parser

def execute(query, *args, **kwargs):
    issues = jira_client().search(query)

    for issue in issues:
        print("{: <10}{: <10}{: <10}{: <14}{}".format(
            issue.key, 
            issue.fields.priority.name, 
            issue.fields.customfield_11061[0], 
            issue.fields.status.name, 
            issue.fields.summary))

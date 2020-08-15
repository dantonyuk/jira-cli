from jira import jira_client


def parser(build):
    parser = build('done', help='Done an issue')
    parser.add_argument('issue')
    parser.add_argument('-c', '--comment', default='')
    return parser


def execute(issue, comment, *args, **kwargs):
    client = jira_client()
    client.issue(issue).transit(101, resolution="Done", comment=comment)

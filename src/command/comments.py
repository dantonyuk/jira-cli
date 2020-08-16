from jira import jira_client


def parser(build):
    parser = build('comments', help='Search for issue comments')
    parser.add_argument('issue')
    return parser


def execute(issue, *args, **kwargs):
    client = jira_client()
    json = client.rest.get('issue/' + issue + '/comment').result
    for comment in json['comments']:
        print("\n{} {}\n{}".format(
            comment.created,
            comment.author.name,
            comment.body))

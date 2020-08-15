from utils import *


def parser(build):
    parser = build('comments', help='Search for issue comments')
    parser.add_argument('issue')
    return parser


def execute(issue, *args, **kwargs):
    config = read_config()
    client = JiraClient(config)
    json = client.get('issue/' + issue + '/comment')
    for comment in json['comments']:
        print("\n{} {}\n{}".format(
            comment.created, 
            comment.author.name, 
            comment.body))

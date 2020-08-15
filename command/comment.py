from config import rest_config
from jira import jira_client
from utils import content_from_editor, open_in_browser


_initial = """
# Put comment in this file.
# Lines starting with # will be ignored.
"""

def parser(build):
    parser = build('comment', help='Add comment to the issue')
    parser.add_argument('issue')
    parser.add_argument('-c', '--comment', default=None, help='Comment to be added')
    parser.add_argument('-o', '--open', type=bool, default=False, help='Open comment after adding')
    return parser


def execute(issue, comment, open, *args, **kwargs):
    client = jira_client()
    comment = comment or content_from_editor('edit comment', _initial)
    if not comment or not comment.strip():
        print('Comment is not defined.')
        exit(1)

    new_comment = client.issue(issue).comment(comment)

    if open:
        url = rest_config()['url']
        id = new_comment.id.value
        permalink = f"{url}browse/{issue}?focusedCommentId={id}&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-{id}"
        open_in_browser(permalink)

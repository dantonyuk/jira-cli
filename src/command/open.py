from urllib.parse import urljoin

from config import rest_config
from utils import open_in_browser


def parser(build):
    parser = build('open', help='Open issue in the browser')
    parser.add_argument('issue')
    return parser


def execute(issue, *args, **kwargs):
    open_in_browser(urljoin(rest_config()['url'], f'browse/{issue}'))

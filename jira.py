import requests
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import urljoin

from config import read_config, rest_config
from rest import RestClient
from propdict import PropDict


def jira_client():
    read_config()
    return JiraClient(rest_config())


class JiraClient(object):
    def __init__(self, config):
        url = urljoin(config['url'], '/rest/api/latest/')
        auth = (config['username'], config['password'])
        self.rest = RestClient(url, auth)

    def search(self, jql):
        response = self.rest.get('search', params={'jql': jql})
        return JiraIssues(self.rest, response.result.issues)

    def issue(self, key):
        return JiraIssue(self.rest, self.rest.get(f'issue/{key}').result)


class JiraList(object):
    def __init__(self, client, values):
        self.client = client
        self.values = values

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __len__(self):
        return len(self.items)

    def add(self, value):
        not_implemented()


class JiraIssues(JiraList):
    def __init__(self, client, issues):
        super(JiraIssues, self).__init__(client, issues)


class JiraIssue(object):
    def __init__(self, client, issue):
        self.client = client
        self.issue = issue

    def comments(self):
        resp = self.client.get(f'issue/{self.issue.key}/comment')
        return JiraComments(resp.result.comments)

    def comment(self, body):
        return self.client.post(f'issue/{self.issue.key}/comment', json={'body': body}).result

    def subtask(self, summary, description):
        subtask = {
            'fields': {
                'project': {
                    'id': self.fields.project.id.value
                },
                'issuetype': {
                    'name': 'Sub-task'
                },
                'parent': {
                    'key': self.issue.key.value
                },
                'assignee': {
                    'name': rest_config()['username']
                },
                'summary': summary,
                'description': description,
            }
        }

        return self.client.post('issue', json=subtask).result

    def worklog(self, spentTime, comment):
        if not comment or not comment.strip():
            comment = ''

        worklog = {
            "author": { "name": rest_config()['username'] },
            "comment": comment,
            "timeSpent": spentTime,
        }
        
        return self.client.post(f'issue/{self.issue.key}/worklog', json=worklog).result

    def transit(self, transition_id, resolution=None, comment=None):
        transition = {
            'transition': {
                'id': transition_id
            },
            'fields': {},
            'update': {},
        }

        if resolution:
            transition['fields']['resolution'] = { 'name': resolution }
        if comment:
            transition['update']['comment'] = [{ 'add': { 'body': comment }}]

        return self.client.post(f'issue/{self.issue.key}/transitions', json=transition)

    fields = property(lambda self: self.issue.fields)


class JiraComments(JiraList):
    def __init__(self, client, comments):
        super(JiraComments, self).__init__(client, comments)

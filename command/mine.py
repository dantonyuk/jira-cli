from jira import jira_client


def parser(build):
    return build('mine', help='Search for my issues')


def execute(*args, **kwargs):
    issues = jira_client().search('assignee=currentUser() and resolution=Unresolved and type!=Sub-task order by updated')

    for issue in issues:
        print("{: <10}{: <10}{: <10}{: <14}{}".format(
            issue.key, 
            issue.fields.priority.name, 
            issue.fields.customfield_11061[0], 
            issue.fields.status.name, 
            issue.fields.summary))

from .UserAgent import UserAgent

import pprint

class CmdIssue:
    def __init__(self, config_obj):
        self.issue_endpoint = config_obj.base_url + '/issues'
        self.pp = pprint.PrettyPrinter(indent=4)
        self.ua = UserAgent()

    def view(self, issue_id):
        # view the detail of a chosen pull request
        endpoint = self.issue_endpoint + '/' + str(issue_id)

        issue = self.ua.get(endpoint)

        print("Title: {}".format(issue['title']))
        print("ID: {}".format(issue['id']))
        print("Assigned to {}".format(issue['assignee']))
        print("Summary:\n\t{}".format(issue['content']['raw']))
        return 1

    def create(self, details={}):
        data = {
            "title": details['title'],
            "content": {
                "raw": details['content']
            }
        }

        new_issue = self.ua.post(self.issue_endpoint, data)
        print("New issue (ID={}) is created ({})".format(new_issue['id'], new_issue['links']['self']['href']))

        return 1

    def status(self, issue_id):
        endpoint = self.issue_endpoint + '/' + str(issue_id)

        issue = self.ua.get(endpoint)

        print("Title: {}".format(issue['title']))
        print("Status: {}, Type: {}, Priority: {}".format(issue['state'], issue['kind'], issue['priority']))
        return 1

    def close(self, issue_id, status="closed"):
        endpoint = self.issue_endpoint + '/' + str(issue_id) + '/changes'
        data = {
            "changes": {
                "state": { "new": status }
            }
        }
        self.ua.post(endpoint, data)
        print("Issue (ID={}) is {}".format(str(issue_id), status))
        return 1

    def list(self, id):
        # list all issue
        issues = self.ua.get(self.issue_endpoint)

        for issue in issues['values']:
            if issue['state'] == 'closed':
                continue
            print("Title: {}".format(issue['title']))
            print("ID: {}".format(issue['id']))
            print("Assigned to {}".format(issue['assignee']))
            print("Summary:\n\t{}\n".format(issue['content']['raw']))
        return 1

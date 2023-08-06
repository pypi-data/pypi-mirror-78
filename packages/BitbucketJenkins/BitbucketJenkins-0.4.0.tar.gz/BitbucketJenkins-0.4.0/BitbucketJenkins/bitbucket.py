#! /usr/bin/env python

import json
import requests
from .client import Client
from .error import error

class Bitbucket:
    def __init__(self, base_url, username, password):
        self.client = Client(base_url, username, password)
        self.client.session.headers.update({'Content-Type': 'application/json'})
        self.project = Project(self.client)
        self.branchRestriction = BranchRestriction(self.client)
        self.permission = Permission(self.client)
        self.defaultReviewer = DefaultReviewer(self.client)
        self.admin = Admin(self.client)
    
class Project:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/api/1.0/projects/"

    @error
    def get(self, project_key):
        """
        Retrieve the project matching the supplied key
        """
        return self.client.get(self.resource_path + project_key)

    @error
    def create(self, project_key, project_name, description):
        """
        Create a project in bitbucket server
        """
        data = json.dumps(dict(key=project_key, name=project_name, description=description))
        return self.client.post(self.resource_path, data)

class BranchRestriction:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/branch-permissions/2.0/projects/{}/restrictions"
        self.data = []
        self.branch_types = ["fast-forward-only", "no-deletes", "pull-request-only"]
    
    @error
    def get(self, project_key):
        """
        Retrieve branch restriction by key
        """
        return self.client.get(self.resource_path.format(project_key))
    
    @error
    def create(self, project_key, branches):
        """
        Create branch restriction to a project
        """
        self.index = 0
        for i in range(0, len(branches)):
            for branch_type in self.branch_types:
                self.data.append({})
                self.data[self.index]['type'] = branch_type
                self.data[self.index]['matcher'] = {}
                self.data[self.index]['matcher']['id'] = branches[i]
                self.data[self.index]['matcher']['displayId'] = branches[i]
                self.data[self.index]['matcher']['type'] = {}
                self.data[self.index]['matcher']['type']['id'] = "BRANCH"
                self.data[self.index]['matcher']['type']['name'] = "Branch"
                self.data[self.index]['matcher']['active'] = True
                self.data[self.index]['users'] = []
                self.data[self.index]['groups'] = []
                self.data[self.index]['accessKeys'] = []
                self.index += 1
        data = json.dumps(self.data)
        return self.client.post(self.resource_path.format(project_key.upper()), data, headers={'Content-Type':'application/vnd.atl.bitbucket.bulk+json'})

class Permission:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/api/1.0/projects/{}/permissions/{}/all?allow=true"

    @error
    def create(self, project_key, permission):
        """
        Create/grant default permission to a bitbucket project.
        Permissions are :
        - PROJECT_READ
        - PROJECT_WRITE
        - PROJECT_ADMIN
        """
        return self.client.post(self.resource_path.format(project_key, permission))

class DefaultReviewer:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/default-reviewers/1.0/projects/{}/condition"
        self.data = {}

    @error
    def get(self, project_key):
        """
        Retrieve default reviewer matchin the supplied key
        """
        return self.client.get(self.resource_path.format(project_key) + 's')
    
    def getUserID(self, username):
        """
        Retrieve user ID
        """
        user_path = "/rest/api/1.0/users/{}"
        try :
            data = self.client.get(user_path.format(username))
            user_id = json.loads(data.text)['id']
            return user_id
        except ValueError:
            print("username not found")

    @error
    def create(self, project_key, users, branch):
        """
        Create default reviewer in project
        """
        self.data['reviewers'] = []
        for i in range(0, len(users)) : 
            user_id = self.getUserID(users[i])
            self.data['reviewers'].append({})
            self.data['reviewers'][i]['id'] = user_id
        self.data['sourceMatcher'] = {}
        self.data['sourceMatcher']['active'] = True
        self.data['sourceMatcher']['id'] = "ANY_REF_MATCHER_ID"
        self.data['sourceMatcher']['displayId'] = "ANY_REF_MATCHER_ID"
        self.data['sourceMatcher']['type'] = {}
        self.data['sourceMatcher']['type']['id'] = "ANY_REF"
        self.data['sourceMatcher']['type']['name'] = "Any branch"
        self.data['targetMatcher'] = {}
        self.data['targetMatcher']['active'] = True
        self.data['targetMatcher']['id'] = branch
        self.data['targetMatcher']['displayId'] = branch
        self.data['targetMatcher']['type'] = {}
        self.data['targetMatcher']['type']['id'] = "BRANCH"
        self.data['targetMatcher']['type']['name'] = "Branch"
        self.data['requiredApprovals'] = 1
        data = json.dumps(self.data)
        return self.client.post(self.resource_path.format(project_key), data)

class Admin:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/api/1.0/projects/{}/permissions/users?name={}&permission=PROJECT_ADMIN"

    @error
    def create(self, project_key, username):
        """
        Create an admin user for a project
        """
        return self.client.put(self.resource_path.format(project_key, username))



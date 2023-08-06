import datetime
import pandas as pd
import os
import numpy as np
import requests
import base64
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from dotenv import load_dotenv
import boto3
from ast import literal_eval
load_dotenv()

class clockify():
    def __init__(self):
        self.base_url = os.environ['CLOCKIFY_BASE_URL']
        self.workspace_id = os.environ['CLOCKIFY_WORKSPACE_ID']
        self.headers = {'X-Api-key':os.environ['CLOCKIFY_API_KEY'],'content-type':'application/json'}
        self.yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.start = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=10),'%Y-%m-%d')
        self.end = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=3),'%Y-%m-%d')
        self.s3 = boto3.resource('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
                            )

    def build_user_dictionary(self):
        results = requests.get(self.base_url + 'workspaces/' + str(self.workspace_id) + '/users',headers=self.headers)
        users = []
        for user in results.json():
            users.append({'name':user['name'],'id':user['id']})
        for index_i,user in enumerate(users):
            params = {'start':self.start + 'T00:00:00.000Z','end':self.end + 'T23:59:59.999Z'}
            results = requests.get(self.base_url + 'workspaces/' + str(self.workspace_id) + '/user/' + user['id'] + '/time-entries',params=params,headers=self.headers).json()
            projects = []
            project_ids = {}
            for project in results:
                if project['projectId'] in project_ids:
                    pass
                else:
                    project_ids[project['projectId']] = project['projectId']
            for project in project_ids:
                if type(project) != type(None):
                    project_info = {}
                    project_info['id'] = project
                    projects.append(project_info)
            users[index_i]['projects'] = projects
        for user in users:
            for index_i,project in enumerate(user['projects']):
                project_info = requests.get(self.base_url + 'workspaces/' + str(self.workspace_id) + '/projects/' + project['id'],headers=self.headers).json()
                project['name'] = project_info['name']
                tasks_info = requests.get(self.base_url + 'workspaces/' + str(self.workspace_id) + '/projects/' + project['id'] + '/tasks',params=params,headers=self.headers).json()
                task_macro = []
                for task in tasks_info:
                    task_micro = {}
                    task_micro['id'] = task['id']
                    task_micro['name'] = task['name']
                    task_macro.append(task_micro)
                project['tasks'] = task_macro
        return self.s3.Object(os.environ['AWS_BUCKET'], os.environ['AWS_CLOCKIFY_USERS_FILENAME']).put(Body=json.dumps(users))

    def get_time_entries_from_user_dictionary(self):
        obj = self.s3.Object(os.environ['AWS_BUCKET'], os.environ['AWS_CLOCKIFY_USERS_FILENAME'])
        body = obj.get()['Body'].read()
        users = literal_eval(body.decode('utf8'))
        time_entry_macro = []
        for user in users:
            params = {'start':self.start + 'T00:00:00.000Z','end':self.end + 'T23:59:59.999Z'}
            time_entries = requests.get(self.base_url + 'workspaces/' + str(self.workspace_id) + '/user/' + user['id'] + '/time-entries',params=params,headers=self.headers).json()
            for time_entry in time_entries:
                project_id = time_entry['projectId']
                task_id = time_entry['taskId']
                start = datetime.datetime.strptime(time_entry['timeInterval']['start'],'%Y-%m-%dT%H:%M:%SZ')
                end = datetime.datetime.strptime(time_entry['timeInterval']['end'],'%Y-%m-%dT%H:%M:%SZ')
                for project in user['projects']:
                    if project['id'] == project_id:
                        time_entry_micro = {}
                        time_entry_micro['name'] = user['name']
                        time_entry_micro['project'] = project['name']
                        time_entry_micro['start'] = start
                        time_entry_micro['end'] = end
                        time_entry_micro['duration'] = int(end.timestamp() - start.timestamp())
                        time_entry_micro['date'] = start.date()
                        for task in project['tasks']:
                            if task['id'] == task_id:
                                time_entry_micro['task'] = task['name']
                            else:
                                time_entry_micro['task'] = None
                        time_entry_macro.append(time_entry_micro.copy())
        creds_path = os.environ['BIGQUERY_CREDS_PATH']
        bq = bigQuery(os.environ['BIGQUERY_DATASET'],'clockify',creds_path)
        request_error = bq.main(time_entry_macro)
        return time_entry_macro

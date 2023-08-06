from google.oauth2 import service_account #Service Account
import pandas_gbq #Pandas GBQ.
from google.cloud import bigquery #To connect to BigQuery.
import os
import boto3
from ast import literal_eval
import pandas as pd
import datetime

class BigQuery():
    '''
    In order use the BigQuery class in your project you will complete the following:
        1. Install the package to your project by running the following:
            a. In Visual Studio console:
                i. pipenv install fp-utils
            b. In Google Colab
                i. !pip install fp-utils
        2. Import the package to your python file / colab project by placing the following
        at the top of your code:
            a. import fp_utils
    '''

    def df_from_big_query(self, query, project, creds_path):
        '''
        In order to use the this function in the BigQuery class you will complete the following:
            1. Create a new instance of the BigQuery class in your project by adding the following to your code:
                a. bq = fp_utils.BigQuery()
            2. Call the df_to_big_query function from the class by adding the following to your code with the
            proper settings for your purposes as populated by the fields described in the next section:
                a. bq.df_from_big_query(query, project, creds_path)

        [ * - Required fields ]

        *query (str): SQL query
        *project (str): Then name of the Big Query project
        *creds_path (str): Path to service account json file (_eg. 'creds/google_creds.json'_)

        returns: Pandas dataframe with query data.
        '''

        #Authenticate
        credentials = service_account.Credentials.from_service_account_file(creds_path)
        pandas_gbq.context.credentials = credentials

        #Read in dataframe.
        dataframe = pandas_gbq.read_gbq(
            query,
            project_id=project,
            dialect='standard')

        return dataframe

    def df_to_big_query(self, dataframe, project, dataset, table, **kwargs):
        '''
        In order to use the this function in the BigQuery class you will complete the following:
            1. Create a new instance of the BigQuery class in your project by adding the following to your code:
                a. bq = fp_utils.BigQuery()
            2. Call the df_to_big_query function from the class by adding the following to your code with the
            proper settings for your purposes as populated by the fields described in the next section:
                a. bq.df_to_big_query(dataframe, project, dataset, table, creds_path=creds_path, creds_from_service_account_info=False, remove_duplicates=True, replace_table=False)

        [ * - Required fields ]

        *dataframe (pandas dataframe): The data that you want uploaded to Big Query.
            Notes:
                1. Make sure the dtypes for each column of the dataframe matches the
                variable type for the table in BigQuery.
                    a. datetime objects will show dtype "object"
                2. Make sure the column names in the dataframe match the column names
                in BigQuery exactly.

        *project (str): The name of the Big Query project.
            Notes:
                1. This can be found on the BigQuery console on the left right below
                the search bar that says "Search for your tables and datasets" and to
                left of the pin icon.

        *dataset (str): The name of the Big Query dataset.
            Notes:
                1. This can be found on the BigQuery console underneath the project dropdown
                indented one tab space in from the project.

        *table (str): The name of the Big Query table.
            Notes:
                1. This can be found on the BigQuery console underneath the dataset dropdown
                indented one tab space in from the dataset.

        creds_path=(str): Path to the service account json file (_eg. 'creds/google_creds.json'_)
            Notes:
                1. The bigquery client can either authenticate directly with a service
                account file hosted in the project or the service account info hosted in a file
                elsewhere. When you are running scripts locally, you will likely use a
                service account file. If you are going to push your code to Heroku then,
                for security purposes, you will want to use the creds_from_service_account_info
                option described below.

        creds_from_service_account_info=(bool): If true, credentials will be acquired through amazon s3 bucket
            Notes:
                1. This option will require the environment variables listed below to be
                populated in Heroku:
                    a. ['AWS_BUCKET']
                        i. This is the name of the Amazon S3 bucket that you have created
                        for hosting the service account file
                    b. ['AWS_SECRET_ACCESS_KEY']
                        i. This is the secret access key that can be found from the
                        authorization info on the Amazon S3 bucket you created
                    c. ['AWS_ACCESS_KEY_ID']
                        i. This is the secret access key id that can be found from the
                        authorization info on the Amazon S3 bucket you created
                    d. ['AWS_GOOGLE_APPLICATION_CREDENTIALS_FILE']
                        i. This is the name of the service account credentials file that
                        is hosted on the Amazon S3 bucket

        remove_duplicates=(bool): If true, request will only submit unique values
            Notes:
                1. This will tell the code to read the target Heroku table and compare
                the version to be uploaded with the current version and remove any
                exact match duplicates where all the column values are the exact same.

        replace_table=(bool): If true, request will erase all values from table and build new table
            Notes:
                1. BigQuery is not capable of updating individual row values. This
                makes accurately updating the database difficult if pre-existing row values
                have changed and need to be modified. If pre-existing row values change, you
                will need to delete the entire table and replace all it with an up-to-date table.
                Marking this argument as True will perfrom the deletion of the old table and the
                insertion of the new table.

        '''

        remove_duplicates, creds_from_service_account_info, database_action = BigQuery.__check_df_to_big_query_kwargs(self,kwargs)

        if creds_from_service_account_info:
            service_account_json = BigQuery.__get_credentials_from_s3(self)
            credentials = service_account.Credentials.from_service_account_info(service_account_json)
            client = bigquery.client.Client(project,credentials=credentials)
        else:
            credentials = service_account.Credentials.from_service_account_file(kwargs['creds_path'])
            client = bigquery.client.Client(project,credentials=credentials)

        dataset_table = f'{dataset}.{table}'
        if database_action != "replace":
            query = (f'SELECT * FROM `{dataset_table}`')
            query_job = client.query(query)
            bq_data = query_job.result()
            tschemas = bq_data.schema
            schema = [{'name':tschema.name, 'type':tschema.field_type} for tschema in tschemas]
            bq_array = [row.values() for row in bq_data]
            bq_columns = [column['name'] for column in schema]
            bigquery_dataframe = pd.DataFrame(bq_array,columns=bq_columns)  
            if database_action == 'append' and remove_duplicates == True:
                bigquery_dataframe = bigquery_dataframe.append(bigquery_dataframe)
                dataframe = dataframe.append(bigquery_dataframe)
                dataframe = dataframe.drop_duplicates(keep=False)
        else:
            schema = None
        pandas_gbq.context.credentials = credentials
        dataframe.to_gbq(project_id=project,destination_table=dataset_table,credentials=credentials,if_exists=database_action,table_schema=schema)

        return 'Success'


    # --------------------------------- Private BigQuery Class Functions ---------------------------------
    # ----------------------------------------------------------------------------------------------------


    def __get_credentials_from_s3(self):
        s3 = boto3.resource('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
                            )
        obj = s3.Object(os.environ['AWS_BUCKET'],os.environ['AWS_GOOGLE_APPLICATION_CREDENTIALS_FILE'])
        body = obj.get()['Body'].read()
        service_account_json = literal_eval(body.decode('utf8'))
        return service_account_json

    def __check_df_to_big_query_kwargs(self,kwargs):
        if 'creds_path' not in kwargs.keys() and 'creds_from_service_account_info' not in kwargs.keys():
            raise ArgumentError('Must either pass in argument creds_path with valid path to service account file or argument creds_from_service_account_info=True')
        if 'remove_duplicates' in kwargs.keys():
            if kwargs['remove_duplicates']:
                remove_duplicates = True
            else:
                remove_duplicates = False
        else:
            remove_duplicates = False
        if 'creds_from_service_account_info' in kwargs.keys():
            if kwargs['creds_from_service_account_info']:
                creds_from_service_account_info = True
            else:
                creds_from_service_account_info = False
        else:
            creds_from_service_account_info = False
        if 'replace_table' in kwargs.keys():
            if kwargs['replace_table']:
                database_action='replace'
            else:
                database_action='append'
        else:
            database_action='append'

        return remove_duplicates, creds_from_service_account_info, database_action

class ArgumentError(Exception):
    pass

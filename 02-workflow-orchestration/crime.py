# !usr/bin/local
"""
Author: Daniel Egbo
Year: 2025
Description: A script to query and read Chicago Crime dataset from Google Bigquery 
public dataset and return a pandas dataframe. The data is available from year 2001 - 2024.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

from google.cloud import bigquery
import pandas
import pandas as pd


def _set_env(var: str):
    # Load environment variables from the .env file
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)

    # Retrieve the value of the environment variable
    value = os.getenv(var)
    # print(value)
    return value


# print("Client creating using default project: {}".format(client.project))

# credentials = service_account.Credentials.from_service_account_file('/home/daniel/.ssh/.gc/gcp.json')

project_id = _set_env('PROJECT_ID')
gcp_cred = _set_env('GCP_CREDENTIALS')
# client = bigquery.Client(credentials= gcp_cred, project=project_id)

client = bigquery.Client(location="US", project=project_id)

query_job = client.query("""
    SELECT *
    FROM bigquery-public-data.chicago_crime.crime
    WHERE year=2012
    LIMIT 500 """)

df = query_job.to_dataframe() # Wait for the job to complete.
df.drop(columns=['location'], inplace=True)
df.date = pd.to_datetime(df.date)
df.updated_on = pd.to_datetime(df.updated_on)
print(df.head())
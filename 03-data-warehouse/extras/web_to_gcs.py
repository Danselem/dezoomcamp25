import io
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage

def _set_env(var: str):
    # Load environment variables from the .env file
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)

    # Retrieve the value of the environment variable
    # os.getenv(var)
    # print(value)
    

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

_set_env('PROJECT_ID')
_set_env('GCP_CREDENTIALS')
_set_env('BUCKET_NAME')

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("BUCKET_NAME",)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dezoomcamp-447712-02e79e96f81c.json"


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


# Define PyArrow schema directly for 'yellow', 'green', and 'fhv' services
yellow_schema = pa.schema([
    ('VendorID', pa.float64()),
    ('passenger_count', pa.float64()),
    ('trip_distance', pa.float64()),
    ('RatecodeID', pa.float64()),
    ('store_and_fwd_flag', pa.string()),
    ('PULocationID', pa.int64()),
    ('DOLocationID', pa.int64()),
    ('payment_type', pa.float64()),
    ('fare_amount', pa.float64()),
    ('extra', pa.float64()),
    ('mta_tax', pa.float64()),
    ('tip_amount', pa.float64()),
    ('tolls_amount', pa.float64()),
    ('improvement_surcharge', pa.float64()),
    ('total_amount', pa.float64()),
    ('congestion_surcharge', pa.float64()),
    ('tpep_pickup_datetime', pa.timestamp('ns')),
    ('tpep_dropoff_datetime', pa.timestamp('ns'))
])

green_schema = pa.schema([
    ('VendorID', pa.float64()),
    ('store_and_fwd_flag', pa.string()),
    ('RatecodeID', pa.float64()),
    ('PULocationID', pa.int64()),
    ('DOLocationID', pa.int64()),
    ('passenger_count', pa.float64()),
    ('trip_distance', pa.float64()),
    ('fare_amount', pa.float64()),
    ('extra', pa.float64()),
    ('mta_tax', pa.float64()),
    ('tip_amount', pa.float64()),
    ('tolls_amount', pa.float64()),
    ('ehail_fee', pa.float64()),
    ('improvement_surcharge', pa.float64()),
    ('total_amount', pa.float64()),
    ('payment_type', pa.float64()),
    ('trip_type', pa.float64()),
    ('congestion_surcharge', pa.float64()),
    ('lpep_pickup_datetime', pa.timestamp('ns')),
    ('lpep_dropoff_datetime', pa.timestamp('ns'))
])

fhv_schema = pa.schema([
    ('dispatching_base_num', pa.string()),
    ('PUlocationID', pa.float64()),
    ('DOlocationID', pa.float64()),
    ('SR_Flag', pa.float64()),
    ('Affiliated_base_number', pa.string()),
    ('pickup_datetime', pa.timestamp('ns')),
    ('dropOff_datetime', pa.timestamp('ns'))
])

# Choose schema based on service type
def get_service_schema(service):
    if service == 'yellow':
        return yellow_schema
    elif service == 'green':
        return green_schema
    elif service == 'fhv':
        return fhv_schema
    else:
        raise ValueError(f"Unknown service: {service}")

def web_to_gcs(year, service):
    # Choose schema based on the service
    schema = get_service_schema(service)

    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # read it back into a dataframe
        df = pd.read_csv(file_name, compression='gzip')

        # Convert datetime columns to pandas datetime format
        datetime_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 
                            'lpep_pickup_datetime', 'lpep_dropoff_datetime', 
                            'pickup_datetime', 'dropOff_datetime']
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Apply the schema (convert df to pyarrow Table)
        table = pa.Table.from_pandas(df, schema=schema)

        # Convert to Parquet
        file_name = file_name.replace('.csv.gz', '.parquet')
        pq.write_table(table, file_name)
        print(f"Parquet: {file_name}")

        # upload it to GCS 
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS: {service}/{file_name}")

        # delete file locally
        print(f'file: {file_name} removed successfully.', 
              os.system(f"rm {file_name}"),
              os.system(f"rm {file_name.split('.parquet')[0]+'.csv.gz'}"))


# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
web_to_gcs('2019', 'yellow')
web_to_gcs('2020', 'yellow')
web_to_gcs('2019', 'fhv')

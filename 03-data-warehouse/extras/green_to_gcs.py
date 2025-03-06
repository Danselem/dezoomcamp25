import io
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import pandas as pd
from google.cloud import storage
import gc

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

def _set_env(var: str):
    # Load environment variables from the .env file
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)

    # Retrieve the value of the environment variable
    # os.getenv(var)
    # print(value)

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname

_set_env('PROJECT_ID')
_set_env('GCP_CREDENTIALS')
_set_env('BUCKET_NAME')

BUCKET = os.environ.get("BUCKET_NAME",)




def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
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

        # Define the schema
        taxi_dtypes = {
            'VendorID': pd.Int64Dtype(),
            'store_and_fwd_flag': str,
            'RatecodeID': pd.Int64Dtype(),
            'PULocationID': pd.Int64Dtype(),
            'DOLocationID': pd.Int64Dtype(),
            'passenger_count': pd.Int64Dtype(),
            'trip_distance': float,
            'fare_amount': float,
            'extra': float,
            'mta_tax': float,
            'tip_amount': float,
            'tolls_amount': float,
            'ehail_fee': float,
            'improvement_surcharge': float,
            'total_amount': float,
            'payment_type': pd.Int64Dtype(),
            'trip_type': pd.Int64Dtype(),
            'congestion_surcharge': float 
            }

        parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']


        # Process in chunks to optimize memory
        parquet_file = file_name.replace('.csv.gz', '.parquet')
        temp_parquet_files = []

        with pd.read_csv(
            file_name, compression='gzip', dtype=taxi_dtypes, 
            parse_dates=parse_dates, chunksize=100000, low_memory=False
        ) as reader:
            for chunk_idx, chunk in enumerate(reader):
                temp_file = f"{parquet_file}_part{chunk_idx}.parquet"
                chunk.to_parquet(temp_file, engine='pyarrow', index=False)
                temp_parquet_files.append(temp_file)

        # Combine all chunk files into one
        combined_df = pd.concat([pd.read_parquet(temp_file) for temp_file in temp_parquet_files])
        combined_df.to_parquet(parquet_file, engine='pyarrow', index=False)
        print(f"Parquet: {parquet_file}")

        # Cleanup temporary chunk files
        for temp_file in temp_parquet_files:
            os.remove(temp_file)


        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{service}/{parquet_file}", parquet_file)
        print(f"GCS: {service}/{parquet_file}")

        # Cleanup local files to save disk space
        os.remove(parquet_file.replace('.parquet', '.csv.gz'))
        os.remove(parquet_file)
        #print(f"Cleaned up local files: {file_name})

        # Free memory
        #gc.collect()

# # This script is for Green taxi data only... 
web_to_gcs('2019', 'green')
web_to_gcs('2020', 'green')

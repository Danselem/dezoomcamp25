-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.ny_taxi.external_yellow24_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://scenic-dynamo-447811-m9-dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata AS
SELECT * FROM scenic-dynamo-447811-m9.ny_taxi.external_yellow24_tripdata;

-- Count of records for the 2024 Yellow Taxi Data
SELECT COUNT(*) AS total_records
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`;


SELECT COUNT(DISTINCT PULocationID)
FROM `scenic-dynamo-447811-m9.ny_taxi.external_yellow24_tripdata`;
-- external estimated amount 0MB

SELECT COUNT(DISTINCT PULocationID)
FROM scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata;
-- native estimated amount 155.12MB


SELECT PULocationID
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`;
-- estimated amount 155.12MB

SELECT PULocationID, DOLocationID
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`;
-- estimated amount 310.24MB

-- records have a fare_amount of 0
SELECT COUNT(1)
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`
WHERE fare_amount = 0;
-- 8333


CREATE OR REPLACE TABLE `scenic-dynamo-447811-m9.ny_taxi.partitioned_yellow24_tripdata`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS (
  SELECT * FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`
);


SELECT DISTINCT(VendorID) 
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT(VendorID) 
FROM `scenic-dynamo-447811-m9.ny_taxi.partitioned_yellow24_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';


SELECT COUNT(*)
FROM `scenic-dynamo-447811-m9.ny_taxi.yellow24_tripdata`;
-- 0B
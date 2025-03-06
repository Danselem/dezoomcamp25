-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/yellow/yellow_tripdata_2019-*.parquet', 'gs://dezoomcamp25/yellow/yellow_tripdata_2020-*.parquet']
);


CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/yellow/*.parquet']
);


CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/green/green_tripdata_2019-*.parquet', 'gs://dezoomcamp25/green/green_tripdata_2020-*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/green/*.parquet']
);


CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/fhv/fhv_tripdata_2019-*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `scenic-dynamo-447811-m9.trips_data_all.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp25/fhv/*.parquet']
);


-- create materialized table for yellow taxi data
CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.yellow_tripdata
AS(
SELECT 
  VendorID,
  TIMESTAMP_MICROS(CAST(tpep_pickup_datetime / 1000 AS INT64)) AS tpep_pickup_datetime,
  TIMESTAMP_MICROS(CAST(tpep_dropoff_datetime / 1000 AS INT64)) AS tpep_dropoff_datetime,
  passenger_count,
  trip_distance,
  RatecodeID,
  store_and_fwd_flag,
  PULocationID,
  DOLocationID,
  payment_type,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  improvement_surcharge,
  total_amount,
  congestion_surcharge
FROM scenic-dynamo-447811-m9.trips_data_all.external_yellow_tripdata
);


-- create materialized table for green taxi data
CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.green_tripdata
AS(
SELECT 
  VendorID,
  TIMESTAMP_MICROS(CAST(lpep_pickup_datetime / 1000 AS INT64)) AS lpep_pickup_datetime,
  TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime / 1000 AS INT64)) AS lpep_dropoff_datetime,
  store_and_fwd_flag,
  RatecodeID,
  PULocationID,
  DOLocationID,
  passenger_count,
  trip_distance,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  ehail_fee,
  improvement_surcharge,
  total_amount,
  payment_type,
  trip_type,
  congestion_surcharge 
FROM scenic-dynamo-447811-m9.trips_data_all.external_green_tripdata
);



-- create materialized table for fhv taxi data
CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.fhv_tripdata
AS(
SELECT 
  dispatching_base_num,
  TIMESTAMP_MICROS(CAST(pickup_datetime / 1000 AS INT64)) AS pickup_datetime,
  TIMESTAMP_MICROS(CAST(dropOff_datetime / 1000 AS INT64)) AS dropOff_datetime,
  PULocationID,
  DOLocationID,
  SR_Flag,
  Affiliated_base_number 
FROM scenic-dynamo-447811-m9.trips_data_all.external_fhv_tripdata
);











CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.yellow_tripdata AS
SELECT * FROM scenic-dynamo-447811-m9.trips_data_all.external_yellow_tripdata;


CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.green_tripdata AS
SELECT * FROM scenic-dynamo-447811-m9.trips_data_all.external_green_tripdata;

CREATE OR REPLACE TABLE scenic-dynamo-447811-m9.trips_data_all.fhv_tripdata AS
SELECT * FROM scenic-dynamo-447811-m9.trips_data_all.external_fhv_tripdata;


SELECT count(*) as yellow_trips
FROM scenic-dynamo-447811-m9.trips_data_all.yellow_tripdata;

SELECT count(*) as green_trips
FROM scenic-dynamo-447811-m9.trips_data_all.green_tripdata;

SELECT count(*) as fhv_trips
FROM scenic-dynamo-447811-m9.trips_data_all.fhv_tripdata;

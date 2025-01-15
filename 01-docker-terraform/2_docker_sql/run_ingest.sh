#!/bin/bash

# Define the Yellow taxi URL
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"


docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}


# Define the Green taxi URL
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

# Run the Docker container with the specified arguments
docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url="${URL}"


## Define the Zone URL
zone_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# Run the Docker container with the specified arguments
docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=zones \
  --url="${zone_url}"
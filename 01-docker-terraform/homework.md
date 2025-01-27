# Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice
Docker and SQL

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework. 

When your solution has SQL or shell commands and not code
(e.g. python files) file format, include them directly in
the README file of your repository.


## Question 1. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1

## Solution
```bash
  docker run -it --entrypoint bash python:3.12.8
  pip --version
```
24.2.1

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

If there are more than one answers, select only one of them
## Solution
postgres:5432

##  Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from October 2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether
you want to use Jupyter or a python script.

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles 

Answers:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202

## Solution
```SQL
SELECT 
  CASE
      WHEN trip_distance <= 1 THEN '0-1 mile'
      WHEN trip_distance > 1 AND trip_distance <= 3 THEN '1-3 miles'
      WHEN trip_distance > 3 AND trip_distance <= 7 THEN '3-7 miles'
      WHEN trip_distance > 7 AND trip_distance <= 10 THEN '7-10 miles'
      ELSE 'Over 10 miles'
  END AS distance_category,
  COUNT(*) AS trip_count
FROM green_taxi_trips t
WHERE CAST(lpep_dropoff_datetime AS DATE) >= '2019-10-01' 
  AND CAST(lpep_dropoff_datetime AS DATE) < '2019-11-01'
GROUP BY 
    CASE
        WHEN trip_distance <= 1 THEN '0-1 mile'
        WHEN trip_distance > 1 AND trip_distance <= 3 THEN '1-3 miles'
        WHEN trip_distance > 3 AND trip_distance <= 7 THEN '3-7 miles'
        WHEN trip_distance > 7 AND trip_distance <= 10 THEN '7-10 miles'
        ELSE 'Over 10 miles'
    END
ORDER BY distance_category;
```
- 104,802;  198,924;  109,603;  27,678;  35,189

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31

## Solution
```SQL
SELECT
    CAST(lpep_pickup_datetime AS DATE) AS "pickday",
    MAX(trip_distance) AS longest_trip_distance
FROM 
    green_taxi_trips t
GROUP BY
    CAST(lpep_pickup_datetime AS DATE)
ORDER BY
    longest_trip_distance DESC
LIMIT 1;
```
- 2019-10-31

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

## Solution
```SQL
SELECT zpu."Zone", SUM(t.total_amount) AS total_amount_sum
FROM green_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zones."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2019-10-18'
GROUP BY zpu."Zone"
HAVING SUM(t.total_amount) > 13000
ORDER BY total_amount_sum DESC;
```
- East Harlem North, East Harlem South, Morningside Heights

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone
named "East Harlem North" which was the drop off zone that had
the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

## Solution
```SQL
SELECT zpu."Zone" AS pickup_zone, zdo."Zone" AS dropoff_zone,
  MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE
  DATE(t.lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
	AND zpu."Zone"='East Harlem North'
GROUP BY pickup_zone, dropoff_zone
ORDER BY max_tip DESC;
```
- JFK Airport

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](../../../01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

## Solution
```bash
  terraform init

Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/google versions matching "4.51.0"...
- Installing hashicorp/google v4.51.0...
- Installed hashicorp/google v4.51.0 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

```bash
terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "dext"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + project                    = "scenic-dynamo-447811-m9"
      + self_link                  = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "dextra"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "Delete"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 30
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning {
          + enabled = true
        }

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

```bash
terraform apply


Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/scenic-dynamo-447811-m9/datasets/dext]
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dextra]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
```bash
terraform destroy

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_storage_bucket.data-lake-bucket: Destroying... [id=dextra]
google_bigquery_dataset.dataset: Destroying... [id=projects/scenic-dynamo-447811-m9/datasets/dext]
google_bigquery_dataset.dataset: Destruction complete after 0s
google_storage_bucket.data-lake-bucket: Destruction complete after 0s

Destroy complete! Resources: 2 destroyed.
```
- terraform init, terraform apply -auto-approve, terraform destroy

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1

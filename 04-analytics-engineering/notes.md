
## To set up locl dbt core:

mkdir custom
cd custom/
cp ../docker_setup/Dockerfile .
cp ../docker_setup/docker-compose.yaml .

## Edit the docker-compose.yaml
Edit the docker-compose and rename the service to your choice, e.g. `dbt-bq-nyc`.

## Setup dbt profile.

To create a dbt profile, follow the commands:

```bash
mkdir ~/.dbt/
vi ~/.dbt/profiles.yml
```

Copy and paste the info below into ~/.dbt/profiles.yml:
Change `dataset`, `location`, `project` to your gcp project id.
`taxi_data` can be renamed to your choice.

```bash
taxi_data:
  outputs:
    dev:
      dataset: ny_taxi
      fixed_retries: 1
      keyfile: /.google/credentials/google_credentials.json
      location: US
      method: service-account
      priority: interactive
      project: scenic-dynamo-447811-m9
      threads: 4
      timeout_seconds: 300
      type: bigquery
  target: dev
```
**Note**: Ensure your GCP credentials is saved in `.google/credentials/google_credentials.json`.

## Build the docker compose

```bash
docker compose build
```

## Run the docker

```bash
docker compose run dbt-bq-nyc init
```

## Error ModuleNotFoundError: No module named 'pytz'
While trying to run `docker compose run dbt-bq-nyc init`, an error occurs: `ModuleNotFoundError: No module named 'pytz'`

**Solution**

Edit the `Dockerfile` and include under dbt-bigquery

```bash
RUN python -m pip install pytz
```
the build the docker again

## Run Docker


   - **Note:** We are essentially running `dbt init` above because the `ENTRYPOINT` in the [Dockerfile](Dockerfile) is `['dbt']`.
    - Input the required values. Project name will be `taxi_data`
    - This should create `dbt/taxi_data/` and you should see `dbt_project.yml` in there.
    - In `dbt_project.yml`, replace `profile: 'taxi_rides_ny'` with `profile: 'bq-dbt-nyc'` as we have a profile with the later name in our `profiles.yml`


## Error

```bash
Failed to save 'dbt_project.yml': Unable to write file 'vscode-remote://ssh-remote+gcp/home/daniel/dezoomcamp25/04-analytics-engineering/custom/dbt/taxi_data/dbt_project.yml' (NoPermissions (FileSystemError): Error: EACCES: permission denied, open '/home/daniel/dezoomcamp25/04-analytics-engineering/custom/dbt/taxi_data/dbt_project.yml')
```

```bash
sudo chmod 777 /home/daniel/dezoomcamp25/04-analytics-engineering/custom/dbt/taxi_data/dbt_project.yml


sudo chmod 777 /home/daniel/dezoomcamp25/04-analytics-engineering/custom/dbt/taxi_rides/dbt_project.yml
```

```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-nyc debug
```

### Install packages

```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-nyc deps
```

```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-nyc build
```

Make folders rewritable

sudo chown -R daniel:daniel custom/dbt/


### Run

```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-nyc run
```
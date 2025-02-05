docker compose down --volumes

docker compose up -d


docker system prune -a --volumes

docker logs 02-workflow-orchestration-kestra-1

docker compose down --volumes

## Internal error in Kestra Flow

```
2025-01-24 03:38:13.760org.postgresql.util.PSQLException: The connection attempt failed.
2025-01-24 03:38:13.760The connection attempt failed.
 host.docker.internal
```

Fix with 
```bash
url: jdbc:postgresql://postgres:5432/kestra
```


## Running executable script
```bash
    chmod +x addFlow.sh

    ./addFlow.sh
```

## Error while running `dbt`

```bash
    Database Error
  could not translate host name "host.docker.internal" to address: Name or service not known
```
**Solution**
Run the command `hostname -I` on the terminal and use the first ip address as the host, e.g in

```bash
host: host.docker.internal
```

replace `host.docker.internal` with the first ip address

first address after using the command `hostname -I
hostname -I

## Scheduling with Kestra
Click `Trigger`
Note: after setting the date, under `advanced configuration`, for Excution labels.

```bash
Key: backfill
Value: true
```
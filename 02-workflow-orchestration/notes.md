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
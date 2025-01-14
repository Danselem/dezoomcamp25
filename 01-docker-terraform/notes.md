## Instructions for installing Docker
To install `Docker` on Ubuntu, forllow the instructions on the [Docker installation guide](https://docs.docker.com/engine/install/ubuntu/).


## How to configure Docker to run without sudo
```bash
    sudo groupadd docker
    sudo gpasswd -a $USER docker
    docker run hello-world
    sudo service docker restart
    logout
```

## Installing Terraform
To install `terraform`, follow the installtion instructions at [Terraform website](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

## How to spin a docker compose file
If you have a `docker-compose.yaml` and want to quickly spin up a docker compose container, then run the command n detach mode:
```bash
    docker compose up -d
```
Also, to shut down the container, run:
```bash
    docker compose down
```

To view a running container:
```bash
    docker ps
```
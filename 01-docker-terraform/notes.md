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

## How to use git and Github in a VM
If you want to use git in a VM to handle your Github project, then you need to do the following.

### Generate SSH key
In your VM compute on the terminal, run the command below to geneate an ssh key:
```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
```
This will generate two files `id_ed25519` and `id_ed25519.pub`.

### Adding your SSH key to the ssh-agent
Type the command below to add your SSH key to the ssh agent.
```bash
    eval "$(ssh-agent -s)"
```
### Configure Git parameters
Provide your Github information profile with the command: 
```bash
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
```

### Add SSH key to Github
Go to your Github account profile, click `Settings` under Freeture preview. On the right, click `SSH and GPG keys` to open up the SSH keys page. Click the green button `New SSH key` to add a title and your ssh key.

On your terminal, type:
```bash
    cat ~/.ssh/id_ed25519.pub
```
This will display your ssh public key, copy it and paste inside the `Key` box on Github, then click `Add SSH key` to complete the task.

## Google Application Credentials
### Setup for Access
 
1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   
3. Please ensure `GOOGLE_APPLICATION_CREDENTIALS` env-var is set.
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```


```bash
    export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/gcp.json
```
Now authenticate:
```bash
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
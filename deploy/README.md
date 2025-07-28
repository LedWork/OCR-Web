# Update and backup

## Make scripts executable (one-time setup)
chmod +x deploy/*.sh

## Deploy update

```bash
# export all deployment env variables
export DOCKER_COMPOSE_FILE=./docker-compose-deploy.yaml
git pull origin main
cd frontend/app
./build.sh
cd -
./deploy/update-deployment.sh
```

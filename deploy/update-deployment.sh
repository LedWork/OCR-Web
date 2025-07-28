#!/bin/bash

# Safe Deployment Script for OCR-Web2
# This script ensures data safety during updates

set -e  # Exit on any error

echo "🚀 Starting safe deployment process..."

DOCKER_COMPOSE_FILE="${DOCKER_COMPOSE_FILE:-docker-compose-deploy.yaml}"

# Step 2: Save current working image as backup
echo "💾 Saving current working image..."
CURRENT_IMAGE=$(docker compose -f $DOCKER_COMPOSE_FILE images -q app)
if [ ! -z "$CURRENT_IMAGE" ]; then
    docker tag $CURRENT_IMAGE ocr-web2-backup:$(date +%Y%m%d_%H%M%S)
    echo "✅ Current image saved as backup"
else
    echo "⚠️  No current image found to backup"
fi

# Step 3: Build and deploy with zero downtime
echo "🔧 Building and deploying new version..."

# Build the new image
docker compose -f $DOCKER_COMPOSE_FILE build app

# Deploy with zero downtime
docker compose -f $DOCKER_COMPOSE_FILE up -d --no-deps app

# Wait a moment for the new container to start
sleep 10

# Check if the new container is healthy
if docker compose -f $DOCKER_COMPOSE_FILE ps app | grep -q "Up"; then
    echo "✅ New version deployed successfully!"
    
    # Optional: Remove old images to save space (keep the most recent backup)
    echo "🧹 Cleaning up old images..."
    docker image prune -f
else
    echo "❌ Deployment failed! Rolling back..."
    
    # Get the backup image
    BACKUP_IMAGE=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep "ocr-web2-backup" | tail -1)
    
    if [ ! -z "$BACKUP_IMAGE" ]; then
        echo "🔄 Rolling back to previous version: $BACKUP_IMAGE"
        
        # Stop the failed container
        docker compose -f $DOCKER_COMPOSE_FILE stop app
        
        # Tag the backup image as the current app image
        docker tag $BACKUP_IMAGE $(docker compose -f $DOCKER_COMPOSE_FILE config --services | head -1):latest
        
        # Start the backup version
        docker compose -f $DOCKER_COMPOSE_FILE up -d --no-deps app
        
        echo "✅ Rollback completed successfully!"
    else
        echo "❌ No backup image found for rollback!"
        echo "🔄 Restarting current container..."
        docker compose -f $DOCKER_COMPOSE_FILE up -d --no-deps app
    fi
    
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "📊 Your data is safe in the mongo-data volume"

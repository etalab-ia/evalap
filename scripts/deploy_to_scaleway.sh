#!/bin/bash
set -e

# Configuration
CONTAINER_NAME="evalap"
REGION="fr-par"
# Try to get repository name from git, otherwise default
REPO_NAME=$(git config --get remote.origin.url | sed -E 's/.*github.com[:\/](.*)\.git/\1/' | tr '[:upper:]' '[:lower:]')
IMAGE_NAME="ghcr.io/${REPO_NAME}/evalap"
IMAGE_TAG=$(git rev-parse --short HEAD)

# Check dependencies
if ! command -v scw &> /dev/null; then
    echo "Error: scw CLI is not installed."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed."
    exit 1
fi

echo "🚀 Starting deployment of $CONTAINER_NAME to Scaleway ($REGION)"

# 1. Build the production image
echo "📦 Building production Docker image..."
docker build --platform linux/amd64 -t "${IMAGE_NAME}:${IMAGE_TAG}" .

# 2. Push to Registry
echo "⬆️ Pushing image to $IMAGE_NAME:$IMAGE_TAG..."
docker push "${IMAGE_NAME}:${IMAGE_TAG}"

# 3. Find Scaleway Container ID
echo "🔍 Searching for container named '$CONTAINER_NAME'..."
CONTAINER_ID=$(scw container container list region=$REGION name=$CONTAINER_NAME -o json | jq -r '.[0].id')

if [ "$CONTAINER_ID" == "null" ] || [ -z "$CONTAINER_ID" ]; then
    echo "❌ Error: Container '$CONTAINER_NAME' not found in region $REGION."
    echo "Please create the container first in the Scaleway Console or via Terraform."
    exit 1
fi

echo "✅ Found container ID: $CONTAINER_ID"

# 4. Update and Deploy
echo "🔄 Updating container with new image..."
scw container container update "$CONTAINER_ID" \
    region=$REGION \
    registry-image="${IMAGE_NAME}:${IMAGE_TAG}" \
    port=8080

echo "🚀 Triggering deployment..."
scw container container deploy "$CONTAINER_ID" region=$REGION

echo "✨ Deployment triggered successfully!"
echo "Check the status at: https://console.scaleway.com/containers/containers/$REGION/$CONTAINER_ID"

#!/bin/bash
set -e

# Configuration
CONTAINER_NAME="evalap"
REGION="fr-par"

# Get Scaleway Registry endpoint
echo "🔍 Fetching Scaleway Registry endpoint for namespace 'evalap'..."
REGISTRY_ENDPOINT=$(scw registry namespace list region=$REGION -o json | jq -r '.[] | select(.name == "evalap") | .endpoint')

if [ -z "$REGISTRY_ENDPOINT" ]; then
    echo "❌ Error: Scaleway Registry namespace 'evalap' not found in region $REGION."
    echo "Current namespaces:"
    scw registry namespace list region=$REGION
    exit 1
fi

IMAGE_NAME="${REGISTRY_ENDPOINT}/${CONTAINER_NAME}"
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

# 2. Login to Scaleway Registry
echo "🔐 Logging in to Scaleway Registry..."
scw registry login

# 3. Push to Registry
echo "⬆️ Pushing image to $IMAGE_NAME:$IMAGE_TAG..."
docker push "${IMAGE_NAME}:${IMAGE_TAG}"

# 4. Find Scaleway Container ID
echo "🔍 Searching for container named '$CONTAINER_NAME'..."
CONTAINER_ID=$(scw container container list region=$REGION name=$CONTAINER_NAME -o json | jq -r '.[0].id')

if [ "$CONTAINER_ID" == "null" ] || [ -z "$CONTAINER_ID" ]; then
    echo "❌ Error: Container '$CONTAINER_NAME' not found in region $REGION."
    echo "Please create the container first in the Scaleway Console or via Terraform."
    exit 1
fi

echo "✅ Found container ID: $CONTAINER_ID"

# 5. Update and Deploy
echo "🔄 Updating container with new image..."
scw container container update "$CONTAINER_ID" \
    region=$REGION \
    registry-image="${IMAGE_NAME}:${IMAGE_TAG}" \
    port=8080

echo "🚀 Triggering deployment..."
scw container container deploy "$CONTAINER_ID" region=$REGION

echo "✨ Deployment triggered successfully!"
echo "Check the status at: https://console.scaleway.com/containers/containers/$REGION/$CONTAINER_ID"

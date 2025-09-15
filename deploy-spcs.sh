#!/bin/bash

# SPCS Deployment Script for Live Coding Interview Platform
# This script helps deploy the application to Snowflake Park Container Services

echo "🚀 Live Coding Interview Platform - SPCS Deployment Script"
echo "=========================================================="

# Check if required environment variables are set
if [ -z "$SNOWFLAKE_ACCOUNT" ] || [ -z "$SNOWFLAKE_USER" ] || [ -z "$SNOWFLAKE_PASSWORD" ] || [ -z "$SNOWFLAKE_DATABASE" ] || [ -z "$SNOWFLAKE_SCHEMA" ]; then
    echo "❌ Missing required environment variables. Please set:"
    echo "   - SNOWFLAKE_ACCOUNT"
    echo "   - SNOWFLAKE_USER"
    echo "   - SNOWFLAKE_PASSWORD"
    echo "   - SNOWFLAKE_DATABASE"
    echo "   - SNOWFLAKE_SCHEMA"
    exit 1
fi

# Configuration
IMAGE_NAME="coding-interview-platform"
SERVICE_NAME="coding_interview_service"
COMPUTE_POOL="${COMPUTE_POOL:-default_compute_pool}"
REGISTRY_PATH="/${SNOWFLAKE_DATABASE}/${SNOWFLAKE_SCHEMA}/${IMAGE_NAME}"

echo "📋 Configuration:"
echo "   Account: $SNOWFLAKE_ACCOUNT"
echo "   Database: $SNOWFLAKE_DATABASE"
echo "   Schema: $SNOWFLAKE_SCHEMA"
echo "   Image: $IMAGE_NAME"
echo "   Registry Path: $REGISTRY_PATH"
echo "   Compute Pool: $COMPUTE_POOL"
echo ""

# Step 1: Build Docker image
echo "🔨 Step 1: Building Docker image..."
docker build -t $IMAGE_NAME:latest .
if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi
echo "✅ Docker image built successfully"
echo ""

# Step 2: Login to Snowflake Docker registry
echo "🔐 Step 2: Logging into Snowflake registry..."
REGISTRY_HOST="${SNOWFLAKE_ACCOUNT}.registry.snowflakecomputing.com"
echo $SNOWFLAKE_PASSWORD | docker login $REGISTRY_HOST -u $SNOWFLAKE_USER --password-stdin
if [ $? -ne 0 ]; then
    echo "❌ Failed to login to Snowflake registry!"
    exit 1
fi
echo "✅ Successfully logged into Snowflake registry"
echo ""

# Step 3: Tag and push image
echo "📤 Step 3: Tagging and pushing image..."
docker tag $IMAGE_NAME:latest $REGISTRY_HOST$REGISTRY_PATH:latest
docker push $REGISTRY_HOST$REGISTRY_PATH:latest
if [ $? -ne 0 ]; then
    echo "❌ Failed to push image to registry!"
    exit 1
fi
echo "✅ Image pushed successfully"
echo ""

# Step 4: Create SPCS specification
echo "📝 Step 4: Creating SPCS specification..."
cat > spcs-spec-generated.yaml << EOF
spec:
  containers:
  - name: coding-interview-app
    image: $REGISTRY_PATH:latest
    env:
      DATABASE_URL: \${DATABASE_URL}
      SECRET_KEY: \${SECRET_KEY}
      REDIS_URL: \${REDIS_URL}
      MAX_EXECUTION_TIME: "30"
      MAX_MEMORY_LIMIT: "128"
    resources:
      requests:
        cpu: 1
        memory: 2Gi
      limits:
        cpu: 2
        memory: 4Gi
    readinessProbe:
      port: 8000
      path: /health
    livenessProbe:
      port: 8000
      path: /health
  endpoints:
  - name: app-endpoint
    port: 8000
    public: true
EOF
echo "✅ SPCS specification created: spcs-spec-generated.yaml"
echo ""

# Step 5: Generate Snowflake SQL commands
echo "📜 Step 5: Generating Snowflake SQL commands..."
cat > deploy-service.sql << EOF
-- Create image repository (if not exists)
CREATE IMAGE REPOSITORY IF NOT EXISTS ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${IMAGE_NAME};

-- Create or replace the service
CREATE OR REPLACE SERVICE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SERVICE_NAME}
  IN COMPUTE POOL ${COMPUTE_POOL}
  FROM SPECIFICATION_FILE='spcs-spec-generated.yaml'
  EXTERNAL_ACCESS_INTEGRATIONS = ()
  AUTO_RESUME = TRUE
  MIN_INSTANCES = 1
  MAX_INSTANCES = 3;

-- Grant necessary permissions
GRANT USAGE ON SERVICE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SERVICE_NAME} TO ROLE PUBLIC;

-- Resume the service
ALTER SERVICE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SERVICE_NAME} RESUME;

-- Show service status
DESCRIBE SERVICE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SERVICE_NAME};

-- Show service endpoints
SHOW ENDPOINTS IN SERVICE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SERVICE_NAME};
EOF
echo "✅ Snowflake SQL commands generated: deploy-service.sql"
echo ""

echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Connect to Snowflake and execute the SQL commands in 'deploy-service.sql'"
echo "2. Set the required environment variables in Snowflake:"
echo "   - DATABASE_URL: Your database connection string"
echo "   - SECRET_KEY: A strong secret key for JWT signing"
echo "   - REDIS_URL: Redis connection string (optional)"
echo "3. Monitor the service status and access the application via the provided endpoint"
echo ""
echo "📚 For more details, refer to the README.md file"
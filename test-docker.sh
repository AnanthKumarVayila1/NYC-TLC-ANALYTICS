#!/bin/bash

###############################################################################
# Local Testing and Validation Script
# Tests Docker builds and validates configuration files
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        NYC TLC Analytics - Local Testing Script               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Docker
echo -e "${YELLOW}🐳 Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    echo "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo "Please start Docker Desktop"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed and running${NC}"
echo ""

# Validate configuration files
echo -e "${YELLOW}📋 Validating configuration files...${NC}"

FILES=(
    "backend/Dockerfile"
    "backend/.dockerignore"
    "frontend/Dockerfile"
    "frontend/.dockerignore"
    "frontend/nginx.conf"
    "docker-compose.yml"
    ".github/workflows/backend-ci-cd.yml"
    ".github/workflows/frontend-ci-cd.yml"
    ".github/workflows/tests.yml"
    "deployment/azure-deploy.sh"
    "deployment/azure-template.json"
    "deployment/AZURE_DEPLOYMENT.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file (missing)${NC}"
    fi
done
echo ""

# Test backend Docker build
echo -e "${YELLOW}🔨 Testing Backend Docker build...${NC}"
if docker build -t nyc-tlc-backend:test ./backend; then
    echo -e "${GREEN}✅ Backend Docker image built successfully${NC}"
    
    # Show image size
    IMAGE_SIZE=$(docker images nyc-tlc-backend:test --format "{{.Size}}")
    echo -e "${BLUE}   Image size: $IMAGE_SIZE${NC}"
else
    echo -e "${RED}❌ Backend Docker build failed${NC}"
    exit 1
fi
echo ""

# Test frontend Docker build
echo -e "${YELLOW}🔨 Testing Frontend Docker build...${NC}"
if docker build -t nyc-tlc-frontend:test ./frontend; then
    echo -e "${GREEN}✅ Frontend Docker image built successfully${NC}"
    
    # Show image size
    IMAGE_SIZE=$(docker images nyc-tlc-frontend:test --format "{{.Size}}")
    echo -e "${BLUE}   Image size: $IMAGE_SIZE${NC}"
else
    echo -e "${RED}❌ Frontend Docker build failed${NC}"
    exit 1
fi
echo ""

# Test docker-compose validation
echo -e "${YELLOW}📦 Validating docker-compose.yml...${NC}"
if docker-compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✅ docker-compose.yml is valid${NC}"
else
    echo -e "${RED}❌ docker-compose.yml has errors${NC}"
    exit 1
fi
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✅ All Tests Passed!                              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo "1. Start services: docker-compose up --build"
echo "2. Test backend: curl http://localhost:8000/health"
echo "3. Test frontend: open http://localhost:80"
echo "4. Deploy to Azure: ./deployment/azure-deploy.sh"
echo ""

echo -e "${YELLOW}To clean up test images:${NC}"
echo "docker rmi nyc-tlc-backend:test nyc-tlc-frontend:test"
echo ""

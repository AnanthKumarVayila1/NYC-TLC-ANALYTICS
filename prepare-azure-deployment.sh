#!/bin/bash

###############################################################################
# Azure Portal Deployment Helper
# This script helps you prepare for Azure deployment via UI
###############################################################################

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     NYC TLC Analytics - Azure Portal Deployment Helper        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}This helper will guide you through Azure Portal deployment.${NC}"
echo -e "${YELLOW}No GitHub Secrets needed - we'll use the Portal UI!${NC}"
echo ""

# Check if Azure account exists
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 1: Azure Account${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
read -p "Do you have an Azure account? (y/n): " has_account

if [ "$has_account" != "y" ]; then
    echo ""
    echo -e "${GREEN}✨ Create a FREE Azure account:${NC}"
    echo "   https://azure.microsoft.com/free"
    echo ""
    echo "Benefits:"
    echo "   • $200 free credit for 30 days"
    echo "   • Many services free for 12 months"
    echo "   • Some services always free"
    echo ""
    read -p "Press Enter after creating your account..."
fi

echo ""
echo -e "${GREEN}✅ Great! Let's prepare for deployment.${NC}"
echo ""

# Check Azure CLI and current account
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 1.5: Check Azure Account${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if command -v az &> /dev/null; then
    echo "Checking Azure login status..."
    echo ""
    
    if az account show &> /dev/null; then
        CURRENT_USER=$(az account show --query "user.name" -o tsv)
        CURRENT_SUB=$(az account show --query "name" -o tsv)
        CURRENT_TENANT=$(az account show --query "tenantDisplayName" -o tsv)
        
        echo -e "${GREEN}✅ You are logged into Azure:${NC}"
        echo ""
        echo "   User: $CURRENT_USER"
        echo "   Subscription: $CURRENT_SUB"
        echo "   Tenant: $CURRENT_TENANT"
        echo ""
        
        read -p "Is this the correct account for deployment? (y/n): " correct_account
        
        if [ "$correct_account" != "y" ]; then
            echo ""
            echo -e "${YELLOW}Let's see your available subscriptions:${NC}"
            echo ""
            az account list --output table
            echo ""
            echo "To switch to a different account:"
            echo "   1. Different email: az logout && az login"
            echo "   2. Different subscription: az account set --subscription \"NAME\""
            echo ""
            read -p "Press Enter after switching accounts..."
            
            # Check again
            CURRENT_USER=$(az account show --query "user.name" -o tsv)
            CURRENT_SUB=$(az account show --query "name" -o tsv)
            echo ""
            echo -e "${GREEN}✅ Now using:${NC}"
            echo "   User: $CURRENT_USER"
            echo "   Subscription: $CURRENT_SUB"
        fi
    else
        echo -e "${YELLOW}⚠️  Not logged into Azure. Please login:${NC}"
        echo ""
        echo "   az login"
        echo ""
        read -p "Press Enter after logging in..."
    fi
else
    echo -e "${YELLOW}⚠️  Azure CLI not installed.${NC}"
    echo ""
    echo "Install with: brew install azure-cli"
    echo ""
    read -p "Press Enter after installing Azure CLI..."
fi

echo ""

# Database info
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 2: Database Information${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Your current database setup:"
echo "   Server: nyc-sqldb-server.database.windows.net"
echo "   Database: nyc-sqldatabase"
echo "   User: serveradmin"
echo ""
read -p "Press Enter to continue..."

# Generate SECRET_KEY
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 3: Generate SECRET_KEY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Generating a secure SECRET_KEY for JWT authentication..."
echo ""

if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo -e "${GREEN}✅ Generated SECRET_KEY:${NC}"
    echo ""
    echo -e "${YELLOW}$SECRET_KEY${NC}"
    echo ""
    echo "💾 IMPORTANT: Copy this key! You'll need it in Azure Portal."
    echo ""
else
    echo -e "${YELLOW}⚠️  Python not found. Generate manually later with:${NC}"
    echo "   python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
    SECRET_KEY="<GENERATE_THIS>"
fi

# Save to file
cat > deployment-info.txt << EOF
NYC TLC Analytics - Azure Deployment Information
================================================

BACKEND APP SERVICE
-------------------
Name: nyc-tlc-backend-<YOUR-UNIQUE-ID>
Runtime: Python 3.12
OS: Linux
Region: East US
Plan: B1 Basic

ENVIRONMENT VARIABLES TO SET:
-------------------------------
DB_SERVER=nyc-sqldb-server.database.windows.net
DB_NAME=nyc-sqldatabase
DB_USER=serveradmin
DB_PASSWORD=<YOUR-DB-PASSWORD>
DB_DRIVER=ODBC Driver 18 for SQL Server
SECRET_KEY=$SECRET_KEY
ALLOWED_ORIGINS=*

(Update ALLOWED_ORIGINS later with your frontend URL)

STARTUP COMMAND:
----------------
cd backend && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000

FRONTEND STATIC WEB APP
-----------------------
Name: nyc-tlc-frontend-<YOUR-UNIQUE-ID>
Plan: Free
Region: East US 2
Source: Other

DEPLOYMENT URLS (will be available after deployment):
------------------------------------------------------
Backend: https://nyc-tlc-backend-<YOUR-ID>.azurewebsites.net
Frontend: https://nyc-tlc-frontend-<YOUR-ID>.azurestaticapps.net

IMPORTANT FILES:
----------------
• Full Guide: AZURE_PORTAL_DEPLOYMENT.md
• Quick Checklist: QUICK_DEPLOY.md
• This file: deployment-info.txt
EOF

echo ""
echo -e "${GREEN}✅ Deployment information saved to: deployment-info.txt${NC}"
echo ""

# Next steps
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 4: Deploy Backend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "1. Open Azure Portal: https://portal.azure.com"
echo "2. Click 'Create a resource' → Search 'Web App'"
echo "3. Fill in the details from deployment-info.txt"
echo "4. After creation:"
echo "   → Go to 'Deployment Center' → Select 'Local Git'"
echo "   → Copy Git URL and credentials"
echo ""
read -p "Press Enter after setting up App Service..."

echo ""
echo -e "${YELLOW}Now we'll push your code to Azure...${NC}"
echo ""
read -p "Enter your Azure Git URL: " azure_url

if [ ! -z "$azure_url" ]; then
    echo ""
    echo "Adding Azure remote and pushing code..."
    git remote remove azure 2>/dev/null || true
    git remote add azure "$azure_url"
    
    echo ""
    echo -e "${YELLOW}Pushing to Azure (you'll need to enter credentials)...${NC}"
    git push azure main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Code pushed successfully!${NC}"
        echo ""
        echo "⏳ Wait 5-10 minutes for deployment to complete."
    else
        echo ""
        echo -e "${RED}❌ Push failed. Check your credentials and try manually:${NC}"
        echo "   git push azure main"
    fi
fi

# Frontend setup
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 5: Update Frontend Configuration${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
read -p "Enter your Backend URL (e.g., https://nyc-tlc-backend.azurewebsites.net): " backend_url

if [ ! -z "$backend_url" ]; then
    # Update environment.prod.ts
    cat > frontend/environments/environment.prod.ts << EOF
export const environment = {
  production: true,
  apiUrl: '$backend_url'
};
EOF
    
    echo ""
    echo -e "${GREEN}✅ Frontend configuration updated!${NC}"
    echo ""
    echo "Building production frontend..."
    cd frontend
    npm run build -- --configuration production
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Frontend built successfully!${NC}"
        echo "   Output: frontend/dist/nyc-tlc-frontend/"
    else
        echo ""
        echo -e "${RED}❌ Build failed. Run manually:${NC}"
        echo "   cd frontend && npm run build -- --configuration production"
    fi
    cd ..
fi

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}STEP 6: Deploy Frontend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "1. In Azure Portal: Create a resource → 'Static Web App'"
echo "2. Name: nyc-tlc-frontend"
echo "3. Plan: Free"
echo "4. Deploy using Azure CLI:"
echo ""
echo -e "${YELLOW}   az login${NC}"
echo -e "${YELLOW}   az staticwebapp upload \\${NC}"
echo -e "${YELLOW}     --name nyc-tlc-frontend \\${NC}"
echo -e "${YELLOW}     --resource-group nyc-tlc-analytics-rg \\${NC}"
echo -e "${YELLOW}     --app-location frontend/dist/nyc-tlc-frontend${NC}"
echo ""

# Final checklist
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ DEPLOYMENT CHECKLIST${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Complete these steps:"
echo ""
echo "□ Backend App Service created"
echo "□ Environment variables configured (see deployment-info.txt)"
echo "□ Startup command set"
echo "□ Code pushed via Git"
echo "□ Backend /docs page loads"
echo "□ Frontend Static Web App created"
echo "□ Frontend deployed"
echo "□ ALLOWED_ORIGINS updated with frontend URL"
echo "□ SQL Server firewall allows Azure services"
echo "□ Can login with admin/secret"
echo ""
echo -e "${YELLOW}📚 Need help? Read:${NC}"
echo "   • AZURE_PORTAL_DEPLOYMENT.md (detailed guide)"
echo "   • QUICK_DEPLOY.md (quick reference)"
echo "   • deployment-info.txt (your settings)"
echo ""
echo -e "${GREEN}🎉 You're ready to deploy! Good luck!${NC}"
echo ""

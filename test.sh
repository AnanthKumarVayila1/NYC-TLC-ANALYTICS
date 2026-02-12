#!/bin/bash

# NYC TLC Analytics - Complete Testing Script
# This script provides options to test backend, frontend, or both

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

echo "======================================================================="
echo "  🧪 NYC TLC ANALYTICS - TESTING SUITE"
echo "======================================================================="
echo ""

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}$1${NC}"
    echo "-----------------------------------------------------------------------"
}

# Function to check if Python environment is set up
check_python_env() {
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        echo -e "${RED}❌ Python virtual environment not found${NC}"
        echo "Creating virtual environment..."
        python3 -m venv "$PROJECT_ROOT/.venv"
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    fi
}

# Function to check if backend dependencies are installed
check_backend_deps() {
    print_section "📦 Checking Backend Dependencies"
    
    source "$PROJECT_ROOT/.venv/bin/activate"
    
    if ! python -c "import fastapi" 2>/dev/null; then
        echo "Installing backend dependencies..."
        pip install -r "$PROJECT_ROOT/requirements.txt"
        echo -e "${GREEN}✅ Backend dependencies installed${NC}"
    else
        echo -e "${GREEN}✅ Backend dependencies already installed${NC}"
    fi
}

# Function to check if frontend dependencies are installed
check_frontend_deps() {
    print_section "📦 Checking Frontend Dependencies"
    
    if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
        echo "Installing frontend dependencies..."
        cd "$PROJECT_ROOT/frontend"
        npm install
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
        cd "$PROJECT_ROOT"
    else
        echo -e "${GREEN}✅ Frontend dependencies already installed${NC}"
    fi
}

# Function to test backend
test_backend() {
    print_section "🔧 TESTING BACKEND"
    
    check_python_env
    check_backend_deps
    
    echo ""
    echo "Running backend tests..."
    source "$PROJECT_ROOT/.venv/bin/activate"
    cd "$PROJECT_ROOT/backend"
    python run_tests.py
    cd "$PROJECT_ROOT"
}

# Function to start backend server
start_backend() {
    print_section "🚀 STARTING BACKEND SERVER"
    
    check_python_env
    check_backend_deps
    
    source "$PROJECT_ROOT/.venv/bin/activate"
    cd "$PROJECT_ROOT/backend"
    echo ""
    echo "Starting backend server on http://localhost:8000"
    echo "Press CTRL+C to stop"
    echo ""
    python start_server.py
}

# Function to test frontend
test_frontend() {
    print_section "🎨 TESTING FRONTEND"
    
    check_frontend_deps
    
    echo ""
    echo "Frontend testing checklist is available in frontend/TESTING.md"
    echo ""
    echo "To start the frontend development server:"
    echo "  cd frontend"
    echo "  npm start"
    echo ""
    echo "Then open http://localhost:4200 in your browser"
    echo ""
}

# Function to start both services
start_all() {
    print_section "🚀 STARTING ALL SERVICES"
    
    echo ""
    echo "This will start both backend and frontend servers."
    echo ""
    
    # Start backend in background
    check_python_env
    check_backend_deps
    source "$PROJECT_ROOT/.venv/bin/activate"
    
    echo "Starting backend server..."
    cd "$PROJECT_ROOT/backend"
    python start_server.py &
    BACKEND_PID=$!
    cd "$PROJECT_ROOT"
    
    sleep 3
    
    # Start frontend
    check_frontend_deps
    echo "Starting frontend server..."
    cd "$PROJECT_ROOT/frontend"
    npm start &
    FRONTEND_PID=$!
    cd "$PROJECT_ROOT"
    
    echo ""
    echo -e "${GREEN}✅ Both servers started${NC}"
    echo ""
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:4200"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press CTRL+C to stop both servers"
    echo ""
    
    # Wait for user interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
    wait
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "  1) Test Backend (Run automated tests)"
    echo "  2) Start Backend Server (http://localhost:8000)"
    echo "  3) Test Frontend (View testing guide)"
    echo "  4) Start Both Services"
    echo "  5) Run Manual API Tests (requires backend running)"
    echo "  6) Exit"
    echo ""
    read -p "Enter your choice [1-6]: " choice
    
    case $choice in
        1)
            test_backend
            ;;
        2)
            start_backend
            ;;
        3)
            test_frontend
            read -p "Press Enter to return to menu..."
            show_menu
            ;;
        4)
            start_all
            ;;
        5)
            print_section "🧪 MANUAL API TESTS"
            echo ""
            echo "Make sure the backend server is running first!"
            echo ""
            read -p "Is the backend running? (y/n): " backend_running
            if [ "$backend_running" = "y" ]; then
                chmod +x "$PROJECT_ROOT/backend/test_api_manual.sh"
                bash "$PROJECT_ROOT/backend/test_api_manual.sh"
            else
                echo "Please start the backend first (option 2)"
            fi
            read -p "Press Enter to return to menu..."
            show_menu
            ;;
        6)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            show_menu
            ;;
    esac
}

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${RED}⚠️  WARNING: .env file not found${NC}"
    echo ""
    echo "Please create a .env file with your Azure SQL Database credentials."
    echo "You can copy .env.example and update with your actual values:"
    echo ""
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your credentials"
    echo ""
    read -p "Press Enter to continue anyway, or CTRL+C to exit..."
fi

# Run menu
show_menu

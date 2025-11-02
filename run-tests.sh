#!/bin/bash
# Comprehensive test runner script for SkinVision AI

set -e

echo "🧪 Running SkinVision AI Test Suite"
echo "===================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run backend tests
run_backend_tests() {
    echo -e "\n${YELLOW}Running Backend Tests...${NC}"
    cd backend
    
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python -m venv .venv
    fi
    
    source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || true
    
    pip install -q -r requirements.txt
    pytest tests/ -v --cov=app --cov-report=term --cov-report=html
    
    echo -e "${GREEN}✓ Backend tests completed${NC}"
    cd ..
}

# Function to run frontend tests
run_frontend_tests() {
    echo -e "\n${YELLOW}Running Frontend Tests...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi
    
    npm run test:coverage
    
    echo -e "${GREEN}✓ Frontend tests completed${NC}"
    cd ..
}

# Main
echo "Select test suite to run:"
echo "1) Backend only"
echo "2) Frontend only"
echo "3) Both (Full test suite)"
echo "4) Quick tests (no coverage)"

read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        run_backend_tests
        ;;
    2)
        run_frontend_tests
        ;;
    3)
        run_backend_tests
        run_frontend_tests
        echo -e "\n${GREEN}✓ All tests completed successfully!${NC}"
        ;;
    4)
        echo -e "\n${YELLOW}Running Quick Tests...${NC}"
        cd backend && pytest tests/ -v --no-cov && cd ..
        cd frontend && npm test && cd ..
        echo -e "${GREEN}✓ Quick tests completed${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Test suite completed!${NC}"

#!/bin/bash

# Comprehensive Test Runner for Legal Research Platform
# This script runs all tests for both backend and frontend

set -e  # Exit on any error

echo "🧪 Legal Research Platform - Comprehensive Test Suite"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse command line arguments
RUN_BACKEND=true
RUN_FRONTEND=true
RUN_E2E=true
COVERAGE=true
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            RUN_FRONTEND=false
            RUN_E2E=false
            shift
            ;;
        --frontend-only)
            RUN_BACKEND=false
            RUN_E2E=false
            shift
            ;;
        --no-coverage)
            COVERAGE=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --backend-only    Run only backend tests"
            echo "  --frontend-only   Run only frontend tests"
            echo "  --no-coverage     Skip coverage reporting"
            echo "  --verbose         Verbose output"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Test results tracking
BACKEND_RESULT=0
FRONTEND_RESULT=0
E2E_RESULT=0

print_status "Starting comprehensive test suite..."

# Backend Tests
if [ "$RUN_BACKEND" = true ]; then
    print_status "Running Backend Tests..."
    echo "----------------------------------------"
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
        print_warning "No virtual environment found. Creating one..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        # Activate virtual environment
        if [ -d "venv" ]; then
            source venv/bin/activate
        else
            source .venv/bin/activate
        fi
    fi
    
    # Install test dependencies if not present
    print_status "Installing/updating test dependencies..."
    pip install -r requirements.txt
    
    # Run backend tests
    if [ "$COVERAGE" = true ]; then
        if [ "$VERBOSE" = true ]; then
            python3 -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml
        else
            python3 -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml
        fi
    else
        if [ "$VERBOSE" = true ]; then
            python3 -m pytest tests/ -v
        else
            python3 -m pytest tests/
        fi
    fi
    
    BACKEND_RESULT=$?
    
    if [ $BACKEND_RESULT -eq 0 ]; then
        print_success "Backend tests passed!"
    else
        print_error "Backend tests failed!"
    fi
    
    # Generate test report
    if [ "$COVERAGE" = true ] && [ $BACKEND_RESULT -eq 0 ]; then
        print_status "Backend coverage report generated in backend/htmlcov/"
    fi
    
    cd ..
fi

# Frontend Tests
if [ "$RUN_FRONTEND" = true ]; then
    print_status "Running Frontend Tests..."
    echo "----------------------------------------"
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "node_modules not found. Installing dependencies..."
        npm install
    fi
    
    # Install test dependencies
    print_status "Installing/updating frontend test dependencies..."
    npm install
    
    # Run frontend tests
    if [ "$COVERAGE" = true ]; then
        if [ "$VERBOSE" = true ]; then
            npm run test:coverage -- --reporter=verbose
        else
            npm run test:coverage
        fi
    else
        if [ "$VERBOSE" = true ]; then
            npm run test:run -- --reporter=verbose
        else
            npm run test:run
        fi
    fi
    
    FRONTEND_RESULT=$?
    
    if [ $FRONTEND_RESULT -eq 0 ]; then
        print_success "Frontend tests passed!"
    else
        print_error "Frontend tests failed!"
    fi
    
    # Generate test report
    if [ "$COVERAGE" = true ] && [ $FRONTEND_RESULT -eq 0 ]; then
        print_status "Frontend coverage report generated in frontend/coverage/"
    fi
    
    cd ..
fi

# Generate Combined Test Report
print_status "Generating test summary..."
echo "============================================"
echo "📊 Test Results Summary"
echo "============================================"

if [ "$RUN_BACKEND" = true ]; then
    if [ $BACKEND_RESULT -eq 0 ]; then
        print_success "✅ Backend Tests: PASSED"
    else
        print_error "❌ Backend Tests: FAILED"
    fi
fi

if [ "$RUN_FRONTEND" = true ]; then
    if [ $FRONTEND_RESULT -eq 0 ]; then
        print_success "✅ Frontend Tests: PASSED"
    else
        print_error "❌ Frontend Tests: FAILED"
    fi
fi

# Overall result
OVERALL_RESULT=0
if [ "$RUN_BACKEND" = true ] && [ $BACKEND_RESULT -ne 0 ]; then
    OVERALL_RESULT=1
fi
if [ "$RUN_FRONTEND" = true ] && [ $FRONTEND_RESULT -ne 0 ]; then
    OVERALL_RESULT=1
fi

echo "============================================"
if [ $OVERALL_RESULT -eq 0 ]; then
    print_success "🎉 All tests passed successfully!"
else
    print_error "💥 Some tests failed. Please check the output above."
fi

if [ "$COVERAGE" = true ]; then
    echo ""
    print_status "Coverage reports available:"
    if [ "$RUN_BACKEND" = true ]; then
        echo "  📈 Backend: backend/htmlcov/index.html"
    fi
    if [ "$RUN_FRONTEND" = true ]; then
        echo "  📈 Frontend: frontend/coverage/index.html"
    fi
fi

echo ""
print_status "Test run completed!"

exit $OVERALL_RESULT 
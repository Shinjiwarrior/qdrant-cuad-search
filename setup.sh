#!/bin/bash

echo "🔍 Qdrant CUAD Search - Setup Script"
echo "===================================="

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

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    command -v python3 >/dev/null 2>&1 || { print_error "Python 3 is required but not installed. Aborting."; exit 1; }
    command -v node >/dev/null 2>&1 || { print_error "Node.js is required but not installed. Aborting."; exit 1; }
    command -v npm >/dev/null 2>&1 || { print_error "npm is required but not installed. Aborting."; exit 1; }
    
    print_success "All requirements satisfied!"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Copy environment template
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        cp env.example .env
        print_warning "Please edit backend/.env with your API keys before running!"
    fi
    
    cd ..
    print_success "Backend setup complete!"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Copy environment template
    if [ ! -f .env.local ]; then
        print_status "Creating .env.local file from template..."
        cp env.example .env.local
        print_success "Frontend environment configured!"
    fi
    
    cd ..
    print_success "Frontend setup complete!"
}

# Print next steps
print_next_steps() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Set up your API keys:"
    echo "   - Get an OpenAI API key from https://platform.openai.com/"
    echo "   - Set up Qdrant Cloud at https://qdrant.io/"
    echo "   - Edit backend/.env with your credentials"
    echo ""
    echo "2. Load CUAD contract data:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python scripts/load_cuad_data.py"
    echo ""
    echo "3. Start the backend:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn app.main:app --reload"
    echo ""
    echo "4. Start the frontend (in another terminal):"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "5. Visit http://localhost:5173 to use Qdrant CUAD Search!"
    echo ""
    echo "📚 Documentation:"
    echo "   - API docs: http://localhost:8000/docs"
    echo "   - Health check: http://localhost:8000/api/health"
    echo "   - CUAD stats: http://localhost:8000/api/stats"
    echo ""
}

# Main setup process
main() {
    check_requirements
    setup_backend
    setup_frontend
    print_next_steps
}

# Run main function
main 
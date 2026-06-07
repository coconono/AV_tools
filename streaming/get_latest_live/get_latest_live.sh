#!/bin/bash
# get_latest_live.sh
# Shell script to run the YouTube Latest Live Stream Checker

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Virtual environment directory
VENV_DIR=".venv"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

print_info "Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_info "Virtual environment created successfully"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    deactivate
    exit 1
fi

# Check if dependencies are installed
print_info "Checking dependencies..."
DEPS_INSTALLED=true

# Try importing the required modules
python3 -c "import googleapiclient, dotenv, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    DEPS_INSTALLED=false
fi

# Install or update dependencies if necessary
if [ "$DEPS_INSTALLED" = false ]; then
    print_warning "Dependencies not found or incomplete. Installing..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies"
        deactivate
        exit 1
    fi
    print_info "Dependencies installed successfully"
else
    print_info "All dependencies are already installed"
fi

# Check if configuration exists
if [ ! -f ".env" ] && [ ! -f "config.yaml" ]; then
    print_warning "No configuration file found (.env or config.yaml)"
    print_warning "Please create a .env file or config.yaml with your YouTube API key and channel info"
    print_warning "See config.yaml.example for reference"
fi

# Run the Python script with all passed arguments
print_info "Running get_latest_live.py..."
echo ""

python3 get_latest_live.py "$@"
EXIT_CODE=$?

echo ""

# Deactivate virtual environment
deactivate

if [ $EXIT_CODE -eq 0 ]; then
    print_info "Script completed successfully"
else
    print_error "Script exited with error code $EXIT_CODE"
fi

exit $EXIT_CODE

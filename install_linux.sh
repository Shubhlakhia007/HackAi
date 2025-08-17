#!/bin/bash
# HackAI Linux Installation Script
# Automatically detects system, installs dependencies, and sets up HackAI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        print_warning "Please run as a regular user with sudo privileges"
        exit 1
    fi
}

# Detect Linux distribution
detect_distro() {
    print_status "Detecting Linux distribution..."
    
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
        print_status "Detected: $NAME $VERSION"
    else
        print_error "Could not detect Linux distribution"
        exit 1
    fi
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python version: $PYTHON_VERSION"
        
        # Check if Python 3.8+
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
            print_error "Python 3.8+ is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python3 is not installed"
        exit 1
    fi
    
    # Check RAM
    TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    print_status "Total RAM: ${TOTAL_RAM}GB"
    
    if [[ $TOTAL_RAM -lt 8 ]]; then
        print_warning "Less than 8GB RAM detected. Performance may be limited."
    fi
    
    # Check disk space
    FREE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    print_status "Free disk space: ${FREE_SPACE}GB"
    
    if [[ $FREE_SPACE -lt 10 ]]; then
        print_error "Less than 10GB free space. Need at least 10GB for installation."
        exit 1
    fi
    
    # Check CPU cores
    CPU_CORES=$(nproc)
    print_status "CPU cores: $CPU_CORES"
}

# Install system dependencies based on distribution
install_system_deps() {
    print_status "Installing system dependencies..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"linuxmint")
            print_status "Using apt package manager..."
            sudo apt update
            sudo apt install -y \
                python3-pip \
                python3-venv \
                git \
                curl \
                wget \
                build-essential \
                nmap \
                wireshark \
                binwalk \
                exiftool \
                steghide \
                john \
                hashcat \
                sqlmap \
                nikto \
                dirb \
                gobuster \
                hydra \
                aircrack-ng \
                tcpdump \
                netcat \
                net-tools \
                htop \
                tree
            ;;
        "centos"|"rhel"|"fedora"|"rocky"|"alma")
            print_status "Using dnf/yum package manager..."
            if command -v dnf &> /dev/null; then
                sudo dnf update -y
                sudo dnf install -y \
                    python3-pip \
                    python3-venv \
                    git \
                    curl \
                    wget \
                    gcc \
                    gcc-c++ \
                    make \
                    nmap \
                    wireshark \
                    binwalk \
                    exiftool \
                    steghide \
                    john \
                    hashcat \
                    sqlmap \
                    nikto \
                    dirb \
                    gobuster \
                    hydra \
                    aircrack-ng \
                    tcpdump \
                    nc \
                    net-tools \
                    htop \
                    tree
            else
                sudo yum update -y
                sudo yum install -y \
                    python3-pip \
                    python3-venv \
                    git \
                    curl \
                    wget \
                    gcc \
                    gcc-c++ \
                    make \
                    nmap \
                    wireshark \
                    binwalk \
                    exiftool \
                    steghide \
                    john \
                    hashcat \
                    sqlmap \
                    nikto \
                    dirb \
                    gobuster \
                    hydra \
                    aircrack-ng \
                    tcpdump \
                    nc \
                    net-tools \
                    htop \
                    tree
            fi
            ;;
        "arch"|"manjaro")
            print_status "Using pacman package manager..."
            sudo pacman -Sy --noconfirm \
                python-pip \
                python-virtualenv \
                git \
                curl \
                wget \
                base-devel \
                nmap \
                wireshark-qt \
                binwalk \
                exiftool \
                steghide \
                john \
                hashcat \
                sqlmap \
                nikto \
                dirb \
                gobuster \
                hydra \
                aircrack-ng \
                tcpdump \
                netcat \
                net-tools \
                htop \
                tree
            ;;
        *)
            print_error "Unsupported distribution: $DISTRO"
            print_warning "Please install dependencies manually"
            ;;
    esac
}

# Detect existing LLM models
detect_existing_models() {
    print_status "Scanning for existing LLM models..."
    
    COMMON_PATHS=(
        "models/cache"
        "$HOME/.cache/huggingface"
        "$HOME/.local/share/huggingface"
        "/usr/local/share/huggingface"
        "/opt/huggingface"
    )
    
    FOUND_MODELS=()
    
    for path in "${COMMON_PATHS[@]}"; do
        if [[ -d "$path" ]]; then
            print_status "Scanning: $path"
            for item in "$path"/*; do
                if [[ -d "$item" ]]; then
                    # Check if it looks like a model directory
                    if [[ "$item" =~ (phi|mistral|llama|gpt|bert) ]]; then
                        MODEL_NAME=$(basename "$item")
                        MODEL_SIZE=$(du -sh "$item" 2>/dev/null | cut -f1)
                        FOUND_MODELS+=("$item|$MODEL_NAME|$MODEL_SIZE")
                        print_status "Found: $MODEL_NAME ($MODEL_SIZE)"
                    fi
                fi
            done
        fi
    done
    
    if [[ ${#FOUND_MODELS[@]} -gt 0 ]]; then
        print_status "Found ${#FOUND_MODELS[@]} existing model(s)"
        echo
        echo "Existing models:"
        for model in "${FOUND_MODELS[@]}"; do
            IFS='|' read -r path name size <<< "$model"
            echo "  • $name ($size) at $path"
        done
        echo
        
        read -p "Use existing model? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Use the first found model
            IFS='|' read -r path name size <<< "${FOUND_MODELS[0]}"
            EXISTING_MODEL_PATH="$path"
            EXISTING_MODEL_NAME="$name"
            print_status "Using existing model: $name"
            return 0
        fi
    fi
    
    return 1
}

# Setup Python environment
setup_python_env() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment
    python3 -m venv hackai_env
    source hackai_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_status "Python environment setup complete"
}

# Setup project directories
setup_directories() {
    print_status "Setting up project directories..."
    
    mkdir -p models/cache
    mkdir -p models/configs
    mkdir -p data/llm_cache
    mkdir -p reports
    mkdir -p logs
    
    print_status "Directories created successfully"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    cat > .env << EOF
# HackAI Environment Configuration
HACKAI_ROOT=.
TRANSFORMERS_CACHE=models/cache
HF_HOME=models/cache
TORCH_HOME=models/cache
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
OMP_NUM_THREADS=8

# Optional: Add your API keys here
# GEMINI_API_KEY=your_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
EOF
    
    print_status "Environment file created: .env"
}

# Setup LLM model
setup_llm() {
    print_status "Setting up LLM model..."
    
    if [[ -n "$EXISTING_MODEL_PATH" ]]; then
        print_status "Using existing model: $EXISTING_MODEL_NAME"
        # Create symlink to existing model
        ln -sf "$EXISTING_MODEL_PATH" "models/cache/$EXISTING_MODEL_NAME"
    else
        print_status "Downloading new model..."
        python3 setup_llm.py
    fi
}

# Create launch script
create_launch_script() {
    print_status "Creating launch script..."
    
    cat > launch.sh << 'EOF'
#!/bin/bash
echo "🚀 HackAI - Advanced Security Testing Framework"
echo "================================================"
echo "🤖 LLM Support: Enabled"
echo "🔧 Tools: 200+ Security Tools"
echo "📊 Reports: JSON, TXT, HTML"
echo "================================================"

# Activate virtual environment
if [[ -d "hackai_env" ]]; then
    source hackai_env/bin/activate
fi

# Set environment variables
export HACKAI_ROOT=.
export TRANSFORMERS_CACHE=models/cache
export HF_HOME=models/cache
export TORCH_HOME=models/cache
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export OMP_NUM_THREADS=8

# Check if models are available
if [ -d "models/cache" ] && [ "$(ls -A models/cache)" ]; then
    echo "✅ Local models found"
    export HACKAI_MODELS_PATH="models"
else
    echo "⚠️  No local models found. Will download on first use."
fi

# Run HackAI
python3 run_interactive.py
EOF
    
    chmod +x launch.sh
    print_status "Launch script created: launch.sh"
}

# Run tests
run_tests() {
    print_status "Running setup tests..."
    
    if python3 test_local_setup.py; then
        print_status "All tests passed!"
    else
        print_warning "Some tests failed. Check the output above."
    fi
}

# Main installation function
main() {
    print_header "HackAI Linux Installation"
    print_status "Starting installation process..."
    
    # Check if not running as root
    check_root
    
    # Detect distribution
    detect_distro
    
    # Check requirements
    check_requirements
    
    # Install system dependencies
    install_system_deps
    
    # Setup Python environment
    setup_python_env
    
    # Setup directories
    setup_directories
    
    # Setup environment variables
    setup_environment
    
    # Detect existing models
    if detect_existing_models; then
        print_status "Using existing model"
    fi
    
    # Setup LLM
    setup_llm
    
    # Create launch script
    create_launch_script
    
    # Run tests
    run_tests
    
    print_header "Installation Complete!"
    print_status "HackAI has been successfully installed!"
    echo
    print_status "To start HackAI:"
    echo "  ./launch.sh"
    echo "  or"
    echo "  python3 run_interactive.py"
    echo
    print_status "To get help:"
    echo "  python3 ai_assistant.py"
    echo "  or"
    echo "  python3 run_interactive.py"
    echo "  Then type: ai help me"
    echo
    print_status "To test your setup:"
    echo "  python3 test_local_setup.py"
    echo
    print_status "Happy Hacking! 🚀"
}

# Run main function
main "$@"

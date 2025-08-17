# 🚀 HackAI Local Setup Guide

## 🎯 Quick Start (No Docker Required)

HackAI is now optimized for local installation with pre-configured LLM models and security tools.

### Prerequisites

- **Python 3.8+** 
- **8GB+ RAM** (12GB+ recommended for optimal LLM performance)
- **10GB+ free disk space** for models and tools
- **Windows/Linux/macOS** supported

### 🚀 One-Click Installation

```bash
# Clone the repository
git clone <repository-url>
cd hackingAI

# Run the local installation script
python install_local.py

# Setup the LLM model
python setup_llm.py

# Start HackAI
python run_interactive.py
```

## 📋 System Requirements

### Minimum Requirements
- **RAM**: 8GB (6GB for LLM + 2GB for system)
- **Storage**: 10GB free space
- **CPU**: 4 cores (2.4GHz+)
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.15+

### Recommended Requirements
- **RAM**: 12GB+ (8GB for LLM + 4GB for system)
- **Storage**: 20GB+ free space
- **CPU**: 8 cores (3.0GHz+)
- **GPU**: NVIDIA RTX 3060+ (optional, for accelerated inference)

## 🔧 Installation Options

### Option 1: Automated Installation (Recommended)

```bash
# Run the complete setup
python install_local.py
```

This script will:
- ✅ Check system requirements
- ✅ Install Python dependencies
- ✅ Install system security tools
- ✅ Setup directories and environment
- ✅ Create launch scripts

### Option 2: Manual Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install system tools (see platform-specific instructions below)
# 3. Setup directories
mkdir -p models/cache data/llm_cache reports logs

# 4. Setup environment
python setup_llm.py
```

## 🛠️ Platform-Specific Setup

### Windows Setup

```powershell
# Install Chocolatey (if not already installed)
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required tools
choco install nmap wireshark git python3 -y

# Run HackAI setup
python install_local.py
```

### Linux Setup (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install required tools
sudo apt install -y nmap wireshark git python3 python3-pip binwalk exiftool steghide john hashcat

# Run HackAI setup
python3 install_local.py
```

### macOS Setup

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install nmap wireshark git python3 binwalk exiftool steghide john hashcat

# Run HackAI setup
python3 install_local.py
```

## 🤖 LLM Model Management

### Current Model: Microsoft Phi-2

**Specifications:**
- **Model**: `microsoft/phi-2`
- **Parameters**: 2.7B
- **Context Window**: 2,048 tokens
- **Memory Usage**: ~1.5GB RAM
- **Inference Speed**: Fast
- **Quality**: Good reasoning, security-aware

**Location**: `models/cache/models--microsoft--phi-2/`

### Model Selection

The system automatically selects the best model based on your hardware:

| RAM | Recommended Model | Performance |
|-----|------------------|-------------|
| <8GB | Phi-2 (current) | Balanced |
| 8-12GB | Phi-2 or Mistral 7B | Good |
| 12GB+ | Mistral 7B | Best |

### Switching Models

```bash
# Run the LLM setup script
python setup_llm.py

# The script will analyze your system and recommend the best model
```

## 🚀 Usage

### Starting HackAI

```bash
# Method 1: Direct execution
python run_interactive.py

# Method 2: Using launch script
./launch.sh  # Linux/macOS
launch.bat   # Windows

# Method 3: With environment variables
source local_env.sh && python3 run_interactive.py
```

### Basic Commands

```bash
# AI-guided security scan
scan example.com

# CTF file analysis
ctf mystery_file.zip

# Run specific tool
run nmap on example.com

# List available tools
tools

# Check system health
health

# View scan reports
reports
```

## 🛠️ Security Tools Included

### Network Security
- **nmap** - Network discovery and port scanning
- **masscan** - Fast port scanner
- **rustscan** - Ultra-fast port scanner
- **wireshark** - Packet analysis

### Web Security
- **nuclei** - Vulnerability scanner
- **sqlmap** - SQL injection testing
- **nikto** - Web vulnerability scanner
- **gobuster** - Directory enumeration
- **dirb** - Web content scanner

### Password Security
- **hydra** - Password brute forcing
- **john** - Password cracking
- **hashcat** - Advanced hash cracking

### Forensics & CTF
- **binwalk** - Firmware analysis
- **exiftool** - Metadata extraction
- **steghide** - Steganography
- **strings** - String extraction
- **xxd** - Hex dump utility

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# HackAI Environment Configuration
HACKAI_ROOT=.
TRANSFORMERS_CACHE=models/cache
HF_HOME=models/cache
TORCH_HOME=models/cache
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
OMP_NUM_THREADS=8

# Optional: Add your API keys here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Configuration

The model configuration is stored in `models/config.json`:

```json
{
  "best_model": {
    "name": "Microsoft Phi-2",
    "model_id": "microsoft/phi-2",
    "size": "2.7B",
    "cache_dir": "models/cache",
    "optimizations": {
      "quantization": "4-bit (nf4)",
      "double_quantization": true,
      "torch_dtype": "float16",
      "device_map": "auto",
      "low_cpu_mem_usage": true
    }
  }
}
```

## 📊 Performance Optimization

### Memory Management

- **4-bit quantization** enabled by default
- **Double quantization** for optimal memory usage
- **Float16 precision** for faster inference
- **Auto device mapping** for optimal resource usage

### CPU Optimization

- **Multi-threading** enabled (8 threads by default)
- **Memory chunking** for large models
- **Low CPU memory usage** mode

### GPU Acceleration (Optional)

If you have an NVIDIA GPU:

```bash
# Install CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# The system will automatically detect and use your GPU
```

## 🔍 Troubleshooting

### Common Issues

1. **Out of Memory**
   ```bash
   # Reduce model size or increase system RAM
   # Check available memory
   python -c "import psutil; print(f'{psutil.virtual_memory().available / 1024**3:.1f} GB available')"
   ```

2. **Model Download Fails**
   ```bash
   # Check internet connection
   ping google.com
   
   # Clear model cache
   rm -rf models/cache/*
   ```

3. **Permission Issues**
   ```bash
   # Fix permissions (Linux/macOS)
   chmod +x launch.sh
   chmod +x local_env.sh
   ```

4. **Python Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Performance Tips

1. **Use SSD storage** for faster model loading
2. **Close unnecessary applications** to free RAM
3. **Monitor memory usage** with Task Manager/htop
4. **Use appropriate model** for your hardware
5. **Enable GPU acceleration** if available

### Logs and Debugging

```bash
# View application logs
tail -f logs/hackai.log

# Check Python environment
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Test model loading
python -c "from transformers import AutoTokenizer; tokenizer = AutoTokenizer.from_pretrained('microsoft/phi-2'); print('Model loaded successfully')"
```

## 🔒 Security Considerations

### Ethical Usage
- **Authorization required** for all testing
- **Legal compliance** with local regulations
- **Responsible disclosure** of vulnerabilities
- **Educational use** only without permission

### Data Privacy
- **Local processing** - no data sent to external APIs
- **Encrypted storage** for sensitive data
- **Audit logging** for all activities
- **Data retention** policies

## 📚 Additional Resources

### Documentation
- [Main README](./README.md) - Complete project documentation
- [LLM Recommendations](./llm_recommendations.md) - AI model guide
- [Docker Setup](./README-Docker.md) - Docker deployment guide

### Community
- **GitHub Issues** - Bug reports and feature requests
- **Discord Server** - Community discussions
- **Security Forums** - Professional discussions

### Updates
```bash
# Update to latest version
git pull origin main

# Reinstall dependencies if needed
pip install -r requirements.txt --upgrade

# Update models if needed
python setup_llm.py
```

---

**🚀 Happy Hacking with HackAI!**

*Remember: Always ensure you have proper authorization before testing any systems.*

# 🪟 HackAI Windows Setup Guide

## 🎯 Current Status

**Your System**: Windows 10/11 with Python 3.11
**Current LLM**: LocalAIProvider (rule-based, offline mode)
**Model Status**: Microsoft Phi-2 downloaded but not loaded
**Performance**: Basic rule-based analysis (no AI inference)

## 🚀 Quick Start Options

### Option 1: Docker (Recommended for Full LLM Support)

#### Install Docker Desktop for Windows

1. **Download Docker Desktop**:
   - Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
   - Download and install Docker Desktop

2. **System Requirements**:
   - Windows 10/11 Pro, Enterprise, or Education (64-bit)
   - WSL 2 enabled
   - Virtualization enabled in BIOS

3. **Install WSL 2** (if not already installed):
   ```powershell
   # Run as Administrator
   wsl --install
   ```

4. **Start Docker Desktop** and wait for it to be ready

#### Run HackAI with Docker

```powershell
# Navigate to project directory
cd D:\hackingAI

# Start HackAI with Docker
docker-compose up -d

# Access the interactive CLI
docker-compose exec hackai python3 run_interactive.py
```

### Option 2: Native Windows Setup (Limited LLM Support)

#### Install Python Dependencies

```powershell
# Install required packages
pip install -r requirements.txt

# Install additional Windows-specific packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate sentence-transformers
```

#### Setup LLM Models

```powershell
# Download and setup LLM models
python setup_llm.py

# Run HackAI
python run_interactive.py
```

## 🤖 LLM Configuration

### Current Model: Microsoft Phi-2

**Location**: `models/cache/models--microsoft--phi-2/`
**Status**: Downloaded but not loaded in current session
**Size**: ~2.7B parameters
**Memory Usage**: ~2GB RAM when loaded

### Model Loading Issues on Windows

The current setup has some limitations on Windows:

1. **Transformers Library**: May have compatibility issues
2. **Memory Management**: Windows memory handling differs from Linux
3. **CUDA Support**: Requires specific Windows CUDA installation

### Recommended Solutions

#### For Full LLM Support (Docker)
```powershell
# Use Docker for consistent Linux environment
docker-compose up -d
docker-compose exec hackai python3 run_interactive.py
```

#### For Native Windows (Limited)
```powershell
# Use rule-based analysis (current mode)
python run_interactive.py

# Or try loading models manually
python -c "
import sys
sys.path.insert(0, 'src')
from ai.local_llm import LocalLLMProvider
provider = LocalLLMProvider('microsoft/phi-2')
print(f'Model loaded: {provider.available}')
"
```

## 🔧 Windows-Specific Configuration

### Environment Variables

```powershell
# Set environment variables for Windows
$env:TRANSFORMERS_CACHE = "D:\hackingAI\models\cache"
$env:HF_HOME = "D:\hackingAI\models\cache"
$env:TORCH_HOME = "D:\hackingAI\models\cache"
$env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:512"
$env:OMP_NUM_THREADS = "8"
```

### PowerShell Profile Setup

Add to your PowerShell profile (`$PROFILE`):

```powershell
# HackAI Environment Setup
function Set-HackAIEnv {
    $env:TRANSFORMERS_CACHE = "D:\hackingAI\models\cache"
    $env:HF_HOME = "D:\hackingAI\models\cache"
    $env:TORCH_HOME = "D:\hackingAI\models\cache"
    $env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:512"
    $env:OMP_NUM_THREADS = "8"
    Write-Host "HackAI environment variables set" -ForegroundColor Green
}

# Quick HackAI launch
function Start-HackAI {
    Set-HackAIEnv
    python run_interactive.py
}
```

## 🛠️ Security Tools on Windows

### Available Tools

Most security tools are designed for Linux. On Windows, you have these options:

#### Docker (Recommended)
- All tools available in Linux container
- Full functionality
- Consistent environment

#### Windows Native (Limited)
- **nmap**: Available via Windows installer
- **sqlmap**: Python-based, works on Windows
- **nikto**: Perl-based, requires WSL or Cygwin
- **gobuster**: Go-based, Windows binaries available

### Installing Windows Tools

```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install security tools
choco install nmap
choco install sqlmap
choco install gobuster
```

## 📊 Performance Comparison

| Setup | LLM Support | Tool Availability | Performance | Ease of Use |
|-------|-------------|-------------------|-------------|-------------|
| **Docker** | ✅ Full | ✅ All Tools | ✅ Excellent | ⭐⭐⭐⭐⭐ |
| **Windows Native** | ⚠️ Limited | ⚠️ Partial | ⚠️ Good | ⭐⭐⭐ |
| **WSL2** | ✅ Full | ✅ All Tools | ✅ Excellent | ⭐⭐⭐⭐ |

## 🔍 Troubleshooting

### Common Windows Issues

1. **Docker Not Starting**
   ```powershell
   # Check WSL 2 status
   wsl --status
   
   # Restart Docker Desktop
   # Enable virtualization in BIOS
   ```

2. **Model Loading Fails**
   ```powershell
   # Clear model cache
   Remove-Item -Recurse -Force models\cache\*
   
   # Reinstall transformers
   pip uninstall transformers torch
   pip install transformers torch --no-cache-dir
   ```

3. **Permission Issues**
   ```powershell
   # Run PowerShell as Administrator
   # Or fix permissions
   icacls . /grant Everyone:F /T
   ```

4. **Memory Issues**
   ```powershell
   # Increase page file size
   # Close unnecessary applications
   # Use smaller model (Phi-2 instead of Mistral)
   ```

### Performance Optimization

1. **Use SSD Storage**: Move project to SSD for faster model loading
2. **Close Background Apps**: Free up RAM for LLM inference
3. **Use Docker**: Consistent Linux environment
4. **Enable GPU**: Install CUDA for Windows if you have NVIDIA GPU

## 🚀 Quick Commands

### Docker Setup
```powershell
# Install Docker Desktop first, then:
docker-compose up -d
docker-compose exec hackai python3 run_interactive.py
```

### Native Windows
```powershell
# Set environment and run
Set-HackAIEnv
python run_interactive.py
```

### Check Status
```powershell
# Check Docker status
docker-compose ps

# Check model status
ls models/cache/

# Check Python environment
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
```

## 📚 Additional Resources

### Windows-Specific
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows/)
- [WSL 2 Installation](https://docs.microsoft.com/en-us/windows/wsl/install)
- [Windows Security Tools](https://github.com/awesome-windows/awesome-windows)

### HackAI Documentation
- [Main README](./README.md) - Complete project documentation
- [Docker README](./README-Docker.md) - Docker-specific guide
- [LLM Recommendations](./llm_recommendations.md) - AI model guide

## 🎯 Recommendations

### For Best Experience
1. **Use Docker**: Full Linux environment with all tools
2. **16GB+ RAM**: For optimal LLM performance
3. **SSD Storage**: Faster model loading
4. **NVIDIA GPU**: For accelerated inference (optional)

### For Development
1. **Native Windows**: For quick testing and development
2. **WSL2**: Alternative to Docker for Linux tools
3. **Hybrid Approach**: Use Docker for production, native for development

---

**🚀 Happy Hacking with HackAI on Windows!**

*Remember: Always ensure you have proper authorization before testing any systems.*

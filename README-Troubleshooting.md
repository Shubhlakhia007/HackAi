# 🔧 HackAI Troubleshooting Guide

## 🚨 Quick Fix Commands

### Test Your Setup
```bash
# Run comprehensive setup test
python test_local_setup.py

# Get AI help for any issue
ai help me fix [your problem]

# Check system health
python run_interactive.py
# Then type: health
```

### Common Quick Fixes
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear and reinstall models
rm -rf models/cache/* && python setup_llm.py

# Fix permissions (Linux/macOS)
chmod +x launch.sh local_env.sh

# Reset environment
rm -f .env && python install_local.py
```

## 🔍 Common Issues & Solutions

### 1. Out of Memory Errors

**Symptoms:**
- `RuntimeError: CUDA out of memory`
- `torch.cuda.OutOfMemoryError`
- `insufficient memory`
- System becomes unresponsive

**Quick Solutions:**
```bash
# Get AI help
ai I'm getting out of memory errors

# Check available memory
python -c "import psutil; print(f'{psutil.virtual_memory().available / 1024**3:.1f} GB available')"

# Close other applications and try again
# Use smaller model
python setup_llm.py  # Choose Phi-2 instead of Mistral 7B
```

**Detailed Solutions:**
1. **Close unnecessary applications** (browsers, IDEs, etc.)
2. **Use smaller model**: Phi-2 (1.5GB) instead of Mistral 7B (4GB)
3. **Enable swap space** on Linux:
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```
4. **Reduce batch size** in model configuration
5. **Use CPU-only mode** if GPU memory is insufficient

### 2. Model Download Fails

**Symptoms:**
- `ConnectionError: Failed to establish a new connection`
- `HTTPError: 404 Client Error`
- `Download failed`
- `Model not found`

**Quick Solutions:**
```bash
# Get AI help
ai model download is failing

# Check internet connection
ping google.com

# Clear cache and retry
rm -rf models/cache/*
python setup_llm.py
```

**Detailed Solutions:**
1. **Check internet connection**:
   ```bash
   ping google.com
   curl -I https://huggingface.co
   ```
2. **Use VPN** if behind corporate firewall
3. **Check disk space**:
   ```bash
   df -h
   # Need at least 10GB free space
   ```
4. **Try different model**:
   ```bash
   # Edit setup_llm.py to use different model
   # Or manually download
   ```
5. **Use mirror/repository** if HuggingFace is blocked

### 3. Permission Errors

**Symptoms:**
- `Permission denied`
- `access denied`
- `chmod: cannot access`
- `Operation not permitted`

**Quick Solutions:**
```bash
# Get AI help
ai permission denied errors

# Fix script permissions (Linux/macOS)
chmod +x launch.sh local_env.sh

# Run as administrator (Windows)
# Right-click PowerShell -> Run as Administrator
```

**Detailed Solutions:**

**Linux/macOS:**
```bash
# Fix file permissions
chmod +x *.sh *.py
chmod +x launch.sh local_env.sh

# Fix directory permissions
chmod -R 755 models/ data/ reports/ logs/

# Use sudo for system-wide installations
sudo apt install -y nmap wireshark git python3
```

**Windows:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Chocolatey as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
```

### 4. Import Errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'torch'`
- `ImportError: cannot import name`
- `Module not found`

**Quick Solutions:**
```bash
# Get AI help
ai import error with [module name]

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+
```

**Detailed Solutions:**
1. **Install missing dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install torch transformers accelerate
   ```
2. **Use virtual environment**:
   ```bash
   python -m venv hackai_env
   source hackai_env/bin/activate  # Linux/macOS
   hackai_env\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. **Check Python version** (3.8+ required):
   ```bash
   python --version
   # If < 3.8, install newer Python
   ```
4. **Force reinstall**:
   ```bash
   pip install --force-reinstall --no-deps torch transformers
   ```

### 5. GPU Issues

**Symptoms:**
- `CUDA not available`
- `nvidia-smi: command not found`
- `torch.cuda.is_available() returns False`

**Quick Solutions:**
```bash
# Get AI help
ai GPU not detected

# Check GPU status
nvidia-smi

# Install CUDA PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Detailed Solutions:**

**Check GPU:**
```bash
# Check if NVIDIA GPU exists
lspci | grep -i nvidia

# Check NVIDIA drivers
nvidia-smi

# Check CUDA installation
nvcc --version
```

**Install NVIDIA drivers:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nvidia-driver-470

# CentOS/RHEL
sudo yum install nvidia-driver

# Restart system after installation
sudo reboot
```

**Install CUDA toolkit:**
```bash
# Download from NVIDIA website
# https://developer.nvidia.com/cuda-downloads

# Or use package manager
sudo apt install nvidia-cuda-toolkit
```

**Install PyTorch with CUDA:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 6. System Tool Issues

**Symptoms:**
- `nmap: command not found`
- `wireshark: command not found`
- `git: command not found`

**Quick Solutions:**
```bash
# Get AI help
ai system tools not found

# Install system tools
python install_local.py
```

**Detailed Solutions:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y nmap wireshark git python3 python3-pip binwalk exiftool steghide john hashcat
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install -y nmap wireshark git python3 python3-pip
sudo yum install -y epel-release
sudo yum install -y binwalk exiftool steghide john hashcat
```

**macOS:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tools
brew install nmap wireshark git python3 binwalk exiftool steghide john hashcat
```

**Windows:**
```powershell
# Install Chocolatey first
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install nmap wireshark git python3 -y
```

### 7. Python Environment Issues

**Symptoms:**
- `pip: command not found`
- `python: command not found`
- Wrong Python version

**Quick Solutions:**
```bash
# Get AI help
ai Python environment issues

# Check Python version
python --version
python3 --version

# Install pip
python -m ensurepip --upgrade
```

**Detailed Solutions:**

**Install Python 3.8+:**
```bash
# Linux
sudo apt install python3.8 python3.8-pip

# macOS
brew install python@3.8

# Windows
# Download from python.org
```

**Install pip:**
```bash
python -m ensurepip --upgrade
# or
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

**Use virtual environment:**
```bash
python -m venv hackai_env
source hackai_env/bin/activate  # Linux/macOS
hackai_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 8. Performance Issues

**Symptoms:**
- Slow model loading
- High memory usage
- Slow inference
- System lag

**Quick Solutions:**
```bash
# Get AI help
ai performance optimization

# Check system resources
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().total/1024**3:.1f}GB, CPU: {psutil.cpu_count()} cores')"

# Optimize model settings
python setup_llm.py
```

**Detailed Solutions:**

**Memory Optimization:**
1. **Use smaller model** (Phi-2 instead of Mistral 7B)
2. **Enable 4-bit quantization** (already enabled by default)
3. **Close unnecessary applications**
4. **Use SSD storage** for faster loading
5. **Enable swap space** on Linux

**CPU Optimization:**
1. **Use multi-threading** (already configured)
2. **Optimize batch size** for your CPU
3. **Use appropriate model** for your hardware
4. **Monitor CPU usage** with htop/task manager

**GPU Optimization:**
1. **Install CUDA drivers** and toolkit
2. **Use GPU-optimized PyTorch**
3. **Monitor GPU memory** with nvidia-smi
4. **Use mixed precision** (already enabled)

## 🧠 AI-Powered Troubleshooting

### Using the AI Assistant

The AI assistant can help with any issue:

```bash
# Start AI assistant
python ai_assistant.py

# Or use from main CLI
python run_interactive.py
# Then type: ai [your question]
```

### Example AI Commands

```bash
# Troubleshooting
ai I'm getting out of memory errors
ai model download is failing
ai permission denied errors
ai import error with torch
ai GPU not detected

# Tool help
ai how do I use nmap for port scanning
ai show me sqlmap examples
ai what tools should I use for web testing

# Configuration
ai how do I configure GPU acceleration
ai optimize performance for my system
ai install additional tools

# CTF help
ai how do I solve this crypto challenge
ai what tools for reverse engineering
ai help me analyze this binary file
```

## 📊 System Requirements Check

### Minimum Requirements
- **RAM**: 8GB (6GB for LLM + 2GB for system)
- **Storage**: 10GB free space
- **CPU**: 4 cores (2.4GHz+)
- **Python**: 3.8+

### Recommended Requirements
- **RAM**: 12GB+ (8GB for LLM + 4GB for system)
- **Storage**: 20GB+ free space
- **CPU**: 8 cores (3.0GHz+)
- **GPU**: NVIDIA RTX 3060+ (optional)

### Check Your System
```bash
# Run comprehensive check
python test_local_setup.py

# Manual checks
python --version
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().total/1024**3:.1f}GB')"
df -h
nproc  # CPU cores
```

## 🔄 Complete Reset

If everything is broken, start fresh:

```bash
# 1. Backup important data
cp -r data/ data_backup/
cp -r reports/ reports_backup/

# 2. Remove everything
rm -rf models/cache/*
rm -f .env
rm -f launch.sh launch.bat

# 3. Reinstall
python install_local.py
python setup_llm.py

# 4. Test
python test_local_setup.py
```

## 📞 Getting Help

### AI Assistant
```bash
# Best option - AI can help with any issue
python ai_assistant.py
```

### Documentation
- **Main README**: Complete project documentation
- **Local Setup**: README-Local.md - Detailed installation guide
- **LLM Guide**: llm_recommendations.md - AI model guide

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discord Server**: Community discussions
- **Security Forums**: Professional discussions

### Logs and Debugging
```bash
# View application logs
tail -f logs/hackai.log

# Check Python environment
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Test model loading
python -c "from transformers import AutoTokenizer; print('Model loading test')"
```

---

**💡 Pro Tip**: The AI assistant is your best friend for troubleshooting. It can diagnose issues, provide step-by-step solutions, and even generate code examples for your specific problem!

**🚀 Happy Hacking with HackAI!**

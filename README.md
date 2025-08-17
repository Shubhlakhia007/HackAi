# 🚀 HackAI - Advanced Security Testing Framework

HackAI is a comprehensive security testing framework with AI-powered analysis, 200+ security tools, and intelligent CTF challenge solving.

## 🌟 Features

- **🤖 AI-Powered Analysis**: Local LLM support (Phi-2, Mistral 7B, CodeLlama)
- **🔧 200+ Security Tools**: Network, web, forensic, crypto, reverse engineering
- **🎮 Smart CTF Analysis**: Automated challenge detection and tool recommendations
- **📊 Advanced Reporting**: JSON, TXT, HTML export formats
- **🏠 Local Installation**: No Docker required, runs natively on your system
- **🧠 AI Troubleshooting**: Built-in AI assistant for solving issues
- **🔍 Auto-Detection**: Automatically finds and configures LLM models
- **💬 AI CLI Chat**: Interactive AI assistant for questions and solutions

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)
```bash
# Run the complete setup script
python install_local.py

# Setup the LLM model (auto-detection enabled)
python setup_llm.py

# Start HackAI
python run_interactive.py
```

### Option 2: Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Setup directories and environment
mkdir -p models/cache data/llm_cache reports logs

# Download best LLM for your system
python setup_llm.py

# Run HackAI
python run_interactive.py
```

### Option 3: Platform-Specific Setup
```bash
# Windows (PowerShell as Administrator)
choco install nmap wireshark git python3 -y
python install_local.py

# Linux (Ubuntu/Debian)
sudo apt install -y nmap wireshark git python3 python3-pip binwalk exiftool steghide john hashcat
python3 install_local.py

# macOS
brew install nmap wireshark git python3 binwalk exiftool steghide john hashcat
python3 install_local.py
```

## 🎮 Usage

### Basic Commands
```bash
# AI-guided security scan
scan example.com

# CTF challenge analysis
ctf mystery_file.zip

# Direct tool execution
nmap example.com

# View reports
reports

# Export results
export
```

### AI Assistant Commands
```bash
# Ask AI for help with any issue
ai help me fix this error

# Get troubleshooting solutions
ai troubleshoot memory issues

# Ask for code examples
ai show me how to use nmap

# Get security advice
ai what tools should I use for web testing

# Ask CTF questions
ai how do I solve this crypto challenge
```

### CTF Commands
```bash
# Smart CTF analysis
ctf challenge_file.zip

# Forensic analysis
forensic mystery_file.jpg

# Crypto analysis
crypto encrypted_file.bin

# Reverse engineering
reverse binary_file.exe
```

### System Commands
```bash
# View available tools
tools

# Check system health
health

# Install additional tools
install nmap nuclei

# Test your setup
test
```

## 🤖 AI Models

### Available Models
- **Phi-2** (2.7B) - Lightweight, fast, good for development
- **Mistral 7B** (7B) - Excellent reasoning, production-ready
- **CodeLlama 7B** (7B) - Specialized for code analysis and CTF

### Auto-Detection Features
The system automatically:
- **Detects existing models** in common locations
- **Recommends optimal models** for your hardware
- **Downloads missing models** with one command
- **Configures optimizations** automatically
- **Tests model functionality** before use

### Model Selection
The system automatically selects the best model for your hardware:
- **16GB+ RAM**: Mistral 7B (best quality)
- **12-16GB RAM**: Phi-2 (balanced)
- **<12GB RAM**: Phi-2 (optimized)

## 🔧 Tool Categories

### Network Security
- nmap, masscan, rustscan, zmap
- wireshark, tcpdump, tshark
- aircrack-ng, kismet, wifite

### Web Security
- nuclei, httpx, gobuster, feroxbuster
- sqlmap, nikto, wpscan, joomscan
- burpsuite, zap, w3af

### Forensics & CTF
- binwalk, foremost, scalpel
- steghide, exiftool, strings
- volatility, autopsy, sleuthkit

### Reverse Engineering
- ghidra, radare2, ida, cutter
- gdb, objdump, pwntools
- angr, unicorn, ropgadget

### Exploitation
- metasploit, cobaltstrike, empire
- mimikatz, bloodhound, crackmapexec
- linpeas, winpeas, powercat

## 📊 Reporting

### Export Formats
- **JSON**: Structured data export
- **TXT**: Human-readable reports
- **HTML**: Web-based reports

### Report Types
- **Scan Summary**: Overview of all scans
- **Target History**: Historical analysis
- **Tool Statistics**: Usage and success rates
- **Vulnerability Reports**: Detailed findings

## 🏠 Local Installation

### System Requirements
- **RAM**: 8GB+ (12GB+ recommended)
- **Storage**: 10GB+ free space
- **CPU**: 4+ cores (2.4GHz+)
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.15+

### Installation Features
- **Pre-installed Tools**: All security tools included
- **LLM Models**: Cached and optimized for your system
- **Local Processing**: No data sent to external APIs
- **Resource Optimization**: Automatically configured for your hardware
- **GPU Support**: Optional CUDA acceleration
- **Auto-Detection**: Finds existing models automatically

## 🧠 AI Troubleshooting

### Built-in AI Assistant
HackAI includes an intelligent troubleshooting assistant that can:
- **Diagnose issues** automatically
- **Provide step-by-step solutions**
- **Generate code examples**
- **Explain error messages**
- **Suggest optimizations**

### Usage Examples
```bash
# Get help with any error
ai I'm getting "out of memory" error

# Ask for configuration help
ai how do I configure GPU acceleration

# Get tool usage help
ai show me nmap examples for port scanning

# Troubleshoot installation
ai installation failed, help me fix it

# Get security advice
ai what's the best way to scan a web application
```

## 🔍 Auto-Detection Features

### LLM Detection
The system automatically searches for models in:
- `models/cache/` (local cache)
- `~/.cache/huggingface/` (HuggingFace cache)
- `~/.local/share/huggingface/` (user cache)
- `/usr/local/share/huggingface/` (system cache)

### Automatic Setup
When you run `setup_llm.py`, it will:
1. **Scan for existing models** in common locations
2. **Analyze your system** resources
3. **Recommend the best model** for your hardware
4. **Download missing components** automatically
5. **Configure optimizations** for your system
6. **Test the setup** to ensure everything works

## 🔒 Security & Ethics

- **Authorization Required**: Always ensure proper permissions
- **Legal Compliance**: Follow local laws and regulations
- **Responsible Disclosure**: Report vulnerabilities appropriately
- **Educational Use**: Designed for learning and research

## 📁 Project Structure

```
hackai/
├── src/                    # Core application code
├── models/                 # LLM models and cache
├── data/                   # Scan data and cache
├── reports/               # Generated reports
├── logs/                  # Application logs
├── run_interactive.py     # Main interactive CLI
├── setup_llm.py          # LLM setup script
├── install_local.py      # Local installation script
├── test_local_setup.py   # Setup verification script
├── ai_assistant.py       # AI troubleshooting assistant
├── launch.sh             # Linux/macOS launcher
├── launch.bat            # Windows launcher
└── requirements.txt      # Python dependencies
```

## 🛠️ Troubleshooting

### Quick Fix Commands
```bash
# Test your setup
python test_local_setup.py

# Get AI help for any issue
ai help me fix [your problem]

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear and reinstall models
rm -rf models/cache/* && python setup_llm.py

# Check system health
python run_interactive.py
# Then type: health
```

### Common Issues

1. **Out of Memory**
   ```bash
   # Get AI help
   ai I'm getting out of memory errors
   
   # Or check manually
   python -c "import psutil; print(f'{psutil.virtual_memory().available / 1024**3:.1f} GB available')"
   ```

2. **Model Download Fails**
   ```bash
   # Get AI help
   ai model download is failing
   
   # Or check manually
   ping google.com
   rm -rf models/cache/*
   python setup_llm.py
   ```

3. **Permission Issues**
   ```bash
   # Get AI help
   ai permission denied errors
   
   # Or fix manually
   chmod +x launch.sh
   chmod +x local_env.sh
   ```

4. **Import Errors**
   ```bash
   # Get AI help
   ai import error with [module name]
   
   # Or fix manually
   pip install -r requirements.txt --force-reinstall
   ```

### Performance Tips
- Use SSD storage for faster model loading
- Close unnecessary applications to free RAM
- Enable GPU support if available
- Use appropriate model for your hardware

## 🤝 Support

### AI-Powered Support
```bash
# Ask the AI assistant for help
ai [your question or problem]

# Examples:
ai how do I install on Ubuntu?
ai what's wrong with my setup?
ai show me nmap examples
ai help me solve this CTF challenge
```

### Documentation
- **Main README**: This file - Complete project documentation
- **Local Setup**: README-Local.md - Detailed local installation guide
- **LLM Guide**: llm_recommendations.md - AI model guide
- **Troubleshooting**: README-Troubleshooting.md - Common issues and solutions

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discord Server**: Community discussions
- **Security Forums**: Professional discussions

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems.

---

**Made with ❤️ for the security community**

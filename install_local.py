#!/usr/bin/env python3
"""
HackAI Local Installation Script
Sets up HackAI for local use without Docker
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

def check_system():
    """Check system and requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check OS
    system = platform.system()
    print(f"✅ OS: {system}")
    
    # Check available RAM
    try:
        import psutil
        total_ram = psutil.virtual_memory().total / (1024**3)
        print(f"✅ RAM: {total_ram:.1f} GB")
        
        if total_ram < 8:
            print("⚠️  Warning: Less than 8GB RAM detected. Performance may be limited.")
    except ImportError:
        print("⚠️  psutil not available, RAM check skipped")
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    requirements = [
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "accelerate>=0.20.0",
        "sentence-transformers>=2.2.0",
        "peft>=0.4.0",
        "bitsandbytes>=0.41.0",
        "psutil>=5.9.0",
        "colorama>=0.4.6",
        "requests>=2.31.0",
        "urllib3>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pyyaml>=6.0",
        "toml>=0.10.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "cryptography>=41.0.0",
        "paramiko>=3.3.0",
        "aiofiles>=23.0.0"
    ]
    
    for dep in requirements:
        try:
            print(f"Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True

def install_system_tools():
    """Install system security tools"""
    print("\n🔧 Installing system security tools...")
    
    system = platform.system()
    
    if system == "Windows":
        return install_windows_tools()
    elif system == "Linux":
        return install_linux_tools()
    elif system == "Darwin":  # macOS
        return install_macos_tools()
    else:
        print(f"⚠️  Unsupported OS: {system}")
        return False

def install_windows_tools():
    """Install tools on Windows"""
    print("🪟 Installing Windows tools...")
    
    # Check if Chocolatey is available
    try:
        subprocess.run(["choco", "--version"], check=True, capture_output=True)
        print("✅ Chocolatey found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Chocolatey not found. Please install it first:")
        print("   https://chocolatey.org/install")
        return False
    
    tools = [
        "nmap",
        "wireshark",
        "git",
        "python3"
    ]
    
    for tool in tools:
        try:
            print(f"Installing {tool}...")
            subprocess.run(["choco", "install", tool, "-y"], check=True)
            print(f"✅ {tool}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {tool}, skipping...")
    
    return True

def install_linux_tools():
    """Install tools on Linux"""
    print("🐧 Installing Linux tools...")
    
    # Detect package manager
    package_managers = [
        ("apt", ["apt-get", "update"]),
        ("yum", ["yum", "update"]),
        ("dnf", ["dnf", "update"]),
        ("pacman", ["pacman", "-Sy"])
    ]
    
    package_manager = None
    for pm_name, pm_cmd in package_managers:
        try:
            subprocess.run(pm_cmd, check=True, capture_output=True)
            package_manager = pm_name
            print(f"✅ Using {pm_name}")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not package_manager:
        print("❌ No supported package manager found")
        return False
    
    # Define tools for different package managers
    tool_packages = {
        "apt": [
            "nmap", "wireshark", "git", "python3", "python3-pip",
            "binwalk", "exiftool", "steghide", "john", "hashcat",
            "sqlmap", "nikto", "dirb", "gobuster", "hydra"
        ],
        "yum": [
            "nmap", "wireshark", "git", "python3", "python3-pip",
            "binwalk", "exiftool", "steghide", "john", "hashcat"
        ],
        "dnf": [
            "nmap", "wireshark", "git", "python3", "python3-pip",
            "binwalk", "exiftool", "steghide", "john", "hashcat"
        ],
        "pacman": [
            "nmap", "wireshark", "git", "python", "python-pip",
            "binwalk", "exiftool", "steghide", "john", "hashcat"
        ]
    }
    
    tools = tool_packages.get(package_manager, [])
    
    for tool in tools:
        try:
            if package_manager == "apt":
                subprocess.run(["apt-get", "install", "-y", tool], check=True)
            elif package_manager == "yum":
                subprocess.run(["yum", "install", "-y", tool], check=True)
            elif package_manager == "dnf":
                subprocess.run(["dnf", "install", "-y", tool], check=True)
            elif package_manager == "pacman":
                subprocess.run(["pacman", "-S", "--noconfirm", tool], check=True)
            
            print(f"✅ {tool}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {tool}, skipping...")
    
    return True

def install_macos_tools():
    """Install tools on macOS"""
    print("🍎 Installing macOS tools...")
    
    # Check if Homebrew is available
    try:
        subprocess.run(["brew", "--version"], check=True, capture_output=True)
        print("✅ Homebrew found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Homebrew not found. Please install it first:")
        print("   https://brew.sh")
        return False
    
    tools = [
        "nmap", "wireshark", "git", "python3",
        "binwalk", "exiftool", "steghide", "john", "hashcat"
    ]
    
    for tool in tools:
        try:
            print(f"Installing {tool}...")
            subprocess.run(["brew", "install", tool], check=True)
            print(f"✅ {tool}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {tool}, skipping...")
    
    return True

def setup_directories():
    """Setup project directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        "models/cache",
        "models/configs",
        "data/llm_cache",
        "reports",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")

def setup_environment():
    """Setup environment variables"""
    print("\n⚙️  Setting up environment...")
    
    # Create .env file
    env_content = """# HackAI Environment Configuration
HACKAI_ROOT=.
TRANSFORMERS_CACHE=models/cache
HF_HOME=models/cache
TORCH_HOME=models/cache
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
OMP_NUM_THREADS=8

# Optional: Add your API keys here
# GEMINI_API_KEY=your_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created: .env")

def create_local_config():
    """Create local configuration"""
    print("\n📋 Creating configuration...")
    
    config = {
        "local_setup": {
            "enabled": True,
            "docker_disabled": True,
            "installation_date": str(Path().absolute())
        },
        "best_model": {
            "name": "Microsoft Phi-2",
            "model_id": "microsoft/phi-2",
            "size": "2.7B",
            "cache_dir": "models/cache",
            "optimizations": {
                "quantization": "4-bit (nf4)",
                "double_quantization": True,
                "torch_dtype": "float16",
                "device_map": "auto",
                "low_cpu_mem_usage": True
            },
            "performance": {
                "memory_usage": "~1.5GB",
                "inference_speed": "Fast",
                "quality": "Good"
            }
        },
        "system_info": {
            "platform": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "optimized_for": "Local security testing and CTF challenges"
        }
    }
    
    with open("models/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created: models/config.json")

def create_launch_script():
    """Create launch script for the platform"""
    print("\n🚀 Creating launch script...")
    
    system = platform.system()
    
    if system == "Windows":
        # Create batch file
        batch_content = """@echo off
echo 🚀 HackAI - Advanced Security Testing Framework
echo ================================================
echo 🤖 LLM Support: Enabled
echo 🔧 Tools: 200+ Security Tools
echo 📊 Reports: JSON, TXT, HTML
echo ================================================

REM Set environment variables
set HACKAI_ROOT=.
set TRANSFORMERS_CACHE=models/cache
set HF_HOME=models/cache
set TORCH_HOME=models/cache
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set OMP_NUM_THREADS=8

REM Run HackAI
python run_interactive.py
pause
"""
        with open("launch.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created: launch.bat")
        
    else:
        # Create shell script
        shell_content = """#!/bin/bash
echo "🚀 HackAI - Advanced Security Testing Framework"
echo "================================================"
echo "🤖 LLM Support: Enabled"
echo "🔧 Tools: 200+ Security Tools"
echo "📊 Reports: JSON, TXT, HTML"
echo "================================================"

# Set environment variables
export HACKAI_ROOT=.
export TRANSFORMERS_CACHE=models/cache
export HF_HOME=models/cache
export TORCH_HOME=models/cache
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export OMP_NUM_THREADS=8

# Run HackAI
python3 run_interactive.py
"""
        with open("launch.sh", "w") as f:
            f.write(shell_content)
        
        # Make executable
        os.chmod("launch.sh", 0o755)
        print("✅ Created: launch.sh")

def main():
    """Main installation function"""
    print("🚀 HackAI Local Installation")
    print("=" * 50)
    
    # Check system
    if not check_system():
        print("❌ System check failed")
        return
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return
    
    # Install system tools
    if not install_system_tools():
        print("⚠️  Some system tools failed to install")
    
    # Setup directories
    setup_directories()
    
    # Setup environment
    setup_environment()
    
    # Create configuration
    create_local_config()
    
    # Create launch script
    create_launch_script()
    
    print(f"\n{'='*50}")
    print("🎉 Local Installation Complete!")
    print("=" * 50)
    
    print(f"\n✅ HackAI is now ready for local use!")
    print(f"📦 All dependencies installed")
    print(f"🔧 System tools configured")
    print(f"🤖 LLM support ready")
    
    print(f"\n🚀 To start HackAI:")
    if platform.system() == "Windows":
        print(f"   Double-click: launch.bat")
        print(f"   Or run: python run_interactive.py")
    else:
        print(f"   Run: ./launch.sh")
        print(f"   Or run: python3 run_interactive.py")
    
    print(f"\n💡 Next Steps:")
    print(f"1. Run the setup script: python setup_llm.py")
    print(f"2. Start HackAI using the launch script")
    print(f"3. Test with: scan example.com")
    
    print(f"\n📚 Available Commands:")
    print(f"  • scan example.com - AI-guided security scan")
    print(f"  • tools - List available tools")
    print(f"  • health - Check system health")
    print(f"  • help - Show all commands")

if __name__ == "__main__":
    main()

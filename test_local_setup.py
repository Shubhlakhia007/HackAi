#!/usr/bin/env python3
"""
HackAI Local Setup Test Script
Verifies that the local installation is working correctly
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def test_python_environment():
    """Test Python environment and dependencies"""
    print("🔍 Testing Python Environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Test key dependencies
    dependencies = [
        "torch", "transformers", "colorama", "requests", 
        "psutil", "numpy", "pandas", "rich"
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - missing")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing Directories...")
    
    directories = [
        "models/cache",
        "data/llm_cache", 
        "reports",
        "logs"
    ]
    
    missing_dirs = []
    for dir_path in directories:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - missing")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️  Missing directories: {', '.join(missing_dirs)}")
        print("Run: python install_local.py")
        return False
    
    return True

def test_system_tools():
    """Test if system security tools are available"""
    print("\n🔧 Testing System Tools...")
    
    # Common security tools
    tools = [
        "nmap", "git", "python3", "strings", "file"
    ]
    
    # Platform-specific tools
    system = platform.system()
    if system == "Linux":
        tools.extend(["binwalk", "exiftool", "steghide"])
    elif system == "Darwin":  # macOS
        tools.extend(["binwalk", "exiftool"])
    
    missing_tools = []
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {tool}")
            else:
                print(f"⚠️  {tool} - not working properly")
                missing_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ {tool} - not found")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n⚠️  Missing tools: {', '.join(missing_tools)}")
        print("Install system tools using your package manager")
        return False
    
    return True

def test_environment_variables():
    """Test environment configuration"""
    print("\n⚙️  Testing Environment Configuration...")
    
    # Check if .env file exists
    if Path(".env").exists():
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found")
    
    # Check key environment variables
    env_vars = [
        "HACKAI_ROOT",
        "TRANSFORMERS_CACHE", 
        "HF_HOME",
        "TORCH_HOME"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value}")
        else:
            print(f"⚠️  {var} - not set")
    
    return True

def test_launch_scripts():
    """Test if launch scripts exist"""
    print("\n🚀 Testing Launch Scripts...")
    
    system = platform.system()
    
    if system == "Windows":
        if Path("launch.bat").exists():
            print("✅ launch.bat found")
        else:
            print("❌ launch.bat missing")
    else:
        if Path("launch.sh").exists():
            print("✅ launch.sh found")
            # Check if executable
            if os.access("launch.sh", os.X_OK):
                print("✅ launch.sh is executable")
            else:
                print("⚠️  launch.sh is not executable")
        else:
            print("❌ launch.sh missing")
    
    return True

def test_basic_functionality():
    """Test basic HackAI functionality"""
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        # Test importing core modules
        sys.path.insert(0, str(Path("src")))
        
        from core.colors import Colors
        print("✅ Core modules import successfully")
        
        # Test color functionality
        test_color = Colors.colorize("Test", Colors.GREEN)
        print(f"✅ Color system working: {test_color}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 HackAI Local Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Directories", test_directories),
        ("System Tools", test_system_tools),
        ("Environment Configuration", test_environment_variables),
        ("Launch Scripts", test_launch_scripts),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! HackAI is ready to use.")
        print("\n🚀 To start HackAI:")
        if platform.system() == "Windows":
            print("   Double-click: launch.bat")
            print("   Or run: python run_interactive.py")
        else:
            print("   Run: ./launch.sh")
            print("   Or run: python3 run_interactive.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 To fix issues:")
        print("1. Run: python install_local.py")
        print("2. Install missing system tools")
        print("3. Run this test again")

if __name__ == "__main__":
    main()

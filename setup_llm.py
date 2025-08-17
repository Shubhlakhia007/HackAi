#!/usr/bin/env python3
"""
HackAI LLM Setup - Comprehensive Setup Script
Combines all LLM setup functionality into one organized script
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add src to Python path for Colors import
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from core.colors import Colors
except ImportError:
    # Fallback if Colors class is not available
    class Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        
        @staticmethod
        def colorize(text, color):
            return f"{color}{text}\033[0m"

def detect_existing_models():
    """Detect existing LLM models in common locations"""
    print("🔍 Scanning for existing models...")
    
    common_paths = [
        "models/cache",
        str(Path.home() / ".cache" / "huggingface"),
        str(Path.home() / ".local" / "share" / "huggingface"),
        "/usr/local/share/huggingface",
        "/opt/huggingface"
    ]
    
    found_models = []
    
    for path in common_paths:
        if Path(path).exists():
            print(f"  Scanning: {path}")
            try:
                # Look for model directories
                for item in Path(path).iterdir():
                    if item.is_dir():
                        # Check if it looks like a model directory
                        if any(keyword in item.name.lower() for keyword in ['phi', 'mistral', 'llama', 'gpt', 'bert']):
                            found_models.append({
                                'path': str(item),
                                'name': item.name,
                                'size': get_directory_size(item)
                            })
                            print(f"    ✅ Found: {item.name}")
            except Exception as e:
                print(f"    ⚠️  Error scanning {path}: {e}")
    
    return found_models

def get_directory_size(path):
    """Get directory size in GB"""
    try:
        total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        return total_size / (1024**3)
    except (OSError, PermissionError):
        return 0

def check_system_resources():
    """Check system resources and recommend best model"""
    print("🔍 Analyzing your system for optimal LLM...")
    
    try:
        import psutil
        
        # Check RAM
        total_ram = psutil.virtual_memory().total / (1024**3)
        available_ram = psutil.virtual_memory().available / (1024**3)
        
        print(f"📊 System Analysis:")
        print(f"  Total RAM: {total_ram:.1f} GB")
        print(f"  Available RAM: {available_ram:.1f} GB")
        
        # Check CPU
        cpu_count = psutil.cpu_count()
        print(f"  CPU Cores: {cpu_count}")
        
        # Check disk space
        disk_usage = psutil.disk_usage('.')
        free_space = disk_usage.free / (1024**3)
        print(f"  Free Disk Space: {free_space:.1f} GB")
        
        # Check for existing models
        existing_models = detect_existing_models()
        
        if existing_models:
            print(f"\n📦 Found {len(existing_models)} existing model(s):")
            for model in existing_models:
                print(f"  • {model['name']} ({model['size']:.1f} GB) at {model['path']}")
            
            # Ask user if they want to use existing model
            use_existing = input(f"\n{Colors.colorize('Use existing model? (y/n): ', Colors.YELLOW)}").strip().lower()
            if use_existing in ['y', 'yes']:
                # Use the first found model
                existing_model = existing_models[0]
                return {
                    "use_existing": True,
                    "existing_model": existing_model,
                    "recommended_model": existing_model['name'],
                    "model_name": existing_model['name'],
                    "model_size": f"{existing_model['size']:.1f}B",
                    "total_ram": total_ram,
                    "free_space": free_space
                }
        
        # Recommend best model based on resources
        if total_ram >= 16:
            recommended_model = "mistralai/Mistral-7B-Instruct-v0.2"
            model_name = "Mistral 7B"
            model_size = "7B"
            reasoning = "Excellent reasoning, production-ready, best for security tasks"
        elif total_ram >= 12:
            recommended_model = "microsoft/phi-2"
            model_name = "Microsoft Phi-2"
            model_size = "2.7B"
            reasoning = "Good balance of performance and resource usage"
        else:
            recommended_model = "microsoft/phi-2"
            model_name = "Microsoft Phi-2"
            model_size = "2.7B"
            reasoning = "Lightweight, optimized for limited resources"
        
        print(f"\n🎯 Recommended Model: {model_name}")
        print(f"  Size: {model_size}")
        print(f"  Model ID: {recommended_model}")
        print(f"  Reasoning: {reasoning}")
        
        return {
            "use_existing": False,
            "recommended_model": recommended_model,
            "model_name": model_name,
            "model_size": model_size,
            "total_ram": total_ram,
            "free_space": free_space
        }
        
    except ImportError:
        print("⚠️  psutil not available, using default recommendation")
        return {
            "use_existing": False,
            "recommended_model": "microsoft/phi-2",
            "model_name": "Microsoft Phi-2",
            "model_size": "2.7B",
            "total_ram": 15.4,
            "free_space": 50
        }

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    dependencies = [
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "accelerate>=0.20.0",
        "sentence-transformers>=2.2.0",
        "peft>=0.4.0",
        "bitsandbytes>=0.41.0",
        "psutil>=5.9.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep, "--break-system-packages"], 
                         check=True, capture_output=True)
            print(f"✅ {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True

def setup_directories():
    """Setup all necessary directories"""
    print("📁 Setting up directories...")
    
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

def download_model(model_info):
    """Download the recommended model with optimizations"""
    model_id = model_info["recommended_model"]
    model_name = model_info["model_name"]
    
    print(f"🚀 Downloading {model_name} (Optimized for your system)...")
    print(f"📥 Model: {model_id}")
    
    try:
        # Set environment variables for optimal performance
        os.environ['TRANSFORMERS_CACHE'] = 'models/cache'
        os.environ['HF_HOME'] = 'models/cache'
        os.environ['TORCH_HOME'] = 'models/cache'
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
        os.environ['OMP_NUM_THREADS'] = '8'
        
        # Import required libraries
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        
        print("📦 Loading transformers and torch...")
        
        # Configure quantization for optimal memory usage
        print("⚙️  Configuring 4-bit quantization for optimal performance...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        # Download tokenizer
        print(f"📥 Downloading tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            cache_dir='models/cache',
            trust_remote_code=True
        )
        
        # Download model with optimizations
        print(f"📥 Downloading {model_name} model (this may take several minutes)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            cache_dir='models/cache',
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        print(f"✅ {model_name} downloaded successfully!")
        
        # Test the model
        print("🧪 Testing model inference...")
        test_prompt = "Analyze this security challenge: I have a binary file to examine for a CTF. What tools should I use?"
        inputs = tokenizer(test_prompt, return_tensors="pt", max_length=512, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=200,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✅ Model test successful!")
        print(f"📝 Sample response: {response[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {model_name}: {e}")
        return False

def create_config(model_info):
    """Create configuration for the LLM"""
    print("⚙️  Creating configuration...")
    
    config = {
        "best_model": {
            "name": model_info["model_name"],
            "model_id": model_info["recommended_model"],
            "size": model_info["model_size"],
            "cache_dir": "models/cache",
            "optimizations": {
                "quantization": "4-bit (nf4)",
                "double_quantization": True,
                "torch_dtype": "float16",
                "device_map": "auto",
                "low_cpu_mem_usage": True
            },
            "performance": {
                "memory_usage": f"~{int(float(model_info['model_size'].replace('B', '')) * 0.5)}GB",
                "inference_speed": "Fast",
                "quality": "High"
            }
        },
        "system_info": {
            "total_ram": model_info["total_ram"],
            "free_space": model_info["free_space"],
            "optimized_for": "Security testing and CTF challenges"
        },
        "docker_settings": {
            "memory_limit": "12G",
            "memory_reservation": "8G",
            "environment_variables": [
                "PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512",
                "OMP_NUM_THREADS=8",
                "TRANSFORMERS_CACHE=/app/models/cache"
            ]
        }
    }
    
    with open("models/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration created: models/config.json")

def setup_local_environment():
    """Setup local environment configuration"""
    print("⚙️  Setting up local environment...")
    
    # Create optimized local environment file
    env_content = """# HackAI Local Environment Configuration
# Set optimal environment variables for local use
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export OMP_NUM_THREADS=8
export TRANSFORMERS_CACHE=models/cache
export HF_HOME=models/cache
export TORCH_HOME=models/cache
export HACKAI_ROOT=.

# Check if models are available
if [ -d "models/cache" ] && [ "$(ls -A models/cache)" ]; then
    echo "✅ Local models found"
    export HACKAI_MODELS_PATH="models"
else
    echo "⚠️  No local models found. Will download on first use."
fi
"""
    
    with open("local_env.sh", "w") as f:
        f.write(env_content)
    
    os.chmod("local_env.sh", 0o755)
    print("✅ Local environment script created: local_env.sh")

def main():
    """Main setup function"""
    print("🚀 HackAI LLM Setup")
    print("=" * 50)
    
    # Check system resources
    model_info = check_system_resources()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Setup directories
    setup_directories()
    
    # Download model
    success = download_model(model_info)
    
    if success:
        # Create configuration
        create_config(model_info)
        
        # Setup local environment
        setup_local_environment()
        
        print(f"\n{'='*50}")
        print("🎉 LLM Setup Complete!")
        print("=" * 50)
        
        print(f"\n✅ Successfully downloaded: {model_info['model_name']}")
        print(f"📦 Model size: {model_info['model_size']}")
        print(f"💾 Memory usage: ~{int(float(model_info['model_size'].replace('B', '')) * 0.5)}GB")
        
        print(f"\n🚀 Next Steps:")
        print(f"1. Start HackAI: python3 run_interactive.py")
        print(f"2. Or use launch script: ./launch.sh")
        print(f"3. Test: scan example.com")
        
        print(f"\n💡 Performance Tips:")
        print(f"- Model optimized with 4-bit quantization")
        print(f"- Double quantization enabled")
        print(f"- Local environment optimized")
        print(f"- Environment variables configured")
        
    else:
        print(f"\n❌ Failed to download LLM")
        print(f"💡 Check disk space and internet connection")

if __name__ == "__main__":
    main()

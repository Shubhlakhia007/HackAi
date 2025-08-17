#!/usr/bin/env python3
"""
HackAI AI Assistant
Intelligent troubleshooting and help system using local LLM
"""

import os
import sys
import json
import asyncio
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.colors import Colors
from ai.base import AIIntegrationManager
from ai.local import LocalAIProvider

class AIAssistant:
    """AI-powered troubleshooting and help assistant"""
    
    def __init__(self):
        self.ai_manager = AIIntegrationManager()
        self.setup_ai_provider()
        
        # Load troubleshooting knowledge base
        self.troubleshooting_kb = self.load_troubleshooting_kb()
        
        # System information
        self.system_info = self.get_system_info()
    
    def setup_ai_provider(self):
        """Setup AI provider"""
        # Load environment variables
        env_file = Path('.env')
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv()
        
        # Add local provider
        local_provider = LocalAIProvider()
        self.ai_manager.add_provider("local", local_provider)
        self.ai_manager.set_default_provider("local")
        
        print(f"{Colors.colorize('✅ AI Assistant initialized with local LLM', Colors.GREEN)}")
    
    def load_troubleshooting_kb(self) -> Dict[str, Any]:
        """Load troubleshooting knowledge base"""
        return {
            "common_issues": {
                "out_of_memory": {
                    "symptoms": ["out of memory", "memory error", "OOM", "insufficient memory"],
                    "solutions": [
                        "Close unnecessary applications to free RAM",
                        "Use a smaller model (Phi-2 instead of Mistral 7B)",
                        "Reduce batch size in model configuration",
                        "Enable swap space on Linux",
                        "Check available memory with: python -c \"import psutil; print(f'{psutil.virtual_memory().available / 1024**3:.1f} GB available')\""
                    ]
                },
                "model_download_fails": {
                    "symptoms": ["download failed", "connection error", "model not found"],
                    "solutions": [
                        "Check internet connection: ping google.com",
                        "Clear model cache: rm -rf models/cache/*",
                        "Try downloading again: python setup_llm.py",
                        "Check disk space: df -h",
                        "Use VPN if behind firewall"
                    ]
                },
                "permission_errors": {
                    "symptoms": ["permission denied", "access denied", "chmod"],
                    "solutions": [
                        "Fix script permissions: chmod +x launch.sh",
                        "Run as administrator on Windows",
                        "Use sudo for system-wide installations",
                        "Check file ownership: ls -la"
                    ]
                },
                "import_errors": {
                    "symptoms": ["import error", "module not found", "no module named"],
                    "solutions": [
                        "Install dependencies: pip install -r requirements.txt",
                        "Force reinstall: pip install -r requirements.txt --force-reinstall",
                        "Check Python version: python --version",
                        "Use virtual environment",
                        "Install missing package: pip install [package_name]"
                    ]
                },
                "gpu_issues": {
                    "symptoms": ["cuda error", "gpu not found", "nvidia"],
                    "solutions": [
                        "Install NVIDIA drivers",
                        "Install CUDA toolkit",
                        "Install PyTorch with CUDA: pip install torch --index-url https://download.pytorch.org/whl/cu118",
                        "Check GPU: nvidia-smi",
                        "Use CPU-only mode if GPU unavailable"
                    ]
                }
            },
            "installation_issues": {
                "python_version": {
                    "check": "python --version",
                    "requirement": "3.8+",
                    "fix": "Install Python 3.8 or higher from python.org"
                },
                "pip_not_found": {
                    "check": "pip --version",
                    "fix": "Install pip: python -m ensurepip --upgrade"
                },
                "system_tools": {
                    "linux": "sudo apt install -y nmap wireshark git python3 python3-pip",
                    "macos": "brew install nmap wireshark git python3",
                    "windows": "choco install nmap wireshark git python3 -y"
                }
            },
            "performance_tips": [
                "Use SSD storage for faster model loading",
                "Close unnecessary applications to free RAM",
                "Enable GPU acceleration if available",
                "Use appropriate model for your hardware",
                "Monitor memory usage with Task Manager/htop",
                "Optimize batch size for your system"
            ]
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get current system information"""
        try:
            import psutil
            
            return {
                "platform": platform.system(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "total_ram": psutil.virtual_memory().total / (1024**3),
                "available_ram": psutil.virtual_memory().available / (1024**3),
                "cpu_count": psutil.cpu_count(),
                "disk_free": psutil.disk_usage('.').free / (1024**3)
            }
        except ImportError:
            return {
                "platform": platform.system(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "error": "psutil not available"
            }
    
    def detect_issue_type(self, user_input: str) -> str:
        """Detect the type of issue from user input"""
        user_input_lower = user_input.lower()
        
        for issue_type, issue_data in self.troubleshooting_kb["common_issues"].items():
            for symptom in issue_data["symptoms"]:
                if symptom in user_input_lower:
                    return issue_type
        
        return "general"
    
    def get_quick_solutions(self, issue_type: str) -> List[str]:
        """Get quick solutions for detected issue"""
        if issue_type in self.troubleshooting_kb["common_issues"]:
            return self.troubleshooting_kb["common_issues"][issue_type]["solutions"]
        return []
    
    async def generate_ai_response(self, user_input: str, context: str = "") -> str:
        """Generate AI response for user input"""
        try:
            # Create enhanced prompt with context
            prompt = f"""
            You are a helpful AI assistant for HackAI, a security testing framework.
            
            System Information:
            - Platform: {self.system_info.get('platform', 'Unknown')}
            - Python: {self.system_info.get('python_version', 'Unknown')}
            - RAM: {self.system_info.get('total_ram', 'Unknown'):.1f} GB
            - Available RAM: {self.system_info.get('available_ram', 'Unknown'):.1f} GB
            
            Context: {context}
            
            User Question: {user_input}
            
            Provide a helpful, detailed response that includes:
            1. Clear explanation of the issue/problem
            2. Step-by-step solution
            3. Code examples if relevant
            4. Additional tips and best practices
            5. How to verify the solution worked
            
            Be specific, practical, and security-focused in your response.
            """
            
            # Get AI response
            response = await self.ai_manager.analyze_target(prompt)
            
            if isinstance(response, dict) and 'summary' in response:
                return response['summary']
            elif isinstance(response, str):
                return response
            else:
                return "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            return f"Error generating AI response: {str(e)}"
    
    async def help_user(self, user_input: str):
        """Main help function"""
        print(f"\n{Colors.colorize('🧠 AI Assistant - Analyzing your request...', Colors.BLUE)}")
        
        # Detect issue type
        issue_type = self.detect_issue_type(user_input)
        
        # Get quick solutions
        quick_solutions = self.get_quick_solutions(issue_type)
        
        # Generate AI response
        ai_response = await self.generate_ai_response(user_input, f"Issue type: {issue_type}")
        
        # Display results
        print(f"\n{Colors.colorize('📋 Analysis Results:', Colors.CYAN)}")
        print(f"Detected Issue Type: {Colors.colorize(issue_type.replace('_', ' ').title(), Colors.YELLOW)}")
        
        if quick_solutions:
            print(f"\n{Colors.colorize('⚡ Quick Solutions:', Colors.GREEN)}")
            for i, solution in enumerate(quick_solutions, 1):
                print(f"  {i}. {Colors.colorize(solution, Colors.WHITE)}")
        
        print(f"\n{Colors.colorize('🤖 AI Response:', Colors.PURPLE)}")
        print(f"{Colors.colorize(ai_response, Colors.WHITE)}")
        
        # Additional tips
        if issue_type == "general":
            print(f"\n{Colors.colorize('💡 General Tips:', Colors.CYAN)}")
            for tip in self.troubleshooting_kb["performance_tips"][:3]:
                print(f"  • {Colors.colorize(tip, Colors.WHITE)}")
    
    async def run_interactive(self):
        """Run interactive AI assistant"""
        print(f"\n{Colors.colorize('🤖 HackAI AI Assistant', Colors.BOLD + Colors.PURPLE)}")
        print(f"{Colors.colorize('Ask me anything about HackAI, troubleshooting, or security testing!', Colors.CYAN)}")
        print(f"{Colors.colorize('Type "quit" to exit', Colors.YELLOW)}")
        
        while True:
            try:
                user_input = input(f"\n{Colors.colorize('🤖 AI> ', Colors.GREEN)}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Colors.colorize('👋 Goodbye!', Colors.CYAN)}")
                    break
                
                if user_input.lower() in ['help', 'h', '?']:
                    self.show_help()
                    continue
                
                # Process the request
                await self.help_user(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Colors.colorize('⏹️  Operation cancelled. Type quit to exit.', Colors.YELLOW)}")
            except Exception as e:
                print(f"{Colors.colorize(f'❌ Error: {str(e)}', Colors.RED)}")
    
    def show_help(self):
        """Show help information"""
        print(f"\n{Colors.colorize('📖 AI Assistant Help', Colors.BOLD + Colors.CYAN)}")
        print(f"\n{Colors.colorize('🔧 Troubleshooting Examples:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('I\'m getting out of memory errors', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Model download is failing', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Permission denied errors', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Import error with torch', Colors.CYAN)}")
        print(f"  • {Colors.colorize('GPU not detected', Colors.CYAN)}")
        
        print(f"\n{Colors.colorize('🛠️  Tool Help Examples:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('How do I use nmap for port scanning?', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Show me sqlmap examples', Colors.CYAN)}")
        print(f"  • {Colors.colorize('What tools should I use for web testing?', Colors.CYAN)}")
        
        print(f"\n{Colors.colorize('🎮 CTF Help Examples:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('How do I solve this crypto challenge?', Colors.CYAN)}")
        print(f"  • {Colors.colorize('What tools for reverse engineering?', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Help me analyze this binary file', Colors.CYAN)}")
        
        print(f"\n{Colors.colorize('⚙️  Configuration Help:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('How do I configure GPU acceleration?', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Optimize performance for my system', Colors.CYAN)}")
        print(f"  • {Colors.colorize('Install additional tools', Colors.CYAN)}")
        
        print(f"\n{Colors.colorize('💡 Tips:', Colors.GREEN)}")
        print(f"  • Be specific in your questions")
        print(f"  • Include error messages if applicable")
        print(f"  • Ask for code examples when needed")
        print(f"  • Type {Colors.colorize('quit', Colors.RED)} to exit")

async def main():
    """Main entry point"""
    assistant = AIAssistant()
    await assistant.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())

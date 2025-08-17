#!/usr/bin/env python3
"""
HackAI Enhanced Interactive CLI
Natural language interface for the AI-powered penetration testing framework
"""

import sys
import os
import asyncio
import argparse
import time
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import difflib
import re

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.colors import Colors
from core.models import ScanResult, AIAnalysis
from database.manager import EnhancedDatabaseManager
from tools.manager import ToolManager
from ai.base import AIIntegrationManager
from ai.gemini import GeminiProvider
from ai.local import LocalAIProvider

class InteractiveHackAICLI:
    """Interactive CLI with natural language understanding"""
    
    def __init__(self):
        self.db_manager = EnhancedDatabaseManager()
        self.tool_manager = ToolManager()
        self.ai_manager = AIIntegrationManager()
        self.session_id = f"session_{int(time.time())}"
        self.context = {}
        
        # Initialize AI providers
        self._setup_ai_providers()
        
        # Command mappings
        self.command_patterns = {
            'scan': [
                r'scan\s+(.+)', r'run\s+(.+)', r'test\s+(.+)', r'check\s+(.+)',
                r'audit\s+(.+)', r'pentest\s+(.+)', r'hack\s+(.+)', r'attack\s+(.+)',
                r'analyze\s+(.+)', r'examine\s+(.+)', r'investigate\s+(.+)', r'look\s+(.+)'
            ],
            'ctf_analyze': [
                r'ctf\s+(.+)', r'challenge\s+(.+)', r'flag\s+(.+)', r'solve\s+(.+)',
                r'forensic\s+(.+)', r'crypto\s+(.+)', r'reverse\s+(.+)', r'pwn\s+(.+)'
            ],
            'ai_help': [
                r'ai\s+(.+)', r'help\s+me\s+(.+)', r'assistant\s+(.+)', r'ask\s+(.+)',
                r'troubleshoot\s+(.+)', r'fix\s+(.+)', r'solve\s+(.+)', r'how\s+to\s+(.+)'
            ],
            'tools': [
                r'tools?', r'list\s+tools?', r'show\s+tools?', r'available\s+tools?',
                r'what\s+tools?', r'installed\s+tools?'
            ],
            'health': [
                r'health', r'status', r'system\s+health', r'check\s+health',
                r'how\s+is\s+it', r'everything\s+ok'
            ],
            'install': [
                r'install\s+(.+)', r'add\s+(.+)', r'get\s+(.+)', r'setup\s+(.+)'
            ],
            'reports': [
                r'reports?', r'show\s+reports?', r'view\s+reports?', r'history',
                r'scan\s+history', r'results?', r'summary'
            ],
            'export': [
                r'export\s+(.+)', r'save\s+report', r'generate\s+report'
            ],
            'test': [
                r'test', r'test\s+setup', r'verify', r'check\s+setup'
            ]
        }
        
        # Tool name mappings for fuzzy matching
        self.tool_aliases = {
            'nmap': ['nmap', 'network mapper', 'port scanner', 'network scan'],
            'nuclei': ['nuclei', 'vulnerability scanner', 'vuln scanner'],
            'gobuster': ['gobuster', 'directory buster', 'dir buster', 'web scanner'],
            'sqlmap': ['sqlmap', 'sql injection', 'sqli'],
            'nikto': ['nikto', 'web scanner', 'web vulnerability'],
            'hydra': ['hydra', 'password cracker', 'brute force'],
            'john': ['john', 'john the ripper', 'password cracker'],
            'hashcat': ['hashcat', 'hash cracker', 'password recovery'],
            'metasploit': ['metasploit', 'msf', 'exploit framework'],
            'wireshark': ['wireshark', 'packet analyzer', 'network analyzer'],
            'aircrack': ['aircrack', 'wifi cracker', 'wireless security'],
            'dirsearch': ['dirsearch', 'directory search', 'web path'],
            'ffuf': ['ffuf', 'web fuzzer', 'fast fuzzer'],
            'httpx': ['httpx', 'http toolkit', 'http scanner'],
            'dalfox': ['dalfox', 'xss scanner', 'xss finder'],
            'amass': ['amass', 'subdomain finder', 'reconnaissance'],
            'theharvester': ['theharvester', 'osint', 'information gathering'],
            'shodan': ['shodan', 'search engine', 'device finder'],
            'responder': ['responder', 'llmnr poisoner', 'network poisoner'],
            'netexec': ['netexec', 'network exploitation', 'smb scanner'],
            'autorecon': ['autorecon', 'automated recon', 'reconnaissance'],
            'rustscan': ['rustscan', 'fast scanner', 'port scanner'],
            'masscan': ['masscan', 'mass scanner', 'fast port scanner'],
            # CTF and Forensic tools
            'binwalk': ['binwalk', 'firmware analysis', 'file analysis'],
            'strings': ['strings', 'extract strings', 'string analysis'],
            'file': ['file', 'file type', 'file identification'],
            'exiftool': ['exiftool', 'exif data', 'metadata'],
            'steghide': ['steghide', 'steganography', 'hidden data'],
            'xxd': ['xxd', 'hex dump', 'hexadecimal'],
            'hexdump': ['hexdump', 'hex view', 'binary analysis'],
            'gdb': ['gdb', 'debugger', 'reverse engineering'],
            'objdump': ['objdump', 'object dump', 'binary analysis'],
            'radare2': ['radare2', 'r2', 'reverse engineering'],
            'ghidra': ['ghidra', 'reverse engineering', 'decompiler'],
            'fcrackzip': ['fcrackzip', 'zip cracker', 'archive password'],
            'pdfcrack': ['pdfcrack', 'pdf password', 'pdf analysis'],
            'zip2john': ['zip2john', 'zip to john', 'archive hash'],
            'rar2john': ['rar2john', 'rar to john', 'rar hash']
        }
        
        # Context types
        self.context_types = {
            'cloud': ['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'amazon', 'microsoft'],
            'forensic': ['forensic', 'forensics', 'digital forensics', 'evidence', 'investigation'],
            'bug_bounty': ['bug bounty', 'bugbounty', 'hackerone', 'bugcrowd', 'responsible disclosure'],
            'ctf': ['ctf', 'capture the flag', 'competition', 'challenge', 'game'],
            'ctf_web': ['ctf web', 'web ctf', 'web challenge', 'web game'],
            'ctf_forensic': ['ctf forensic', 'forensic ctf', 'file ctf', 'file challenge', 'file analysis'],
            'ctf_crypto': ['ctf crypto', 'crypto ctf', 'cryptography', 'encryption challenge'],
            'ctf_reverse': ['ctf reverse', 'reverse ctf', 'reverse engineering', 'binary analysis'],
            'ctf_pwn': ['ctf pwn', 'pwn ctf', 'exploitation', 'buffer overflow'],
            'red_team': ['red team', 'redteam', 'penetration test', 'pentest', 'security assessment'],
            'blue_team': ['blue team', 'blueteam', 'defense', 'security monitoring'],
            'web': ['web', 'web application', 'website', 'webapp', 'http', 'https'],
            'network': ['network', 'infrastructure', 'network security', 'network scan'],
            'mobile': ['mobile', 'android', 'ios', 'app', 'application'],
            'iot': ['iot', 'internet of things', 'device', 'embedded', 'smart device']
        }
    
    def _setup_ai_providers(self):
        """Setup available AI providers"""
        # Load environment variables from .env file if it exists
        env_file = Path('.env')
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv()
        
        # Add Gemini provider if API key is available
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            gemini_provider = GeminiProvider(api_key=gemini_key)
            self.ai_manager.add_provider("gemini", gemini_provider)
            self.ai_manager.set_default_provider("gemini")
            print(f"{Colors.colorize('✅ Gemini AI provider initialized', Colors.GREEN)}")
        
        # Always add local provider as fallback
        local_provider = LocalAIProvider()
        self.ai_manager.add_provider("local", local_provider)
        
        if not gemini_key:
            self.ai_manager.set_default_provider("local")
            print(f"{Colors.colorize('✅ Local AI provider initialized (offline mode)', Colors.YELLOW)}")
    
    def _get_context_type(self, user_input: str) -> str:
        """Determine context type from user input"""
        user_input_lower = user_input.lower()
        
        for context_type, keywords in self.context_types.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return context_type
        
        return "general"
    
    def _fuzzy_match_tool(self, tool_name: str) -> Optional[str]:
        """Fuzzy match tool names"""
        tool_name_lower = tool_name.lower()
        
        # Direct match
        if tool_name_lower in self.tool_manager.tools:
            return tool_name_lower
        
        # Alias match
        for actual_name, aliases in self.tool_aliases.items():
            if tool_name_lower in aliases or any(alias in tool_name_lower for alias in aliases):
                return actual_name
        
        # Fuzzy match
        all_tools = list(self.tool_manager.tools.keys())
        matches = difflib.get_close_matches(tool_name_lower, all_tools, n=1, cutoff=0.6)
        
        if matches:
            return matches[0]
        
        return None
    
    def _parse_command(self, user_input: str) -> Dict[str, Any]:
        """Parse natural language command"""
        user_input_lower = user_input.lower().strip()
        
        # Check for system commands first (reports, tools, health, etc.)
        for command, patterns in self.command_patterns.items():
            if command in ['reports', 'tools', 'health', 'install', 'export']:
                for pattern in patterns:
                    if re.search(pattern, user_input_lower):
                        if command == 'install':
                            # Extract tool names for installation
                            words = user_input_lower.split()
                            tools = []
                            for word in words:
                                if word not in ['install', 'add', 'get', 'setup']:
                                    matched_tool = self._fuzzy_match_tool(word)
                                    if matched_tool:
                                        tools.append(matched_tool)
                            
                            return {
                                'command': 'install',
                                'tools': tools,
                                'context': self._get_context_type(user_input)
                            }
                        else:
                            return {
                                'command': command,
                                'context': self._get_context_type(user_input)
                            }
        
        # Check for CTF analysis commands
        for pattern in self.command_patterns['ctf_analyze']:
            match = re.search(pattern, user_input_lower)
            if match:
                target = match.group(1).strip()
                return {
                    'command': 'ctf_analyze',
                    'target': target,
                    'context': self._get_context_type(user_input)
                }
        
        # Check for scan commands
        for pattern in self.command_patterns['scan']:
            match = re.search(pattern, user_input_lower)
            if match:
                target = match.group(1).strip()
                return {
                    'command': 'scan',
                    'target': target,
                    'context': self._get_context_type(user_input)
                }
        
        # Check for tool-specific commands
        for tool_name, aliases in self.tool_aliases.items():
            for alias in aliases:
                if alias in user_input_lower:
                    # Extract target if present
                    target_match = re.search(rf'{alias}\s+(.+)', user_input_lower)
                    target = target_match.group(1).strip() if target_match else None
                    
                    return {
                        'command': 'tool',
                        'tool': tool_name,
                        'target': target,
                        'context': self._get_context_type(user_input)
                    }
        
        return {
            'command': 'unknown',
            'input': user_input,
            'context': self._get_context_type(user_input)
        }
    
    async def _get_context_info(self) -> Dict[str, Any]:
        """Get context information from user"""
        print(f"\n{Colors.colorize('🎯 What type of security testing are you doing?', Colors.CYAN)}")
        print("Choose from:")
        
        context_options = [
            "1. Cloud Security (AWS, Azure, GCP)",
            "2. Digital Forensics",
            "3. Bug Bounty Program",
            "4. Capture The Flag (CTF) - General",
            "5. CTF - Web Challenges",
            "6. CTF - Forensic/File Analysis",
            "7. CTF - Cryptography",
            "8. CTF - Reverse Engineering",
            "9. CTF - Exploitation/Pwn",
            "10. Red Team / Penetration Testing",
            "11. Blue Team / Defense",
            "12. Web Application Security",
            "13. Network Security",
            "14. Mobile Security",
            "15. IoT Security",
            "16. General Security Assessment"
        ]
        
        for option in context_options:
            print(f"   {Colors.colorize(option, Colors.WHITE)}")
        
        while True:
            try:
                choice = input(f"\n{Colors.colorize('Enter your choice (1-16): ', Colors.YELLOW)}").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= 16:
                    context_map = {
                        1: "cloud", 2: "forensic", 3: "bug_bounty", 4: "ctf",
                        5: "ctf_web", 6: "ctf_forensic", 7: "ctf_crypto", 8: "ctf_reverse",
                        9: "ctf_pwn", 10: "red_team", 11: "blue_team", 12: "web",
                        13: "network", 14: "mobile", 15: "iot", 16: "general"
                    }
                    
                    context_type = context_map[choice_num]
                    
                    # Get additional context
                    additional_info = input(f"\n{Colors.colorize('Any additional context (optional): ', Colors.YELLOW)}").strip()
                    
                    # Get hints for CTF challenges
                    hints = None
                    if context_type.startswith('ctf_'):
                        hints = await self._get_ctf_hints(context_type)
                    
                    return {
                        'type': context_type,
                        'additional_info': additional_info if additional_info else None,
                        'hints': hints
                    }
                else:
                    print(f"{Colors.colorize('❌ Please enter a number between 1 and 16', Colors.RED)}")
            except ValueError:
                print(f"{Colors.colorize('❌ Please enter a valid number', Colors.RED)}")
    
    async def _get_ctf_hints(self, ctf_type: str) -> Dict[str, Any]:
        """Get CTF-specific hints and information"""
        hints = {}
        
        print(f"\n{Colors.colorize('💡 CTF Challenge Information', Colors.CYAN)}")
        
        # Ask for challenge description
        challenge_desc = input(f"{Colors.colorize('Challenge description (optional): ', Colors.YELLOW)}").strip()
        if challenge_desc:
            hints['challenge_description'] = challenge_desc
        
        # Ask for event name
        event_name = input(f"{Colors.colorize('Event name (e.g., Hackfinity Battle 2025): ', Colors.YELLOW)}").strip()
        if event_name:
            hints['event_name'] = event_name
        
        # Ask for difficulty
        difficulty = input(f"{Colors.colorize('Difficulty (easy/medium/hard/expert): ', Colors.YELLOW)}").strip()
        if difficulty:
            hints['difficulty'] = difficulty
        
        # Ask for points
        points = input(f"{Colors.colorize('Points value (optional): ', Colors.YELLOW)}").strip()
        if points:
            hints['points'] = points
        
        # Ask for challenge category
        category = input(f"{Colors.colorize('Challenge category (forensic/crypto/web/pwn/reverse/misc): ', Colors.YELLOW)}").strip()
        if category:
            hints['challenge_category'] = category
        
        # Ask for provided hints
        provided_hints = input(f"{Colors.colorize('Any hints provided (optional): ', Colors.YELLOW)}").strip()
        if provided_hints:
            hints['provided_hints'] = provided_hints
        
        # Ask for file information if forensic/crypto/reverse
        if ctf_type in ['ctf_forensic', 'ctf_crypto', 'ctf_reverse']:
            file_path = input(f"{Colors.colorize('File path to analyze: ', Colors.YELLOW)}").strip()
            if file_path:
                hints['file_path'] = file_path
                
                # Ask for file type if known
                file_type = input(f"{Colors.colorize('Known file type (optional): ', Colors.YELLOW)}").strip()
                if file_type:
                    hints['file_type'] = file_type
                
                # Ask for file size if known
                file_size = input(f"{Colors.colorize('File size (optional): ', Colors.YELLOW)}").strip()
                if file_size:
                    hints['file_size'] = file_size
        
        # Ask for target information if web/pwn
        if ctf_type in ['ctf_web', 'ctf_pwn']:
            target = input(f"{Colors.colorize('Target URL/IP: ', Colors.YELLOW)}").strip()
            if target:
                hints['target'] = target
        
        # Ask for flag format
        flag_format = input(f"{Colors.colorize('Flag format (e.g., flag{...}): ', Colors.YELLOW)}").strip()
        if flag_format:
            hints['flag_format'] = flag_format
        
        # Ask for additional context
        additional_context = input(f"{Colors.colorize('Additional context or keywords (optional): ', Colors.YELLOW)}").strip()
        if additional_context:
            hints['additional_context'] = additional_context
        
        return hints if hints else None
    
    def _format_ctf_hints_for_prompt(self, hints: Dict[str, Any]) -> str:
        """Format CTF hints for AI prompt"""
        if not hints:
            return ""
        
        hint_text = "\nCTF Challenge Information:\n"
        
        if hints.get('challenge_description'):
            hint_text += f"- Challenge Description: {hints['challenge_description']}\n"
        
        if hints.get('provided_hints'):
            hint_text += f"- Provided Hints: {hints['provided_hints']}\n"
        
        if hints.get('file_path'):
            hint_text += f"- File to Analyze: {hints['file_path']}\n"
        
        if hints.get('file_type'):
            hint_text += f"- Known File Type: {hints['file_type']}\n"
        
        if hints.get('target'):
            hint_text += f"- Target: {hints['target']}\n"
        
        if hints.get('flag_format'):
            hint_text += f"- Expected Flag Format: {hints['flag_format']}\n"
        
        if hints.get('challenge_category'):
            hint_text += f"- Challenge Category: {hints['challenge_category']}\n"
        
        if hints.get('difficulty'):
            hint_text += f"- Difficulty Level: {hints['difficulty']}\n"
        
        if hints.get('points'):
            hint_text += f"- Points: {hints['points']}\n"
        
        if hints.get('event_name'):
            hint_text += f"- Event: {hints['event_name']}\n"
        
        return hint_text
    
    def _detect_ctf_challenge_type(self, hints: Dict[str, Any]) -> str:
        """Automatically detect CTF challenge type based on hints and file"""
        if not hints:
            return "ctf"
        
        description = hints.get('challenge_description', '').lower()
        category = hints.get('challenge_category', '').lower()
        file_path = hints.get('file_path', '').lower()
        target = hints.get('target', '').lower()
        
        # Check for specific keywords in description
        if any(word in description for word in ['web', 'http', 'website', 'url']):
            return 'ctf_web'
        elif any(word in description for word in ['forensic', 'file', 'image', 'memory', 'dump']):
            return 'ctf_forensic'
        elif any(word in description for word in ['crypto', 'encrypt', 'decrypt', 'hash', 'password']):
            return 'ctf_crypto'
        elif any(word in description for word in ['reverse', 'binary', 'assembly', 'disassemble']):
            return 'ctf_reverse'
        elif any(word in description for word in ['pwn', 'exploit', 'buffer', 'overflow', 'rop']):
            return 'ctf_pwn'
        
        # Check file extensions
        if file_path:
            if any(ext in file_path for ext in ['.exe', '.bin', '.elf', '.dll']):
                return 'ctf_reverse'
            elif any(ext in file_path for ext in ['.pcap', '.pcapng', '.cap']):
                return 'ctf_forensic'
            elif any(ext in file_path for ext in ['.zip', '.rar', '.7z', '.tar']):
                return 'ctf_forensic'
            elif any(ext in file_path for ext in ['.jpg', '.png', '.bmp', '.gif']):
                return 'ctf_forensic'
        
        # Check category
        if category:
            if category in ['web']:
                return 'ctf_web'
            elif category in ['forensic', 'forensics']:
                return 'ctf_forensic'
            elif category in ['crypto', 'cryptography']:
                return 'ctf_crypto'
            elif category in ['reverse', 'reversing']:
                return 'ctf_reverse'
            elif category in ['pwn', 'exploitation']:
                return 'ctf_pwn'
        
        return 'ctf'
    
    def _get_ctf_tool_recommendations(self, ctf_type: str, hints: Dict[str, Any]) -> List[str]:
        """Get recommended tools for CTF challenge type"""
        base_tools = ['strings', 'file', 'xxd', 'hexdump']
        
        tool_recommendations = {
            'ctf_web': base_tools + ['nuclei', 'gobuster', 'sqlmap', 'nikto', 'dalfox'],
            'ctf_forensic': base_tools + ['binwalk', 'exiftool', 'steghide', 'fcrackzip', 'pdfcrack'],
            'ctf_crypto': base_tools + ['john', 'hashcat', 'zip2john', 'rar2john', 'fcrackzip'],
            'ctf_reverse': base_tools + ['gdb', 'objdump', 'radare2', 'ghidra', 'strings'],
            'ctf_pwn': base_tools + ['gdb', 'objdump', 'checksec', 'pwntools', 'ropgadget']
        }
        
        recommended = tool_recommendations.get(ctf_type, base_tools)
        
        # Add specific tools based on hints
        if hints.get('file_path'):
            file_path = hints['file_path'].lower()
            if any(ext in file_path for ext in ['.zip', '.rar', '.7z']):
                recommended.extend(['unzip', '7z', 'fcrackzip'])
            elif any(ext in file_path for ext in ['.jpg', '.png', '.bmp']):
                recommended.extend(['exiftool', 'steghide', 'binwalk'])
            elif any(ext in file_path for ext in ['.pcap', '.pcapng']):
                recommended.extend(['wireshark', 'tshark', 'tcpdump'])
        
        return list(set(recommended))  # Remove duplicates
    
    async def _execute_ctf_analysis(self, target: str):
        """Execute smart CTF analysis on target"""
        print(f"\n{Colors.colorize('🎮 Smart CTF Analysis', Colors.PURPLE)}")
        print(f"Target: {Colors.colorize(target, Colors.CYAN)}")
        
        # Check if target is a file
        if os.path.exists(target):
            print(f"📁 File detected: {Colors.colorize(target, Colors.GREEN)}")
            
            # Auto-detect file type and suggest CTF category
            file_type = self._get_file_type(target)
            suggested_category = self._suggest_ctf_category(target, file_type)
            
            print(f"📋 File type: {Colors.colorize(file_type, Colors.CYAN)}")
            print(f"🎯 Suggested category: {Colors.colorize(suggested_category, Colors.YELLOW)}")
            
            # Get CTF context
            context = await self._get_context_info()
            
            # Auto-detect challenge type from file
            hints = {
                'file_path': target,
                'file_type': file_type,
                'challenge_category': suggested_category
            }
            
            detected_type = self._detect_ctf_challenge_type(hints)
            context['type'] = detected_type
            context['hints'] = hints
            
            # Show recommended tools
            recommended_tools = self._get_ctf_tool_recommendations(detected_type, hints)
            print(f"\n🛠️  Recommended tools: {Colors.colorize(', '.join(recommended_tools[:8]), Colors.CYAN)}")
            
            # Ask if user wants to run analysis
            run_analysis = input(f"\n{Colors.colorize('Run automated analysis? (y/n): ', Colors.YELLOW)}").strip().lower()
            if run_analysis in ['y', 'yes']:
                await self._run_automated_ctf_analysis(target, detected_type, recommended_tools)
        else:
            print(f"❌ File not found: {Colors.colorize(target, Colors.RED)}")
            print(f"💡 Try providing the full path to the file")
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type using file command"""
        try:
            result = subprocess.run(['file', file_path], capture_output=True, text=True, timeout=10)
            if result.stdout:
                return result.stdout.strip().split(': ')[1]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return "unknown"
    
    def _suggest_ctf_category(self, file_path: str, file_type: str) -> str:
        """Suggest CTF category based on file"""
        file_lower = file_path.lower()
        type_lower = file_type.lower()
        
        if any(ext in file_lower for ext in ['.exe', '.bin', '.elf', '.dll']):
            return 'reverse'
        elif any(ext in file_lower for ext in ['.pcap', '.pcapng', '.cap']):
            return 'forensic'
        elif any(ext in file_lower for ext in ['.zip', '.rar', '.7z', '.tar']):
            return 'forensic'
        elif any(ext in file_lower for ext in ['.jpg', '.png', '.bmp', '.gif']):
            return 'forensic'
        elif any(word in type_lower for word in ['executable', 'binary']):
            return 'reverse'
        elif any(word in type_lower for word in ['archive', 'compressed']):
            return 'forensic'
        elif any(word in type_lower for word in ['image', 'picture']):
            return 'forensic'
        else:
            return 'misc'
    
    async def _run_automated_ctf_analysis(self, file_path: str, ctf_type: str, tools: List[str]):
        """Run automated CTF analysis"""
        print(f"\n{Colors.colorize('🤖 Running Automated CTF Analysis...', Colors.BLUE)}")
        
        analysis_results = []
        
        # Basic analysis for all files
        basic_tools = ['file', 'strings', 'xxd']
        for tool in basic_tools:
            if tool in tools:
                result = await self._run_ctf_tool(tool, file_path)
                if result:
                    analysis_results.append((tool, result))
        
        # Specific analysis based on CTF type
        if ctf_type == 'ctf_forensic':
            forensic_tools = ['binwalk', 'exiftool', 'steghide']
            for tool in forensic_tools:
                if tool in tools:
                    result = await self._run_ctf_tool(tool, file_path)
                    if result:
                        analysis_results.append((tool, result))
        
        elif ctf_type == 'ctf_crypto':
            crypto_tools = ['john', 'hashcat']
            for tool in crypto_tools:
                if tool in tools:
                    result = await self._run_ctf_tool(tool, file_path)
                    if result:
                        analysis_results.append((tool, result))
        
        # Display results
        print(f"\n{Colors.colorize('📊 Analysis Results:', Colors.GREEN)}")
        for tool, result in analysis_results:
            print(f"\n🔧 {Colors.colorize(tool.upper(), Colors.CYAN)}:")
            print(f"{result[:500]}{'...' if len(result) > 500 else ''}")
    
    async def _run_ctf_tool(self, tool: str, file_path: str) -> str:
        """Run a CTF tool on file"""
        try:
            if tool == 'file':
                result = subprocess.run(['file', file_path], capture_output=True, text=True, timeout=10)
            elif tool == 'strings':
                result = subprocess.run(['strings', file_path], capture_output=True, text=True, timeout=30)
            elif tool == 'xxd':
                result = subprocess.run(['xxd', file_path], capture_output=True, text=True, timeout=30)
            elif tool == 'binwalk':
                result = subprocess.run(['binwalk', file_path], capture_output=True, text=True, timeout=60)
            elif tool == 'exiftool':
                result = subprocess.run(['exiftool', file_path], capture_output=True, text=True, timeout=30)
            else:
                return f"Tool {tool} not implemented in automated analysis"
            
            if result.stdout:
                return result.stdout
            elif result.stderr:
                return result.stderr
            else:
                return "No output"
        except subprocess.TimeoutExpired:
            return f"Tool {tool} timed out"
        except Exception as e:
            return f"Error running {tool}: {str(e)}"
    
    async def _execute_scan(self, target: str, context: Dict[str, Any]):
        """Execute AI-guided scan with context"""
        print(f"\n{Colors.colorize(f'🤖 Starting AI-Guided Security Assessment', Colors.PURPLE)}")
        print(f"Target: {Colors.colorize(target, Colors.CYAN)}")
        print(f"Context: {Colors.colorize(context['type'].replace('_', ' ').title(), Colors.CYAN)}")
        
        if context.get('additional_info'):
            print(f"Additional Info: {Colors.colorize(context['additional_info'], Colors.CYAN)}")
        
        if context.get('hints'):
            print(f"\n{Colors.colorize('💡 CTF Hints & Context:', Colors.CYAN)}")
            hints = context['hints']
            
            # Auto-detect CTF type
            detected_type = self._detect_ctf_challenge_type(hints)
            if detected_type != context['type']:
                print(f"  🎯 Auto-detected type: {Colors.colorize(detected_type.replace('_', ' ').title(), Colors.GREEN)}")
                context['type'] = detected_type
            
            if hints.get('challenge_description'):
                print(f"  Challenge: {Colors.colorize(hints['challenge_description'], Colors.WHITE)}")
            if hints.get('event_name'):
                print(f"  Event: {Colors.colorize(hints['event_name'], Colors.BLUE)}")
            if hints.get('difficulty'):
                print(f"  Difficulty: {Colors.colorize(hints['difficulty'].upper(), Colors.YELLOW)}")
            if hints.get('provided_hints'):
                print(f"  Hints: {Colors.colorize(hints['provided_hints'], Colors.YELLOW)}")
            if hints.get('file_path'):
                print(f"  File: {Colors.colorize(hints['file_path'], Colors.CYAN)}")
            if hints.get('target'):
                print(f"  Target: {Colors.colorize(hints['target'], Colors.CYAN)}")
            if hints.get('flag_format'):
                print(f"  Flag Format: {Colors.colorize(hints['flag_format'], Colors.GREEN)}")
            
            # Show recommended tools
            recommended_tools = self._get_ctf_tool_recommendations(context['type'], hints)
            print(f"  🛠️  Recommended tools: {Colors.colorize(', '.join(recommended_tools[:5]), Colors.CYAN)}")
        
        try:
            # AI target analysis with context
            print(f"\n{Colors.colorize('🔍 AI Target Analysis Phase...', Colors.BLUE)}")
            
            # Create enhanced prompt with context
            context_prompt = f"""
            Context: {context['type']} security testing
            Additional Info: {context.get('additional_info', 'None')}
            Target: {target}
            
            {self._format_ctf_hints_for_prompt(context.get('hints'))}
            
            Analyze this target for {context['type']} security testing.
            
            Provide a comprehensive analysis including:
            1. Target type (web application, network, API, file, binary, etc.)
            2. Risk assessment (low, medium, high, critical)
            3. Recommended security testing tools (list 5-10 tools specific to {context['type']})
            4. Testing strategy tailored for {context['type']}
            5. Precautions and legal considerations
            
            Format as JSON with keys: target_type, risk_assessment, recommended_tools, testing_strategy, precautions
            """
            
            analysis = await self.ai_manager.analyze_target(target)
            
            print(f"   Target Type: {Colors.colorize(analysis['target_type'], Colors.CYAN)}")
            print(f"   Risk Assessment: {Colors.colorize(analysis['risk_assessment'].upper(), Colors.RED if analysis['risk_assessment'] in ['high', 'critical'] else Colors.YELLOW)}")
            print(f"   Recommended Tools: {Colors.colorize(', '.join(analysis['recommended_tools']), Colors.GREEN)}")
            
            if analysis.get("testing_strategy"):
                print(f"   Strategy: {Colors.colorize(analysis['testing_strategy'], Colors.WHITE)}")
            if analysis.get("precautions"):
                print(f"   ⚠️  Precautions: {Colors.colorize(analysis['precautions'], Colors.YELLOW)}")
            
            # Execute recommended tools
            print(f"\n{Colors.colorize('🚀 Tool Execution Phase...', Colors.PURPLE)}")
            results = []
            ai_analyses = []
            
            for i, tool_name in enumerate(analysis['recommended_tools'], 1):
                if tool_name not in self.tool_manager.tools:
                    print(f"   {Colors.colorize(f'⚠️  Tool {tool_name} not available, skipping...', Colors.YELLOW)}")
                    continue
                
                tool_count = len(analysis['recommended_tools'])
                print(f"\n   {Colors.colorize(f'🔧 [{i}/{tool_count}] Executing {tool_name.upper()}...', Colors.BLUE)}")
                
                try:
                    # Execute tool
                    result = await self.tool_manager.execute_tool(tool_name, [], target, self.session_id)
                    results.append(result)
                    
                    # Display execution summary
                    status_color = Colors.GREEN if result.success else Colors.RED
                    status_text = "SUCCESS" if result.success else "FAILED"
                    
                    print(f"      Status: {Colors.colorize(status_text, status_color)}")
                    print(f"      Duration: {Colors.colorize(f'{result.duration:.2f}s', Colors.CYAN)}")
                    print(f"      Vulnerabilities: {Colors.colorize(str(result.vulnerabilities_found), Colors.RED if result.vulnerabilities_found > 0 else Colors.GREEN)}")
                    
                    # Show sample output
                    if result.success and result.output.strip():
                        sample_lines = result.output.strip().split('\n')[:2]
                        for line in sample_lines:
                            if line.strip():
                                truncated = line[:80] + "..." if len(line) > 80 else line
                                print(f"      📄 {Colors.colorize(truncated, Colors.WHITE)}")
                    
                    # AI interpretation with context
                    print(f"      {Colors.colorize('🧠 AI Analysis...', Colors.PURPLE)}")
                    
                    ai_analysis = await self.ai_manager.interpret_results_with_context(
                        tool_name, result.output, target, context
                    )
                    ai_analyses.append(ai_analysis)
                    
                    # Display AI insights
                    risk_color = Colors.RED if ai_analysis.risk_level in ['high', 'critical'] else Colors.YELLOW
                    print(f"         Summary: {Colors.colorize(ai_analysis.summary, Colors.WHITE)}")
                    print(f"         Risk: {Colors.colorize(ai_analysis.risk_level.upper(), risk_color)}")
                    print(f"         Confidence: {Colors.colorize(f'{ai_analysis.confidence:.1%}', Colors.CYAN)}")
                    
                    if ai_analysis.findings:
                        print(f"         Key Findings:")
                        for finding in ai_analysis.findings[:2]:  # Show top 2
                            print(f"           • {Colors.colorize(finding, Colors.YELLOW)}")
                    
                    # Save to database
                    self.db_manager.save_scan_result(
                        result, 
                        ai_analyses[-1] if ai_analyses else None
                    )
                    
                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    print(f"      {Colors.colorize('❌ ' + error_msg, Colors.RED)}")
            
            # Display scan completion summary
            self._display_scan_summary(results, ai_analyses)
            
            return results
            
        except Exception as e:
            print(f"{Colors.colorize(f'❌ AI-guided scan failed: {str(e)}', Colors.RED)}")
            return []
    
    def _display_scan_summary(self, results: List[ScanResult], ai_analyses: List[AIAnalysis]):
        """Display scan completion summary"""
        print(f"\n{Colors.colorize('📊 SCAN COMPLETION SUMMARY', Colors.BOLD + Colors.CYAN)}")
        print(f"  Total Tools Executed: {len(results)}")
        print(f"  Successful Executions: {sum(1 for r in results if r.success)}")
        print(f"  Failed Executions: {sum(1 for r in results if not r.success)}")
        print(f"  Total Vulnerabilities Found: {sum(r.vulnerabilities_found for r in results)}")
        print(f"  AI Analyses Generated: {len(ai_analyses)}")
        
        if results:
            avg_duration = sum(r.duration for r in results) / len(results)
            print(f"  Average Tool Duration: {avg_duration:.2f}s")
        
        # Risk distribution
        risk_counts = {}
        for analysis in ai_analyses:
            risk = analysis.risk_level
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        if risk_counts:
            print(f"\n{Colors.colorize('⚠️  Risk Distribution:', Colors.YELLOW)}")
            for risk, count in sorted(risk_counts.items(), key=lambda x: ['low', 'medium', 'high', 'critical'].index(x[0])):
                risk_color = Colors.RED if risk in ['high', 'critical'] else Colors.YELLOW
                print(f"    {risk.upper()}: {Colors.colorize(str(count), risk_color)}")
    
    async def _execute_tool(self, tool_name: str, target: str, context: Dict[str, Any]):
        """Execute a specific tool"""
        print(f"\n{Colors.colorize(f'🔧 Executing {tool_name.upper()} on {target}', Colors.BLUE)}")
        print(f"Context: {Colors.colorize(context['type'].replace('_', ' ').title(), Colors.CYAN)}")
        
        # Handle file-based CTF challenges
        if context['type'] in ['ctf_forensic', 'ctf_crypto', 'ctf_reverse'] and context.get('hints', {}).get('file_path'):
            file_path = context['hints']['file_path']
            if os.path.exists(file_path):
                print(f"📁 Analyzing file: {Colors.colorize(file_path, Colors.CYAN)}")
                # Use file path as target for file analysis tools
                target = file_path
            else:
                print(f"⚠️  File not found: {Colors.colorize(file_path, Colors.YELLOW)}")
        
        try:
            result = await self.tool_manager.execute_tool(tool_name, [], target, self.session_id)
            
            # Display results
            status_color = Colors.GREEN if result.success else Colors.RED
            status_text = "SUCCESS" if result.success else "FAILED"
            
            print(f"\nStatus: {Colors.colorize(status_text, status_color)}")
            print(f"Duration: {Colors.colorize(f'{result.duration:.2f}s', Colors.CYAN)}")
            print(f"Vulnerabilities Found: {Colors.colorize(str(result.vulnerabilities_found), Colors.RED if result.vulnerabilities_found > 0 else Colors.GREEN)}")
            
            if result.success and result.output.strip():
                print(f"\n{Colors.colorize('📄 Output:', Colors.WHITE)}")
                lines = result.output.strip().split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    print(f"  {line}")
                if len(lines) > 10:
                    print(f"  {Colors.colorize(f'... and {len(lines) - 10} more lines', Colors.CYAN)}")
            
            # AI analysis
            print(f"\n{Colors.colorize('🧠 AI Analysis...', Colors.PURPLE)}")
            ai_analysis = await self.ai_manager.interpret_results_with_context(
                tool_name, result.output, target, context
            )
            
            risk_color = Colors.RED if ai_analysis.risk_level in ['high', 'critical'] else Colors.YELLOW
            print(f"Summary: {Colors.colorize(ai_analysis.summary, Colors.WHITE)}")
            print(f"Risk: {Colors.colorize(ai_analysis.risk_level.upper(), risk_color)}")
            print(f"Confidence: {Colors.colorize(f'{ai_analysis.confidence:.1%}', Colors.CYAN)}")
            
            if ai_analysis.findings:
                print(f"Key Findings:")
                for finding in ai_analysis.findings:
                    print(f"  • {Colors.colorize(finding, Colors.YELLOW)}")
            
            # Save to database
            self.db_manager.save_scan_result(result, ai_analysis)
            
        except Exception as e:
            print(f"{Colors.colorize(f'❌ Error executing {tool_name}: {str(e)}', Colors.RED)}")
    
    async def run_interactive(self):
        """Run the interactive CLI"""
        print(f"\n{Colors.colorize('🚀 HackAI - Advanced Security Testing Framework', Colors.BOLD + Colors.PURPLE)}")
        print(f"{Colors.colorize('Natural language security testing interface', Colors.CYAN)}")
        print(f"{Colors.colorize('Type help for commands, quit to exit', Colors.YELLOW)}")
        
        while True:
            try:
                user_input = input(f"\n{Colors.colorize('🔍 HackAI> ', Colors.GREEN)}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Colors.colorize('👋 Goodbye!', Colors.CYAN)}")
                    break
                
                if user_input.lower() in ['help', 'h', '?']:
                    self._show_help()
                    continue
                
                # Parse the command
                parsed = self._parse_command(user_input)
                
                if parsed['command'] == 'unknown':
                    print(f"{Colors.colorize('❓ I did not understand that. Try:', Colors.YELLOW)}")
                    print(f"  • {Colors.colorize('scan example.com', Colors.CYAN)}")
                    print(f"  • {Colors.colorize('run nmap on example.com', Colors.CYAN)}")
                    print(f"  • {Colors.colorize('tools', Colors.CYAN)}")
                    print(f"  • {Colors.colorize('health', Colors.CYAN)}")
                    continue
                
                # Only get context for security-related commands
                if parsed['command'] in ['scan', 'tool', 'ctf_analyze']:
                    if 'context' not in parsed or parsed['context'] == 'general':
                        context = await self._get_context_info()
                    else:
                        context = {'type': parsed['context'], 'additional_info': None}
                else:
                    # For system commands, skip context entirely
                    context = None
                
                # Execute command
                if parsed['command'] == 'scan':
                    await self._execute_scan(parsed['target'], context)
                
                elif parsed['command'] == 'tool':
                    if parsed['target']:
                        await self._execute_tool(parsed['tool'], parsed['target'], context)
                    else:
                        tool_name = parsed["tool"]
                        print(f"{Colors.colorize(f'❓ What target do you want to run {tool_name} on?', Colors.YELLOW)}")
                        target = input(f"{Colors.colorize('Target: ', Colors.YELLOW)}").strip()
                        if target:
                            await self._execute_tool(parsed['tool'], target, context)
                
                elif parsed['command'] == 'tools':
                    self.tool_manager.list_tools(None, True)
                
                elif parsed['command'] == 'health':
                    self._check_system_health()
                
                elif parsed['command'] == 'reports':
                    self._show_reports()
                
                elif parsed['command'] == 'export':
                    self._export_report(parsed.get('input', ''))
                
                elif parsed['command'] == 'install':
                    if parsed['tools']:
                        self._install_tools(parsed['tools'])
                    else:
                        print(f"{Colors.colorize('❓ What tools do you want to install?', Colors.YELLOW)}")
                        tools_input = input(f"{Colors.colorize('Tools (space-separated): ', Colors.YELLOW)}").strip()
                        if tools_input:
                            tools = [self._fuzzy_match_tool(tool.strip()) for tool in tools_input.split()]
                            tools = [t for t in tools if t]
                            if tools:
                                self._install_tools(tools)
                
                elif parsed['command'] == 'ctf_analyze':
                    await self._execute_ctf_analysis(parsed['target'])
                
                elif parsed['command'] == 'ai_help':
                    await self._execute_ai_help(parsed['target'])
                
                elif parsed['command'] == 'test':
                    self._run_setup_test()
                
            except KeyboardInterrupt:
                print(f"\n{Colors.colorize('⏹️  Operation cancelled. Type quit to exit.', Colors.YELLOW)}")
            except Exception as e:
                print(f"{Colors.colorize(f'❌ Error: {str(e)}', Colors.RED)}")
    
    def _show_help(self):
        """Show help information"""
        print(f"\n{Colors.colorize('📖 HackAI - Advanced Security Testing Framework', Colors.BOLD + Colors.CYAN)}")
        print(f"\n{Colors.colorize('🔍 Scan Commands:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('scan example.com', Colors.CYAN)} - AI-guided security scan")
        print(f"  • {Colors.colorize('analyze mystery_file.zip', Colors.CYAN)} - CTF file analysis")
        print(f"  • {Colors.colorize('ctf mystery_file.zip', Colors.CYAN)} - Smart CTF analysis")
        print(f"  • {Colors.colorize('forensic mystery_file.zip', Colors.CYAN)} - Forensic analysis")
        print(f"  • {Colors.colorize('crypto mystery_file.zip', Colors.CYAN)} - Crypto analysis")
        print(f"  • {Colors.colorize('reverse mystery_file.exe', Colors.CYAN)} - Reverse engineering")
        print(f"  • {Colors.colorize('run nmap on example.com', Colors.CYAN)} - Run specific tool")
        print(f"  • {Colors.colorize('test example.com', Colors.CYAN)} - Alternative scan command")
        print(f"  • {Colors.colorize('audit example.com', Colors.CYAN)} - Security audit")
        
        print(f"\n{Colors.colorize('🔧 Tool Commands:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('nmap example.com', Colors.CYAN)} - Network scanning")
        print(f"  • {Colors.colorize('gobuster example.com', Colors.CYAN)} - Web directory scanning")
        print(f"  • {Colors.colorize('sqlmap example.com', Colors.CYAN)} - SQL injection testing")
        print(f"  • {Colors.colorize('nuclei example.com', Colors.CYAN)} - Vulnerability scanning")
        print(f"  • {Colors.colorize('binwalk mystery_file', Colors.CYAN)} - File analysis")
        print(f"  • {Colors.colorize('strings mystery_file', Colors.CYAN)} - Extract strings")
        print(f"  • {Colors.colorize('steghide mystery_file', Colors.CYAN)} - Steganography")
        print(f"  • {Colors.colorize('john hash.txt', Colors.CYAN)} - Password cracking")
        
        print(f"\n{Colors.colorize('📋 System Commands:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('tools', Colors.CYAN)} - List available tools")
        print(f"  • {Colors.colorize('health', Colors.CYAN)} - Check system health")
        print(f"  • {Colors.colorize('install nmap nuclei', Colors.CYAN)} - Install tools")
        print(f"  • {Colors.colorize('reports', Colors.CYAN)} - View scan reports and history")
        print(f"  • {Colors.colorize('export', Colors.CYAN)} - Export reports to files")
        print(f"  • {Colors.colorize('test', Colors.CYAN)} - Test your setup")
        
        print(f"\n{Colors.colorize('🤖 AI Assistant Commands:', Colors.YELLOW)}")
        print(f"  • {Colors.colorize('ai help me fix this error', Colors.CYAN)} - Get AI help")
        print(f"  • {Colors.colorize('ai how do I use nmap', Colors.CYAN)} - Ask for tool help")
        print(f"  • {Colors.colorize('ai troubleshoot memory issues', Colors.CYAN)} - Get troubleshooting")
        print(f"  • {Colors.colorize('ai show me CTF examples', Colors.CYAN)} - Get CTF help")
        
        print(f"\n{Colors.colorize('💡 Tips:', Colors.GREEN)}")
        print(f"  • Commands are case-insensitive")
        print(f"  • Spelling mistakes are automatically corrected")
        print(f"  • Context is only asked for security scans")
        print(f"  • Type {Colors.colorize('quit', Colors.RED)} to exit")
    
    def _check_system_health(self):
        """Check system health"""
        print(f"\n{Colors.colorize('🔍 Performing System Health Check...', Colors.CYAN)}")
        
        # Check tool availability
        availability = self.tool_manager.check_tool_availability()
        total_tools = len(availability)
        available_tools = sum(availability.values())
        
        print(f"  Tools Available: {Colors.colorize(f'{available_tools}/{total_tools}', Colors.GREEN if available_tools == total_tools else Colors.YELLOW)}")
        
        # Check AI providers
        print(f"\n{Colors.colorize('🤖 AI Integration Status:', Colors.BLUE)}")
        for name, provider in self.ai_manager.providers.items():
            status = Colors.colorize("✅ Available", Colors.GREEN) if provider.is_available() else Colors.colorize("❌ Unavailable", Colors.RED)
            print(f"  {name}: {status}")
        
        # Check database
        print(f"\n{Colors.colorize('💾 Database Status:', Colors.BLUE)}")
        try:
            stats = self.db_manager.get_database_stats()
            print(f"  Total Scans: {stats['total_scans']}")
            print(f"  Total AI Analyses: {stats['total_ai_analyses']}")
            print(f"  Database Size: {stats['db_size']:,} bytes")
        except Exception as e:
            print(f"  {Colors.colorize(f'❌ Database error: {str(e)}', Colors.RED)}")
        
        # Calculate health score
        health_score = 0
        if available_tools > 0:
            health_score += (available_tools / total_tools) * 40  # Tools: 40 points
        
        if self.ai_manager.get_available_providers():
            health_score += 30  # AI: 30 points
        
        try:
            self.db_manager.get_database_stats()
            health_score += 30  # Database: 30 points
        except Exception:
            pass
        
        print(f"\n{Colors.colorize('📋 System Health Score:', Colors.CYAN)} {Colors.colorize(f'{health_score}/100', Colors.GREEN if health_score >= 75 else Colors.YELLOW if health_score >= 50 else Colors.RED)}")
    
    def _install_tools(self, tools: List[str]):
        """Install tools"""
        print(f"\n{Colors.colorize('📦 Installing Tools...', Colors.CYAN)}")
        
        for tool in tools:
            print(f"  Installing {Colors.colorize(tool, Colors.YELLOW)}...")
            if self.tool_manager.install_tool(tool):
                print(f"    {Colors.colorize('✅ Success', Colors.GREEN)}")
            else:
                print(f"    {Colors.colorize('❌ Failed', Colors.RED)}")
    
    def _show_reports(self):
        """Show scan reports and history"""
        print(f"\n{Colors.colorize('📊 Scan Reports & History', Colors.BOLD + Colors.CYAN)}")
        print("Choose an option:")
        print(f"  1. {Colors.colorize('Summary', Colors.CYAN)} - Show scan statistics")
        print(f"  2. {Colors.colorize('Recent Scans', Colors.CYAN)} - Show recent scan results")
        print(f"  3. {Colors.colorize('Target History', Colors.CYAN)} - Show history for specific target")
        print(f"  4. {Colors.colorize('Export Report', Colors.CYAN)} - Export report to file")
        
        choice = input(f"\n{Colors.colorize('Enter your choice (1-4): ', Colors.YELLOW)}").strip()
        
        if choice == '1':
            self._show_scan_summary()
        elif choice == '2':
            self._show_recent_scans()
        elif choice == '3':
            target = input(f"{Colors.colorize('Enter target: ', Colors.YELLOW)}").strip()
            if target:
                self._show_target_history(target)
        elif choice == '4':
            self._export_report()
    
    def _show_scan_summary(self):
        """Show scan summary"""
        try:
            from view_reports import ReportViewer
            viewer = ReportViewer()
            viewer.display_summary()
        except ImportError:
            print(f"{Colors.colorize('❌ Report viewer not available', Colors.RED)}")
    
    def _show_recent_scans(self):
        """Show recent scans"""
        try:
            from view_reports import ReportViewer
            viewer = ReportViewer()
            viewer.display_recent_scans()
        except ImportError:
            print(f"{Colors.colorize('❌ Report viewer not available', Colors.RED)}")
    
    def _show_target_history(self, target: str):
        """Show target history"""
        try:
            from view_reports import ReportViewer
            viewer = ReportViewer()
            history = viewer.get_target_history(target)
            
            print(f"\n{Colors.colorize(f'🎯 TARGET HISTORY: {target}', Colors.BOLD + Colors.CYAN)}")
            print(f"{Colors.colorize('=' * 80, Colors.CYAN)}")
            
            for scan in history:
                status_color = Colors.GREEN if scan['success'] else Colors.RED
                status_text = "✅ SUCCESS" if scan['success'] else "❌ FAILED"
                
                timestamp = scan['timestamp']
                print(f"\n{Colors.colorize(f'[{timestamp}]', Colors.YELLOW)}")
                print(f"  Tool: {Colors.colorize(scan['tool'], Colors.CYAN)}")
                print(f"  Status: {Colors.colorize(status_text, status_color)}")
                duration = scan['duration']
                vulnerabilities = scan['vulnerabilities_found']
                print(f"  Duration: {Colors.colorize(f'{duration:.2f}s', Colors.CYAN)}")
                print(f"  Vulnerabilities: {Colors.colorize(str(vulnerabilities), Colors.RED if vulnerabilities > 0 else Colors.GREEN)}")
                
                if scan['summary']:
                    print(f"  AI Summary: {Colors.colorize(scan['summary'][:100] + '...', Colors.WHITE)}")
        except ImportError:
            print(f"{Colors.colorize('❌ Report viewer not available', Colors.RED)}")
    
    def _export_report(self, format_hint: str = ""):
        """Export scan report"""
        print(f"\n{Colors.colorize('📤 Export Report', Colors.BOLD + Colors.CYAN)}")
        
        # Get target (optional)
        target = input(f"{Colors.colorize('Target (optional, press Enter to skip): ', Colors.YELLOW)}").strip()
        if not target:
            target = None
        
        # Get format
        print("Choose format:")
        print(f"  1. {Colors.colorize('JSON', Colors.CYAN)} - Machine-readable format")
        print(f"  2. {Colors.colorize('Text', Colors.CYAN)} - Plain text report")
        print(f"  3. {Colors.colorize('HTML', Colors.CYAN)} - Web-friendly report")
        
        format_choice = input(f"{Colors.colorize('Enter format (1-3): ', Colors.YELLOW)}").strip()
        
        format_map = {'1': 'json', '2': 'txt', '3': 'html'}
        export_format = format_map.get(format_choice, 'html')
        
        try:
            from view_reports import ReportViewer
            viewer = ReportViewer()
            filename = viewer.export_report(target, 7, export_format)
            print(f"{Colors.colorize(f'✅ Report exported to: {filename}', Colors.GREEN)}")
        except ImportError:
            print(f"{Colors.colorize('❌ Report viewer not available', Colors.RED)}")

    async def _execute_ai_help(self, question: str):
        """Execute AI help for user question"""
        print(f"\n{Colors.colorize('🤖 AI Assistant - Processing your question...', Colors.PURPLE)}")
        print(f"Question: {Colors.colorize(question, Colors.CYAN)}")
        
        try:
            # Import and use AI assistant
            from ai_assistant import AIAssistant
            assistant = AIAssistant()
            await assistant.help_user(question)
        except ImportError:
            print(f"{Colors.colorize('❌ AI Assistant not available', Colors.RED)}")
            print(f"{Colors.colorize('💡 Try running: python ai_assistant.py', Colors.YELLOW)}")
        except Exception as e:
            print(f"{Colors.colorize(f'❌ AI Assistant error: {str(e)}', Colors.RED)}")

    def _run_setup_test(self):
        """Run setup test"""
        print(f"\n{Colors.colorize('🧪 Running Setup Test...', Colors.BLUE)}")
        
        try:
            # Import and run test script
            import test_local_setup
            test_local_setup.main()
        except ImportError:
            print(f"{Colors.colorize('❌ Test script not available', Colors.RED)}")
            print(f"{Colors.colorize('💡 Try running: python test_local_setup.py', Colors.YELLOW)}")
        except Exception as e:
            print(f"{Colors.colorize(f'❌ Test error: {str(e)}', Colors.RED)}")

async def main():
    """Main entry point"""
    cli = InteractiveHackAICLI()
    await cli.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())

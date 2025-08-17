#!/usr/bin/env python3
"""
Tool management for HackAI Enhanced
"""

import subprocess
import asyncio
import time
from typing import Dict, List, Optional
from core.models import ToolConfig, ScanResult
from core.colors import Colors

class ToolManager:
    """Manages security tools and their execution"""
    
    def __init__(self):
        self.tools = self._init_comprehensive_tools()
    
    def _init_comprehensive_tools(self) -> Dict[str, ToolConfig]:
        """Initialize comprehensive tool configuration with 150+ tools from HackAI AI v6.0"""
        tools = {
            # Network Discovery & Port Scanning (Enhanced)
            "nmap": ToolConfig("nmap", "nmap", "network", "Network port scanner and service detection", 
                             "apt install nmap -y", "which nmap", "nmap --version",
                             common_args=["-sV", "-sC", "--top-ports", "1000"]),
            "masscan": ToolConfig("masscan", "masscan", "network", "High-speed Internet-scale port scanner",
                                "apt install masscan -y", "which masscan", "masscan --version",
                                common_args=["--rate=1000", "-p1-65535"]),
            "rustscan": ToolConfig("rustscan", "rustscan", "network", "Ultra-fast port scanner written in Rust",
                                 "cargo install rustscan", "which rustscan", "rustscan --version",
                                 common_args=["-a", "--ulimit", "5000"]),
            "autorecon": ToolConfig("autorecon", "autorecon", "network", "Automated reconnaissance tool",
                                  "pip3 install autorecon", "which autorecon", "autorecon --version"),
            "netexec": ToolConfig("netexec", "netexec", "network", "Network exploitation tool",
                                "pip3 install netexec", "which netexec", "netexec --version"),
            "responder": ToolConfig("responder", "responder", "network", "LLMNR/NBT-NS/mDNS poisoner",
                                 "apt install responder -y", "which responder", "responder --version"),
            
            # Web Application Testing (Enhanced)
            "gobuster": ToolConfig("gobuster", "gobuster", "web", "Directory/file brute-forcer",
                                 "apt install gobuster -y", "which gobuster", "gobuster version",
                                 common_args=["dir", "-w", "/usr/share/wordlists/dirb/common.txt", "-u"]),
            "feroxbuster": ToolConfig("feroxbuster", "feroxbuster", "web", "Fast content discovery tool",
                                    "cargo install feroxbuster", "which feroxbuster", "feroxbuster --version",
                                    common_args=["-u", "-w", "/usr/share/wordlists/dirb/common.txt"]),
            "dirsearch": ToolConfig("dirsearch", "dirsearch", "web", "Web path scanner",
                                  "pip3 install dirsearch", "which dirsearch", "dirsearch --version",
                                  common_args=["-u", "-e", "php,html,js"]),
            "ffuf": ToolConfig("ffuf", "ffuf", "web", "Fast web fuzzer written in Go",
                             "go install github.com/ffuf/ffuf/v2@latest", "which ffuf", "ffuf -V",
                             common_args=["-w", "/usr/share/wordlists/dirb/common.txt", "-u"]),
            "katana": ToolConfig("katana", "katana", "web", "Advanced web crawling and discovery",
                               "go install github.com/projectdiscovery/katana/cmd/katana@latest", "which katana", "katana -version"),
            "arjun": ToolConfig("arjun", "arjun", "web", "HTTP parameter discovery suite",
                              "pip3 install arjun", "which arjun", "arjun --version"),
            "paramspider": ToolConfig("paramspider", "paramspider", "web", "Mining parameters from dark corners",
                                    "pip3 install paramspider", "which paramspider", "paramspider --version"),
            "x8": ToolConfig("x8", "x8", "web", "HTTP parameter brute forcer",
                           "go install github.com/Sh1Yo/x8@latest", "which x8", "x8 --version"),
            "jaeles": ToolConfig("jaeles", "jaeles", "web", "Advanced web application scanner",
                               "go install github.com/jaeles-project/jaeles@latest", "which jaeles", "jaeles --version"),
            "dalfox": ToolConfig("dalfox", "dalfox", "web", "XSS scanner and parameter analyzer",
                               "go install github.com/hahwul/dalfox/v2@latest", "which dalfox", "dalfox --version"),
            
            # Vulnerability Scanners
            "nuclei": ToolConfig("nuclei", "nuclei", "vuln", "Fast vulnerability scanner",
                               "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                               "which nuclei", "nuclei -version",
                               common_args=["-t", "nuclei-templates/", "-severity", "medium,high,critical"]),
            "httpx": ToolConfig("httpx", "httpx", "web", "Fast HTTP toolkit",
                              "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
                              "which httpx", "httpx -version",
                              common_args=["-status-code", "-title", "-tech-detect"]),
            "nikto": ToolConfig("nikto", "nikto", "web", "Web server scanner",
                              "apt install nikto -y", "which nikto", "nikto -Version",
                              common_args=["-h"]),
            
            # SQL Injection Testing
            "sqlmap": ToolConfig("sqlmap", "sqlmap", "web", "Automatic SQL injection tool",
                               "apt install sqlmap -y", "which sqlmap", "sqlmap --version",
                               common_args=["-u", "--batch", "--level=2"]),
            
            # Authentication & Password Testing
            "hydra": ToolConfig("hydra", "hydra", "auth", "Network login cracker",
                              "apt install hydra -y", "which hydra", "hydra -h"),
            "john": ToolConfig("john", "john", "auth", "Password cracker",
                             "apt install john -y", "which john", "john --version"),
            "hashcat": ToolConfig("hashcat", "hashcat", "auth", "Advanced password recovery",
                                "apt install hashcat -y", "which hashcat", "hashcat --version"),
            
            # Subdomain Enumeration & DNS
            "subfinder": ToolConfig("subfinder", "subfinder", "recon", "Passive subdomain discovery",
                                  "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                                  "which subfinder", "subfinder -version",
                                  common_args=["-d"]),
            "amass": ToolConfig("amass", "amass", "recon", "Attack surface mapping and asset discovery",
                              "apt install amass -y", "which amass", "amass version",
                              common_args=["enum", "-d"]),
            
            # OSINT Tools
            "theharvester": ToolConfig("theharvester", "theharvester", "osint", "Email, domain, employee harvesting",
                                     "pip3 install theharvester", "which theharvester", "theharvester --version"),
            "shodan": ToolConfig("shodan", "shodan", "osint", "Shodan CLI",
                               "pip3 install shodan", "which shodan", "shodan version"),
            
            # Network Analysis
            "wireshark": ToolConfig("wireshark", "wireshark", "network", "Network protocol analyzer",
                                  "apt install wireshark -y", "which wireshark", "wireshark --version"),
            "tcpdump": ToolConfig("tcpdump", "tcpdump", "network", "Command-line packet analyzer",
                                "apt install tcpdump -y", "which tcpdump", "tcpdump --version"),
            
            # Binary Analysis (Enhanced)
            "binwalk": ToolConfig("binwalk", "binwalk", "binary", "Firmware analysis tool",
                                "apt install binwalk -y", "which binwalk", "binwalk --version"),
            "strings": ToolConfig("strings", "strings", "binary", "Extract strings from binaries",
                                "apt install binutils -y", "which strings", "strings --version"),
            "ghidra": ToolConfig("ghidra", "ghidra", "binary", "Software reverse engineering framework",
                               "apt install ghidra -y", "which ghidra", "ghidra --version"),
            "radare2": ToolConfig("radare2", "radare2", "binary", "Advanced reverse engineering framework",
                                "apt install radare2 -y", "which radare2", "radare2 --version"),
            "pwntools": ToolConfig("pwntools", "python3 -m pwn", "binary", "CTF framework and exploit development",
                                 "pip3 install pwntools", "python3 -c 'import pwn'", "python3 -c 'import pwn; print(pwn.__version__)'"),
            "ropgadget": ToolConfig("ropgadget", "ropgadget", "binary", "ROP gadget finder and binary analyzer",
                                  "pip3 install ropgadget", "which ropgadget", "ropgadget --version"),
            "one_gadget": ToolConfig("one_gadget", "one_gadget", "binary", "Find one_gadget in glibc",
                                   "gem install one_gadget", "which one_gadget", "one_gadget --version"),
            "angr": ToolConfig("angr", "angr", "binary", "Platform-agnostic binary analysis framework",
                             "pip3 install angr", "python3 -c 'import angr'", "python3 -c 'import angr; print(angr.__version__)'"),
            
            # Cloud Security (Enhanced)
            "prowler": ToolConfig("prowler", "prowler", "cloud", "AWS/Azure/GCP security tool",
                                "pip3 install prowler", "which prowler", "prowler --version"),
            "trivy": ToolConfig("trivy", "trivy", "cloud", "Container vulnerability scanner",
                              "apt install trivy -y", "which trivy", "trivy --version"),
            "scoutsuite": ToolConfig("scoutsuite", "scout", "cloud", "Multi-cloud security auditing tool",
                                   "pip3 install scoutsuite", "which scout", "scout --version"),
            "cloudmapper": ToolConfig("cloudmapper", "cloudmapper", "cloud", "Cloud infrastructure visualization",
                                    "pip3 install cloudmapper", "which cloudmapper", "cloudmapper --version"),
            "pacu": ToolConfig("pacu", "pacu", "cloud", "AWS exploitation framework",
                             "pip3 install pacu", "which pacu", "pacu --version"),
            "kube-hunter": ToolConfig("kube-hunter", "kube-hunter", "cloud", "Kubernetes security testing",
                                    "pip3 install kube-hunter", "which kube-hunter", "kube-hunter --version"),
            "kube-bench": ToolConfig("kube-bench", "kube-bench", "cloud", "Kubernetes benchmark assessment",
                                   "go install github.com/aquasecurity/kube-bench/cmd/kube-bench@latest", "which kube-bench", "kube-bench --version"),
            
            # Container Security
            "docker-bench": ToolConfig("docker-bench", "docker-bench-security", "container", "Docker security benchmark",
                                     "docker run --rm --net host --pid host --userns host --cap-add audit_control",
                                     "docker --version", "docker --version"),
            
            # Mobile Security
            "mobsf": ToolConfig("mobsf", "mobsf", "mobile", "Mobile Security Framework",
                              "pip3 install mobsf", "which mobsf", "mobsf --version"),
            "apktool": ToolConfig("apktool", "apktool", "mobile", "Android APK reverse engineering",
                                "apt install apktool -y", "which apktool", "apktool --version"),
            
            # Forensics
            "autopsy": ToolConfig("autopsy", "autopsy", "forensics", "Digital forensics platform",
                                "apt install autopsy -y", "which autopsy", "autopsy --version"),
            "volatility": ToolConfig("volatility", "volatility", "forensics", "Memory forensics framework",
                                   "pip3 install volatility3", "which volatility", "volatility --version"),
            
            # Wireless Security
            "aircrack-ng": ToolConfig("aircrack-ng", "aircrack-ng", "wireless", "WiFi security auditing tools",
                                    "apt install aircrack-ng -y", "which aircrack-ng", "aircrack-ng --help"),
            "wifite": ToolConfig("wifite", "wifite", "wireless", "Automated wireless attack tool",
                               "apt install wifite -y", "which wifite", "wifite --help"),
            
            # Social Engineering
            "setoolkit": ToolConfig("setoolkit", "setoolkit", "social", "Social Engineer Toolkit",
                                  "apt install set -y", "which setoolkit", "setoolkit --version"),
            
            # Exploitation
            "metasploit": ToolConfig("metasploit", "msfconsole", "exploitation", "Penetration testing framework",
                                   "apt install metasploit-framework -y", "which msfconsole", "msfconsole --version"),
            "exploitdb": ToolConfig("exploitdb", "searchsploit", "exploitation", "Exploit database search tool",
                                  "apt install exploitdb -y", "which searchsploit", "searchsploit --version")
        }
        
        return tools
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """Check which tools are available on the system"""
        availability = {}
        for name, tool in self.tools.items():
            try:
                if tool.check_cmd:
                    result = subprocess.run(tool.check_cmd.split(), 
                                          capture_output=True, text=True, timeout=5)
                    availability[name] = result.returncode == 0
                else:
                    availability[name] = False
            except Exception:
                availability[name] = False
        return availability
    
    async def execute_tool(self, tool_name: str, args: List[str], target: str = "", session_id: str = "") -> ScanResult:
        """Execute a security tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool = self.tools[tool_name]
        start_time = time.time()
        
        try:
            # Build command
            cmd = [tool.command] + (tool.common_args or []) + args
            if target and tool.requires_target:
                cmd.append(target)
            
            # Execute tool
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            duration = time.time() - start_time
            
            # Create scan result
            scan_result = ScanResult(
                tool=tool_name,
                target=target,
                command=" ".join(cmd),
                output=result.stdout,
                exit_code=result.returncode,
                duration=duration,
                timestamp=time.time(),
                success=result.returncode == 0,
                session_id=session_id,
                risk_level=self._assess_risk_level(result.stdout, tool_name),
                vulnerabilities_found=self._count_vulnerabilities(result.stdout, tool_name)
            )
            
            return scan_result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return ScanResult(
                tool=tool_name,
                target=target,
                command=" ".join(cmd),
                output="Tool execution timed out",
                exit_code=-1,
                duration=duration,
                timestamp=time.time(),
                success=False,
                session_id=session_id,
                risk_level="high",
                vulnerabilities_found=0
            )
        except Exception as e:
            duration = time.time() - start_time
            return ScanResult(
                tool=tool_name,
                target=target,
                command=" ".join(cmd),
                output=f"Error: {str(e)}",
                exit_code=-1,
                duration=duration,
                timestamp=time.time(),
                success=False,
                session_id=session_id,
                risk_level="high",
                vulnerabilities_found=0
            )
    
    def _count_vulnerabilities(self, output: str, tool_name: str) -> int:
        """Count vulnerabilities in tool output"""
        vuln_keywords = ["vulnerability", "vulnerable", "cve", "exploit", "critical", "high", "medium"]
        count = 0
        output_lower = output.lower()
        
        for keyword in vuln_keywords:
            count += output_lower.count(keyword)
        
        return count
    
    def _assess_risk_level(self, output: str, tool_name: str) -> str:
        """Assess risk level based on tool output"""
        output_lower = output.lower()
        
        if any(word in output_lower for word in ["critical", "vulnerable", "exploit"]):
            return "critical"
        elif any(word in output_lower for word in ["high", "dangerous", "severe"]):
            return "high"
        elif any(word in output_lower for word in ["medium", "warning", "caution"]):
            return "medium"
        else:
            return "low"
    
    def list_tools(self, category: str = None, show_status: bool = True):
        """List available tools"""
        availability = self.check_tool_availability() if show_status else {}
        
        if category:
            tools = {name: tool for name, tool in self.tools.items() if tool.category == category}
        else:
            tools = self.tools
        
        # Group by category
        categories = {}
        for name, tool in tools.items():
            cat = tool.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'name': name,
                'description': tool.description,
                'available': availability.get(name, False) if show_status else None
            })
        
        # Display tools
        for cat, tool_list in sorted(categories.items()):
            print(f"\n{Colors.colorize(f'📂 {cat.upper()} ({len(tool_list)} tools)', Colors.YELLOW)}")
            for tool in tool_list:
                if show_status:
                    status = Colors.colorize("✅", Colors.GREEN) if tool['available'] else Colors.colorize("❌", Colors.RED)
                    print(f"  {status} {tool['name']}: {tool['description']}")
                else:
                    print(f"  • {tool['name']}: {tool['description']}")
        
        # Show categories summary
        if show_status:
            print(f"\n{Colors.colorize('📋 Categories Summary:', Colors.CYAN)}")
            category_stats = {}
            for cat, tool_list in categories.items():
                available_in_cat = sum(1 for t in tool_list if t['available'])
                category_stats[cat] = {'total': len(tool_list), 'available': available_in_cat}
            
            for cat, stats in sorted(category_stats.items()):
                available = stats['available']
                total = stats['total']
                print(f"  {cat}: {Colors.colorize(f'{available}/{total}', Colors.GREEN if available == total else Colors.YELLOW)}")
    
    def install_tool(self, tool_name: str) -> bool:
        """Install a tool using its install command"""
        if tool_name not in self.tools:
            print(f"{Colors.colorize(f'❌ Tool {tool_name} not found', Colors.RED)}")
            return False
        
        tool = self.tools[tool_name]
        if not tool.install_cmd:
            print(f"{Colors.colorize(f'❌ No install command for {tool_name}', Colors.RED)}")
            return False
        
        try:
            print(f"{Colors.colorize(f'📦 Installing {tool_name}...', Colors.BLUE)}")
            result = subprocess.run(tool.install_cmd.split(), 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"{Colors.colorize(f'✅ {tool_name} installed successfully', Colors.GREEN)}")
                return True
            else:
                print(f"{Colors.colorize(f'❌ Failed to install {tool_name}: {result.stderr}', Colors.RED)}")
                return False
        except Exception as e:
            print(f"{Colors.colorize(f'❌ Error installing {tool_name}: {str(e)}', Colors.RED)}")
            return False

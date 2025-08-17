#!/usr/bin/env python3
"""
Local LLM Provider for HackAI
Uses local models for AI analysis without API dependencies
"""

import json
import re
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np

# Try to import transformers, but make it optional
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
    from sentence_transformers import SentenceTransformer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  Transformers not available. Install with: pip install transformers torch sentence-transformers")

from src.ai.base import BaseAIProvider
from src.core.models import AIAnalysis

class LocalLLMProvider(BaseAIProvider):
    """Local LLM provider using transformers"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        super().__init__()
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self.embedder = None
        self._initialize()
    
    def _initialize(self):
        """Initialize local LLM models"""
        if not TRANSFORMERS_AVAILABLE:
            print("❌ Transformers not available - using fallback analysis")
            self.available = False
            return
        
        try:
            print("🤖 Loading local LLM models...")
            
            # Load text generation model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Load sentiment/classification model
            self.classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
            
            # Load sentence embedding model
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.available = True
            print("✅ Local LLM models loaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to load local LLM models: {e}")
            self.available = False
    
    def _analyze_text_with_llm(self, text: str, max_length: int = 100) -> str:
        """Generate analysis using local LLM"""
        if not self.available or not self.tokenizer or not self.model:
            return self._get_fallback_analysis_text(text)
        
        try:
            # Prepare input
            inputs = self.tokenizer.encode(text[:500], return_tensors="pt", max_length=512, truncation=True)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.strip()
            
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            return self._get_fallback_analysis_text(text)
    
    def _classify_security_risk(self, text: str) -> Dict[str, Any]:
        """Classify security risk using sentiment analysis"""
        if not self.available or not self.classifier:
            return {"risk_level": "medium", "confidence": 0.5}
        
        try:
            # Analyze sentiment
            result = self.classifier(text[:500])
            
            # Map sentiment to risk level
            sentiment = result[0]['label'].lower()
            confidence = result[0]['score']
            
            risk_mapping = {
                'positive': 'low',
                'neutral': 'medium', 
                'negative': 'high'
            }
            
            risk_level = risk_mapping.get(sentiment, 'medium')
            
            return {
                "risk_level": risk_level,
                "confidence": confidence,
                "sentiment": sentiment
            }
            
        except Exception as e:
            print(f"❌ Risk classification failed: {e}")
            return {"risk_level": "medium", "confidence": 0.5}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract security-related keywords"""
        security_keywords = [
            'vulnerability', 'exploit', 'attack', 'breach', 'malware', 'virus',
            'firewall', 'encryption', 'authentication', 'authorization',
            'sql injection', 'xss', 'csrf', 'rce', 'lfi', 'rfi',
            'port', 'service', 'protocol', 'network', 'web', 'api',
            'password', 'hash', 'crypto', 'stego', 'forensic',
            'reverse', 'debug', 'binary', 'assembly', 'shellcode'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in security_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _generate_recommendations(self, tool: str, findings: List[str], risk_level: str) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Tool-specific recommendations
        tool_recs = {
            'nmap': [
                'Review open ports and services',
                'Check for unnecessary services',
                'Verify firewall rules',
                'Update vulnerable services'
            ],
            'nuclei': [
                'Patch identified vulnerabilities',
                'Review security headers',
                'Implement WAF rules',
                'Monitor for new vulnerabilities'
            ],
            'sqlmap': [
                'Fix SQL injection vulnerabilities',
                'Use parameterized queries',
                'Implement input validation',
                'Review database permissions'
            ],
            'nikto': [
                'Update web server software',
                'Review server configuration',
                'Implement security headers',
                'Monitor access logs'
            ]
        }
        
        # Add tool-specific recommendations
        if tool in tool_recs:
            recommendations.extend(tool_recs[tool])
        
        # Risk-based recommendations
        if risk_level == 'high':
            recommendations.extend([
                'Immediate action required',
                'Implement additional monitoring',
                'Consider incident response plan',
                'Review security controls'
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                'Schedule security review',
                'Update security policies',
                'Implement monitoring',
                'Regular vulnerability assessments'
            ])
        else:
            recommendations.extend([
                'Continue monitoring',
                'Regular security updates',
                'Maintain security best practices'
            ])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analyze target using local LLM"""
        if not self.available:
            return self._get_fallback_analysis(target)
        
        try:
            # Generate analysis using LLM
            analysis_prompt = f"Analyze this security target: {target}. Provide target type, risk assessment, and recommended tools."
            analysis = self._analyze_text_with_llm(analysis_prompt, max_length=150)
            
            # Extract target type
            target_type = self._detect_target_type(target)
            
            # Assess risk
            risk_assessment = self._classify_security_risk(analysis)
            
            # Get recommended tools
            recommended_tools = self._get_recommended_tools(target_type)
            
            return {
                "target_type": target_type,
                "risk_assessment": risk_assessment["risk_level"],
                "recommended_tools": recommended_tools,
                "testing_strategy": f"Start with {recommended_tools[0] if recommended_tools else 'nmap'} for initial reconnaissance",
                "precautions": "Ensure you have proper authorization before testing",
                "ai_analysis": analysis
            }
            
        except Exception as e:
            print(f"❌ Local LLM analysis failed: {e}")
            return self._get_fallback_analysis(target)
    
    async def interpret_results(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Interpret scan results using local LLM"""
        if not self.available:
            return self._get_fallback_analysis_result(tool, output, target)
        
        try:
            # Generate summary using LLM
            summary_prompt = f"Summarize this {tool} scan result for {target}: {output[:500]}"
            summary = self._analyze_text_with_llm(summary_prompt, max_length=100)
            
            # Extract findings
            findings = self._extract_findings(tool, output)
            
            # Assess risk
            risk_assessment = self._classify_security_risk(output)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(tool, findings, risk_assessment["risk_level"])
            
            return AIAnalysis(
                summary=summary,
                findings=findings,
                recommendations=recommendations,
                risk_level=risk_assessment["risk_level"],
                confidence=risk_assessment["confidence"],
                model_used="local-llm"
            )
            
        except Exception as e:
            print(f"❌ Local LLM interpretation failed: {e}")
            return self._get_fallback_analysis_result(tool, output, target)
    
    async def generate_payloads(self, attack_type: str, target_info: Dict[str, Any]) -> List[str]:
        """Generate attack payloads using local LLM"""
        if not self.available:
            return self._get_fallback_payloads(attack_type)
        
        try:
            # Generate payloads using LLM
            payload_prompt = f"Generate {attack_type} payloads for security testing"
            payload_text = self._analyze_text_with_llm(payload_prompt, max_length=200)
            
            # Extract payloads from text
            payloads = self._extract_payloads_from_text(payload_text, attack_type)
            
            return payloads
            
        except Exception as e:
            print(f"❌ Local LLM payload generation failed: {e}")
            return self._get_fallback_payloads(attack_type)
    
    def _extract_payloads_from_text(self, text: str, attack_type: str) -> List[str]:
        """Extract payloads from generated text"""
        # Common payload patterns
        payload_patterns = {
            'sql_injection': [
                r"' OR 1=1--",
                r"'; DROP TABLE users--",
                r"' UNION SELECT NULL--",
                r"admin'--",
                r"1' AND '1'='1"
            ],
            'xss': [
                r"<script>alert\('XSS'\)</script>",
                r"<img src=x onerror=alert\('XSS'\)>",
                r"javascript:alert\('XSS'\)",
                r"<svg onload=alert\('XSS'\)>",
                r"';alert\('XSS'\);//"
            ],
            'command_injection': [
                r"; ls -la",
                r"\| whoami",
                r"&& cat /etc/passwd",
                r"`id`",
                r"\$\(whoami\)"
            ]
        }
        
        # Return predefined payloads for the attack type
        return payload_patterns.get(attack_type, [
            "test_payload_1",
            "test_payload_2",
            "test_payload_3"
        ])
    
    def _get_fallback_analysis(self, target: str) -> Dict[str, Any]:
        """Fallback analysis when LLM is not available"""
        return {
            "target_type": "unknown",
            "risk_assessment": "medium",
            "recommended_tools": ["nmap", "nuclei", "nikto"],
            "testing_strategy": "Standard security assessment",
            "precautions": "Ensure proper authorization"
        }
    
    def _get_fallback_analysis_result(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Fallback analysis result"""
        return AIAnalysis(
            summary=f"Basic analysis of {tool} results for {target}",
            findings=["Analysis completed", "Review output manually"],
            recommendations=["Implement security best practices", "Regular monitoring"],
            risk_level="medium",
            confidence=0.5,
            model_used="fallback"
        )
    
    def _get_fallback_payloads(self, attack_type: str) -> List[str]:
        """Fallback payloads"""
        return [
            f"test_{attack_type}_payload_1",
            f"test_{attack_type}_payload_2",
            f"test_{attack_type}_payload_3"
        ]
    
    def get_models(self) -> List[str]:
        """Get available local models"""
        if self.available:
            return [self.model_name, "local-sentiment", "local-embeddings"]
        return []
    
    def is_available(self) -> bool:
        """Check if local LLM is available"""
        return self.available

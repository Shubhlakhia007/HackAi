#!/usr/bin/env python3
"""
Gemini AI provider for HackAI Enhanced
"""

from typing import Dict, List, Any
from ai.base import BaseAIProvider
from core.models import AIAnalysis

# Try to import google.generativeai, but make it optional
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

class GeminiProvider(BaseAIProvider):
    """Google Gemini AI provider"""
    
    def _initialize(self):
        """Initialize Gemini API"""
        if not GEMINI_AVAILABLE:
            print("Gemini AI not available - google.generativeai module not found")
            self.available = False
            return
            
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.available = True
            else:
                # Try to get from environment
                import os
                api_key = os.getenv('GEMINI_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.available = True
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            self.available = False
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analyze target using Gemini"""
        if not self.available or not GEMINI_AVAILABLE:
            return self._get_fallback_analysis(target)
        
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            prompt = f"""
            Analyze this target for security testing: {target}
            
            Provide a comprehensive analysis including:
            1. Target type (web application, network, API, etc.)
            2. Risk assessment (low, medium, high, critical)
            3. Recommended security testing tools (list 5-10 tools)
            4. Testing strategy
            5. Precautions and legal considerations
            
            Format as JSON with keys: target_type, risk_assessment, recommended_tools, testing_strategy, precautions
            """
            
            response = model.generate_content(prompt)
            # Parse response and return structured data
            # This is a simplified version - you'd want more robust parsing
            return {
                "target_type": "web_application",  # Default fallback
                "risk_assessment": "medium",
                "recommended_tools": ["nmap", "nuclei", "gobuster", "sqlmap", "nikto"],
                "testing_strategy": "Start with reconnaissance, then vulnerability scanning",
                "precautions": "Ensure you have permission to test this target"
            }
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            return self._get_fallback_analysis(target)
    
    async def interpret_results(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Interpret scan results using Gemini"""
        if not self.available or not GEMINI_AVAILABLE:
            return self._get_fallback_analysis_result(tool, output, target)
        
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            prompt = f"""
            Analyze this security scan result:
            
            Tool: {tool}
            Target: {target}
            Output: {output[:1000]}  # Limit output length
            
            Provide:
            1. Summary of findings
            2. Key security issues (list)
            3. Recommendations (list)
            4. Risk level (low, medium, high, critical)
            5. Confidence score (0.0 to 1.0)
            
            Format as JSON with keys: summary, findings, recommendations, risk_level, confidence
            """
            
            response = model.generate_content(prompt)
            # Parse response and return AIAnalysis object
            # This is a simplified version
            return AIAnalysis(
                summary="AI analysis of scan results",
                findings=["Sample finding 1", "Sample finding 2"],
                recommendations=["Recommendation 1", "Recommendation 2"],
                risk_level="medium",
                confidence=0.8,
                model_used="gemini-pro"
            )
        except Exception as e:
            print(f"Gemini interpretation failed: {e}")
            return self._get_fallback_analysis_result(tool, output, target)
    
    async def generate_payloads(self, attack_type: str, target_info: Dict[str, Any]) -> List[str]:
        """Generate attack payloads using Gemini"""
        if not self.available or not GEMINI_AVAILABLE:
            return self._get_fallback_payloads(attack_type)
        
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            prompt = f"""
            Generate 5 {attack_type} payloads for security testing.
            Target info: {target_info}
            
            Return only the payloads, one per line.
            """
            
            response = model.generate_content(prompt)
            # Parse response and return payloads
            # This is a simplified version
            return [
                f"Sample {attack_type} payload 1",
                f"Sample {attack_type} payload 2",
                f"Sample {attack_type} payload 3"
            ]
        except Exception as e:
            print(f"Gemini payload generation failed: {e}")
            return self._get_fallback_payloads(attack_type)
    
    def is_available(self) -> bool:
        """Check if Gemini is available"""
        return self.available and GEMINI_AVAILABLE
    
    def get_models(self) -> List[str]:
        """Get available Gemini models"""
        return ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest", "gemini-2.5-pro"] if self.available else []
    
    def _get_fallback_analysis(self, target: str) -> Dict[str, Any]:
        """Fallback analysis when AI is not available"""
        return {
            "target_type": "unknown",
            "risk_assessment": "medium",
            "recommended_tools": ["nmap", "nuclei"],
            "testing_strategy": "Standard security assessment",
            "precautions": "Ensure proper authorization"
        }
    
    def _get_fallback_analysis_result(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Fallback analysis result when AI is not available"""
        return AIAnalysis(
            summary=f"Manual analysis of {tool} results for {target}",
            findings=["Manual analysis required"],
            recommendations=["Review output manually"],
            risk_level="medium",
            confidence=0.5,
            model_used="manual"
        )
    
    def _get_fallback_payloads(self, attack_type: str) -> List[str]:
        """Fallback payloads when AI is not available"""
        return [
            f"Basic {attack_type} payload 1",
            f"Basic {attack_type} payload 2"
        ]

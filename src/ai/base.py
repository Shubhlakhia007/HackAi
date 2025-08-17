#!/usr/bin/env python3
"""
Base AI provider interface for HackAI Enhanced
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from core.models import AIAnalysis

class BaseAIProvider(ABC):
    """Base class for AI providers"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model = model
        self.available = False
        self._initialize()
    
    @abstractmethod
    def _initialize(self):
        """Initialize the AI provider"""
        pass
    
    @abstractmethod
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analyze a target and provide recommendations"""
        pass
    
    @abstractmethod
    async def interpret_results(self, tool: str, output: str, target: str) -> AIAnalysis:
        """Interpret scan results using AI"""
        pass
    
    @abstractmethod
    async def generate_payloads(self, attack_type: str, target_info: Dict[str, Any]) -> List[str]:
        """Generate attack payloads"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available"""
        pass
    
    @abstractmethod
    def get_models(self) -> List[str]:
        """Get available models"""
        pass

class AIIntegrationManager:
    """Manages multiple AI providers"""
    
    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.default_provider: Optional[str] = None
    
    def add_provider(self, name: str, provider: BaseAIProvider):
        """Add an AI provider"""
        self.providers[name] = provider
        if not self.default_provider:
            self.default_provider = name
    
    def set_default_provider(self, name: str):
        """Set the default AI provider"""
        if name in self.providers:
            self.default_provider = name
    
    def get_provider(self, name: str = None) -> Optional[BaseAIProvider]:
        """Get an AI provider by name or the default one"""
        if name and name in self.providers:
            return self.providers[name]
        elif self.default_provider:
            return self.providers[self.default_provider]
        return None
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    async def analyze_target(self, target: str, provider: str = None) -> Dict[str, Any]:
        """Analyze target using specified or default provider"""
        provider_obj = self.get_provider(provider)
        if provider_obj:
            return await provider_obj.analyze_target(target)
        raise ValueError("No AI provider available")
    
    async def interpret_results(self, tool: str, output: str, target: str, provider: str = None) -> AIAnalysis:
        """Interpret results using specified or default provider"""
        provider_obj = self.get_provider(provider)
        if provider_obj:
            return await provider_obj.interpret_results(tool, output, target)
        raise ValueError("No AI provider available")
    
    async def interpret_results_with_context(self, tool: str, output: str, target: str, context: Dict[str, Any], provider: str = None) -> AIAnalysis:
        """Interpret results with additional context using specified or default provider"""
        provider_obj = self.get_provider(provider)
        if provider_obj:
            # For now, use the regular interpret_results method
            # In the future, this could be enhanced to include context
            return await provider_obj.interpret_results(tool, output, target)
        raise ValueError("No AI provider available")

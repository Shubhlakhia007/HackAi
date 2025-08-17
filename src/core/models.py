#!/usr/bin/env python3
"""
Data models for HackAI Enhanced
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ToolConfig:
    """Configuration for a security tool"""
    name: str
    command: str
    category: str
    description: str
    install_cmd: Optional[str] = None
    check_cmd: Optional[str] = None
    version_cmd: Optional[str] = None
    ai_enhanced: bool = False
    common_args: List[str] = None
    requires_target: bool = True

@dataclass
class ScanResult:
    """Result from a security scan"""
    tool: str
    target: str
    command: str
    output: str
    exit_code: int
    duration: float
    timestamp: float  # Unix timestamp
    success: bool
    session_id: str = ""
    risk_level: str = "medium"
    vulnerabilities_found: int = 0

@dataclass
class AIAnalysis:
    """AI analysis of scan results"""
    summary: str
    findings: List[str]
    recommendations: List[str]
    risk_level: str
    confidence: float
    model_used: str

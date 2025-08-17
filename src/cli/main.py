#!/usr/bin/env python3
"""
Main CLI interface for HackAI Enhanced
"""

import asyncio
import argparse
import sys
import os
import time
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.colors import Colors
from core.models import ScanResult, AIAnalysis
from database.manager import EnhancedDatabaseManager
from tools.manager import ToolManager
from ai.base import AIIntegrationManager
from ai.gemini import GeminiProvider
from ai.local import LocalAIProvider

class HackAIEnhancedCLI:
    """Main CLI interface for HackAI Enhanced"""
    
    def __init__(self):
        self.db_manager = EnhancedDatabaseManager()
        self.tool_manager = ToolManager()
        self.ai_manager = AIIntegrationManager()
        self.session_id = f"session_{int(time.time())}"
        
        # Initialize AI providers
        self._setup_ai_providers()
    
    def _setup_ai_providers(self):
        """Setup available AI providers"""
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
    
    async def run_ai_guided_scan(self, target: str, scan_type: str = "comprehensive"):
        """Run AI-guided security assessment"""
        print(f"\n{Colors.colorize(f'🤖 Starting AI-Guided Security Assessment', Colors.PURPLE)}")
        print(f"Target: {Colors.colorize(target, Colors.CYAN)}")
        print(f"Scan Type: {Colors.colorize(scan_type, Colors.CYAN)}")
        
        try:
            # AI target analysis
            print(f"\n{Colors.colorize('🔍 AI Target Analysis Phase...', Colors.BLUE)}")
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
                
                print(f"\n   {Colors.colorize(f'🔧 [{i}/{len(analysis['recommended_tools'])}] Executing {tool_name.upper()}...', Colors.BLUE)}")
                
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
                    
                    # AI interpretation
                    print(f"      {Colors.colorize('🧠 AI Analysis...', Colors.PURPLE)}")
                    
                    ai_analysis = await self.ai_manager.interpret_results(
                        tool_name, result.output, target
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
    
    def list_tools(self, category: Optional[str] = None, show_status: bool = True):
        """List available tools"""
        self.tool_manager.list_tools(category, show_status)
    
    def check_system_health(self):
        """Check system health and tool availability"""
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
        except:
            pass
        
        print(f"\n{Colors.colorize('📋 System Health Score:', Colors.CYAN)} {Colors.colorize(f'{health_score}/100', Colors.GREEN if health_score >= 75 else Colors.YELLOW if health_score >= 50 else Colors.RED)}")
    
    def install_missing_tools(self, tools: List[str] = None, install_all: bool = False):
        """Install missing tools"""
        print(f"\n{Colors.colorize('📦 Tool Installation Manager', Colors.CYAN)}")
        
        if install_all:
            missing_tools = [name for name, tool in self.tool_manager.tools.items() 
                           if not self.tool_manager.check_tool_availability().get(name, False)]
        elif tools:
            missing_tools = tools
        else:
            print(f"{Colors.colorize('❌ No tools specified for installation', Colors.RED)}")
            return
        
        if not missing_tools:
            print(f"{Colors.colorize('✅ All tools are already installed', Colors.GREEN)}")
            return
        
        print(f"{Colors.colorize(f'Installing {len(missing_tools)} missing tools...', Colors.BLUE)}")
        
        successful_installations = []
        failed_installations = []
        
        for i, tool in enumerate(missing_tools, 1):
            print(f"\n[{i}/{len(missing_tools)}] {Colors.colorize(f'Installing {tool}...', Colors.CYAN)}")
            
            if self.tool_manager.install_tool(tool):
                successful_installations.append(tool)
            else:
                failed_installations.append(tool)
        
        # Installation summary
        print(f"\n{Colors.colorize('📊 Installation Summary:', Colors.CYAN)}")
        print(f"  Successful: {Colors.colorize(str(len(successful_installations)), Colors.GREEN)}")
        print(f"  Failed: {Colors.colorize(str(len(failed_installations)), Colors.RED)}")
        
        if failed_installations:
            print(f"\n{Colors.colorize('❌ Failed installations:', Colors.RED)}")
            for tool in failed_installations:
                print(f"  • {tool}")
            print(f"\n{Colors.colorize('💡 Try running these commands manually with sudo privileges', Colors.YELLOW)}")
        
        if successful_installations:
            print(f"\n{Colors.colorize('✅ Installation complete! Run system check to verify.', Colors.GREEN)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="HackAI Enhanced - AI-Powered Penetration Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py scan example.com                    # Run AI-guided scan
  python main.py scan example.com --type stealth    # Run stealth scan
  python main.py tools --category web               # List web tools
  python main.py tools --status                     # List tools with status
  python main.py health                             # Check system health
  python main.py install --all                      # Install all missing tools
  python main.py install nmap nuclei                # Install specific tools
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Run security scan')
    scan_parser.add_argument('target', help='Target to scan')
    scan_parser.add_argument('--type', choices=['stealth', 'comprehensive', 'aggressive'], 
                           default='comprehensive', help='Scan type')
    
    # Tools command
    tools_parser = subparsers.add_parser('tools', help='Manage security tools')
    tools_parser.add_argument('--category', help='Filter by category')
    tools_parser.add_argument('--status', action='store_true', help='Show tool status')
    
    # Health command
    health_parser = subparsers.add_parser('health', help='Check system health')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install missing tools')
    install_parser.add_argument('tools', nargs='*', help='Tools to install')
    install_parser.add_argument('--all', action='store_true', help='Install all missing tools')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = HackAIEnhancedCLI()
    
    try:
        if args.command == 'scan':
            asyncio.run(cli.run_ai_guided_scan(args.target, args.type))
        elif args.command == 'tools':
            cli.list_tools(args.category, args.status)
        elif args.command == 'health':
            cli.check_system_health()
        elif args.command == 'install':
            if args.all:
                cli.install_missing_tools(install_all=True)
            elif args.tools:
                cli.install_missing_tools(args.tools)
            else:
                install_parser.print_help()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.colorize('⏹️  Operation cancelled by user', Colors.YELLOW)}")
    except Exception as e:
        print(f"\n{Colors.colorize(f'❌ Error: {str(e)}', Colors.RED)}")
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import time
    main()

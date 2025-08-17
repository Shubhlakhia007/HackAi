#!/usr/bin/env python3
"""
Database management for HackAI Enhanced
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional
from core.models import ScanResult, AIAnalysis

class EnhancedDatabaseManager:
    """Enhanced database manager for scan results and AI analysis"""
    
    def __init__(self, db_path: str = "hackai_enhanced.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize comprehensive database schema"""
        with sqlite3.connect(self.db_path) as conn:
            # Main scan results table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    tool TEXT NOT NULL,
                    target TEXT NOT NULL,
                    command TEXT NOT NULL,
                    output TEXT,
                    exit_code INTEGER,
                    duration REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER,
                    risk_level TEXT DEFAULT 'medium',
                    vulnerabilities_found INTEGER DEFAULT 0,
                    ai_analyzed INTEGER DEFAULT 0
                )
            """)
            
            # AI analysis results
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_result_id INTEGER,
                    model_used TEXT,
                    summary TEXT,
                    findings TEXT,
                    recommendations TEXT,
                    risk_assessment TEXT,
                    confidence_score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (scan_result_id) REFERENCES scan_results(id)
                )
            """)
            
            # Targets database
            conn.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT UNIQUE,
                    target_type TEXT,
                    first_scan DATETIME,
                    last_scan DATETIME,
                    total_scans INTEGER DEFAULT 0,
                    risk_score REAL DEFAULT 0.0,
                    notes TEXT
                )
            """)
            
            # Vulnerabilities database
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_result_id INTEGER,
                    vuln_type TEXT,
                    severity TEXT,
                    description TEXT,
                    cve_id TEXT,
                    cvss_score REAL,
                    remediation TEXT,
                    verified INTEGER DEFAULT 0,
                    FOREIGN KEY (scan_result_id) REFERENCES scan_results(id)
                )
            """)
            
            # Tool statistics
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tool_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_name TEXT UNIQUE,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    avg_duration REAL DEFAULT 0.0,
                    last_used DATETIME,
                    version TEXT
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scan_results_target ON scan_results(target)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scan_results_timestamp ON scan_results(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scan_results_tool ON scan_results(tool)")
    
    def save_scan_result(self, result: ScanResult, ai_analysis: Optional[AIAnalysis] = None):
        """Save scan result with optional AI analysis"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO scan_results 
                (session_id, tool, target, command, output, exit_code, duration, timestamp, success, risk_level, vulnerabilities_found, ai_analyzed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.session_id, result.tool, result.target, result.command,
                result.output, result.exit_code, result.duration, result.timestamp,
                result.success, result.risk_level, result.vulnerabilities_found,
                1 if ai_analysis else 0
            ))
            
            scan_result_id = cursor.lastrowid
            
            if ai_analysis:
                conn.execute("""
                    INSERT INTO ai_analysis 
                    (scan_result_id, model_used, summary, findings, recommendations, risk_assessment, confidence_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    scan_result_id, ai_analysis.model_used, ai_analysis.summary,
                    json.dumps(ai_analysis.findings), json.dumps(ai_analysis.recommendations),
                    ai_analysis.risk_level, ai_analysis.confidence
                ))
            
            # Update tool statistics
            self._update_tool_stats(conn, result.tool, result.success, result.duration)
            
            # Update target information
            self._update_target_info(conn, result.target)
    
    def _update_tool_stats(self, conn, tool_name: str, success: bool, duration: float):
        """Update tool usage statistics"""
        conn.execute("""
            INSERT OR REPLACE INTO tool_stats (tool_name, usage_count, success_rate, avg_duration, last_used)
            VALUES (
                ?,
                COALESCE((SELECT usage_count FROM tool_stats WHERE tool_name = ?), 0) + 1,
                CASE 
                    WHEN COALESCE((SELECT usage_count FROM tool_stats WHERE tool_name = ?), 0) = 0 THEN ?
                    ELSE (COALESCE((SELECT success_rate * usage_count FROM tool_stats WHERE tool_name = ?), 0) + ?) / 
                         (COALESCE((SELECT usage_count FROM tool_stats WHERE tool_name = ?), 0) + 1)
                END,
                CASE 
                    WHEN COALESCE((SELECT usage_count FROM tool_stats WHERE tool_name = ?), 0) = 0 THEN ?
                    ELSE (COALESCE((SELECT avg_duration * usage_count FROM tool_stats WHERE tool_name = ?), 0) + ?) / 
                         (COALESCE((SELECT usage_count FROM tool_stats WHERE tool_name = ?), 0) + 1)
                END,
                CURRENT_TIMESTAMP
            )
        """, (tool_name, tool_name, tool_name, 1.0 if success else 0.0, tool_name, 1.0 if success else 0.0, tool_name, tool_name, duration, tool_name, duration, tool_name))
    
    def _update_target_info(self, conn, target: str):
        """Update target scan information"""
        conn.execute("""
            INSERT OR REPLACE INTO targets (target, first_scan, last_scan, total_scans)
            VALUES (
                ?,
                COALESCE((SELECT first_scan FROM targets WHERE target = ?), CURRENT_TIMESTAMP),
                CURRENT_TIMESTAMP,
                COALESCE((SELECT total_scans FROM targets WHERE target = ?), 0) + 1
            )
        """, (target, target, target))
    
    def get_scan_results(self, days: int = 7, limit: int = 100):
        """Get scan results from the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT tool, target, command, output, exit_code, duration, timestamp, success, 
                       risk_level, vulnerabilities_found
                FROM scan_results 
                WHERE timestamp >= datetime('now', '-{} days')
                ORDER BY timestamp DESC 
                LIMIT ?
            """.format(days), (limit,))
            return cursor.fetchall()
    
    def get_ai_analyses(self, days: int = 7, limit: int = 50):
        """Get AI analyses from the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT sa.model_used, sa.summary, sa.findings, sa.recommendations, 
                       sa.risk_assessment, sa.confidence_score
                FROM ai_analysis sa
                JOIN scan_results sr ON sa.scan_result_id = sr.id
                WHERE sr.timestamp >= datetime('now', '-{} days')
                ORDER BY sa.timestamp DESC
                LIMIT ?
            """.format(days), (limit,))
            return cursor.fetchall()
    
    def get_database_stats(self):
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            # Total scan results
            cursor = conn.execute("SELECT COUNT(*) FROM scan_results")
            stats['total_scans'] = cursor.fetchone()[0]
            
            # Total AI analyses
            cursor = conn.execute("SELECT COUNT(*) FROM ai_analysis")
            stats['total_ai_analyses'] = cursor.fetchone()[0]
            
            # Total targets
            cursor = conn.execute("SELECT COUNT(*) FROM targets")
            stats['total_targets'] = cursor.fetchone()[0]
            
            # Database size
            cursor = conn.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            stats['db_size'] = cursor.fetchone()[0]
            
            return stats

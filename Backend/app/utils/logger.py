"""
Logger Utility
Custom logging system
"""

import os
from pathlib import Path
from datetime import datetime


class Logger:
    """
    Custom logger for application
    Demonstrates: file operations, singleton pattern
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, log_path="app/storage/logs"):
        if self._initialized:
            return
        
        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_path / "app.log"
        self._initialized = True
    
    def _write_log(self, level, message):
        """Write log entry to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass  # Logging failure shouldn't stop application
    
    def info(self, message):
        """Log info message"""
        self._write_log("INFO", message)
    
    def warning(self, message):
        """Log warning message"""
        self._write_log("WARNING", message)
    
    def error(self, message):
        """Log error message"""
        self._write_log("ERROR", message)
    
    def debug(self, message):
        """Log debug message"""
        self._write_log("DEBUG", message)


# Global logger instance
logger = Logger()


def setup_logger(log_path="app/storage/logs"):
    """Setup logger with custom path"""
    global logger
    logger = Logger(log_path)
    return logger

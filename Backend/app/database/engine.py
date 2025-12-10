"""
Custom Database Engine
File-based database with JSON storage
Demonstrates: file I/O, threading, exception handling
"""

import json
import os
from pathlib import Path
from threading import Lock
from datetime import datetime
import shutil


class DatabaseException(Exception):
    """Custom exception for database errors"""
    pass


class DatabaseEngine:
    """
    Custom file-based database engine
    Uses JSON files for storage with thread-safe operations
    """
    
    def __init__(self, storage_path="app/storage/data"):
        """
        Initialize database engine
        Args:
            storage_path: Directory path for database files
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.backup_path = self.storage_path.parent / "backups"
        self.backup_path.mkdir(exist_ok=True)
        
        self.index_path = self.storage_path.parent / "indexes"
        self.index_path.mkdir(exist_ok=True)
        
        self.log_path = self.storage_path.parent / "logs"
        self.log_path.mkdir(exist_ok=True)
        
        # Thread locks for each table
        self.locks = {}
    
    def _get_file_path(self, table_name):
        """
        Get file path for table
        Demonstrates: path manipulation
        """
        return self.storage_path / f"{table_name}.json"
    
    def _get_lock(self, table_name):
        """
        Get or create lock for table
        Demonstrates: thread safety, dictionary operations
        """
        if table_name not in self.locks:
            self.locks[table_name] = Lock()
        return self.locks[table_name]
    
    def table_exists(self, table_name):
        """Check if table exists"""
        return self._get_file_path(table_name).exists()
    
    def create_table(self, table_name):
        """
        Create new table
        Args:
            table_name: Name of table to create
        """
        file_path = self._get_file_path(table_name)
        
        if file_path.exists():
            raise DatabaseException(f"Table '{table_name}' already exists")
        
        # Create empty table file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        self._log(f"Created table: {table_name}")
    
    def drop_table(self, table_name):
        """
        Delete table
        Args:
            table_name: Name of table to delete
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            raise DatabaseException(f"Table '{table_name}' does not exist")
        
        # Create backup before deleting
        self._create_backup(table_name)
        
        # Delete file
        file_path.unlink()
        
        self._log(f"Dropped table: {table_name}")
    
    def read_table(self, table_name):
        """
        Read entire table from file
        Demonstrates: file reading, JSON parsing, exception handling
        
        Args:
            table_name: Name of table to read
        Returns:
            List of records (dictionaries)
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            # Auto-create table if it doesn't exist
            self.create_table(table_name)
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            raise DatabaseException(f"Invalid JSON in table '{table_name}': {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Error reading table '{table_name}': {str(e)}")
    
    def write_table(self, table_name, data):
        """
        Write entire table to file
        Demonstrates: file writing, JSON serialization, thread safety
        
        Args:
            table_name: Name of table to write
            data: List of records to write
        """
        if not isinstance(data, list):
            raise DatabaseException("Table data must be a list")
        
        file_path = self._get_file_path(table_name)
        lock = self._get_lock(table_name)
        
        with lock:
            try:
                # Create backup before writing
                if file_path.exists():
                    self._create_backup(table_name)
                
                # Write to temporary file first
                temp_path = file_path.with_suffix('.tmp')
                
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Atomic rename (safer than direct write)
                temp_path.replace(file_path)
                
            except Exception as e:
                # Clean up temp file if it exists
                if temp_path.exists():
                    temp_path.unlink()
                raise DatabaseException(f"Error writing table '{table_name}': {str(e)}")
    
    def _create_backup(self, table_name):
        """
        Create backup of table file
        Demonstrates: file operations, datetime formatting
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_path / f"{table_name}_{timestamp}.json"
        
        try:
            shutil.copy2(file_path, backup_file)
            
            # Keep only last 10 backups per table
            self._cleanup_old_backups(table_name, keep=10)
            
        except Exception as e:
            # Backup failure shouldn't stop operations
            self._log(f"Backup failed for {table_name}: {str(e)}", level="WARNING")
    
    def _cleanup_old_backups(self, table_name, keep=10):
        """
        Remove old backup files, keeping only the most recent
        Demonstrates: file operations, sorting, list slicing
        """
        pattern = f"{table_name}_*.json"
        backups = sorted(self.backup_path.glob(pattern))
        
        # Remove oldest backups
        if len(backups) > keep:
            for backup in backups[:-keep]:
                backup.unlink()
    
    def restore_from_backup(self, table_name, backup_timestamp=None):
        """
        Restore table from backup
        Args:
            table_name: Name of table to restore
            backup_timestamp: Specific backup timestamp, or None for latest
        """
        if backup_timestamp:
            backup_file = self.backup_path / f"{table_name}_{backup_timestamp}.json"
        else:
            # Get latest backup
            pattern = f"{table_name}_*.json"
            backups = sorted(self.backup_path.glob(pattern))
            if not backups:
                raise DatabaseException(f"No backups found for table '{table_name}'")
            backup_file = backups[-1]
        
        if not backup_file.exists():
            raise DatabaseException(f"Backup file not found: {backup_file}")
        
        file_path = self._get_file_path(table_name)
        shutil.copy2(backup_file, file_path)
        
        self._log(f"Restored table '{table_name}' from backup: {backup_file.name}")
    
    def get_table_info(self, table_name):
        """
        Get information about a table
        Returns: Dictionary with table metadata
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            return None
        
        records = self.read_table(table_name)
        stats = file_path.stat()
        
        return {
            'name': table_name,
            'record_count': len(records),
            'file_size': stats.st_size,
            'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat()
        }
    
    def list_tables(self):
        """
        List all tables in database
        Returns: List of table names
        """
        json_files = self.storage_path.glob("*.json")
        return [f.stem for f in json_files]
    
    def _log(self, message, level="INFO"):
        """
        Write to log file
        Demonstrates: file append, datetime formatting
        """
        log_file = self.log_path / "database.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {level}: {message}\n")
        except Exception:
            # Logging failure shouldn't stop operations
            pass
    
    def vacuum(self):
        """
        Optimize database by removing old backups and compacting files
        Demonstrates: file operations, iteration
        """
        for table_name in self.list_tables():
            # Cleanup old backups
            self._cleanup_old_backups(table_name, keep=5)
            
            # Rewrite table to compact JSON
            data = self.read_table(table_name)
            self.write_table(table_name, data)
        
        self._log("Database vacuum completed")
    
    def export_to_csv(self, table_name, output_path):
        """
        Export table to CSV file
        Demonstrates: CSV writing, file operations
        """
        import csv
        
        records = self.read_table(table_name)
        
        if not records:
            raise DatabaseException(f"Table '{table_name}' is empty")
        
        # Get all unique keys from all records
        keys = set()
        for record in records:
            keys.update(record.keys())
        keys = sorted(keys)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(records)
        
        self._log(f"Exported table '{table_name}' to CSV: {output_path}")
    
    def import_from_csv(self, table_name, csv_path):
        """
        Import data from CSV file
        Demonstrates: CSV reading, file operations
        """
        import csv
        
        records = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        
        # Append to existing data
        existing = self.read_table(table_name)
        existing.extend(records)
        
        self.write_table(table_name, existing)
        
        self._log(f"Imported {len(records)} records from CSV to '{table_name}'")
    
    def __repr__(self):
        return f"DatabaseEngine(storage_path='{self.storage_path}')"

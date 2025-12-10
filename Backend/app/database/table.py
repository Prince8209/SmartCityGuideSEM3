"""
Table Class with CRUD Operations
Provides ORM-like interface for database tables
"""

from datetime import datetime
from .engine import DatabaseEngine, DatabaseException


class RecordNotFoundException(DatabaseException):
    """Exception raised when record is not found"""
    pass


class Table:
    """
    Table class providing CRUD operations on database tables
    Demonstrates: OOP, encapsulation, CRUD operations
    """
    
    def __init__(self, name, engine=None):
        """
        Initialize table
        Args:
            name: Table name
            engine: DatabaseEngine instance (creates new if None)
        """
        self.name = name
        self.engine = engine or DatabaseEngine()
        self._auto_increment_id = 0
        self._load_max_id()
    
    def _load_max_id(self):
        """
        Load maximum ID for auto-increment
        Demonstrates: iteration, conditional logic
        """
        try:
            records = self.engine.read_table(self.name)
            if records:
                max_id = max(r.get('id', 0) for r in records if isinstance(r.get('id'), int))
                self._auto_increment_id = max_id
        except Exception:
            self._auto_increment_id = 0
    
    def _get_next_id(self):
        """Get next auto-increment ID"""
        self._auto_increment_id += 1
        return self._auto_increment_id
    
    def insert(self, data):
        """
        Insert new record - CREATE operation
        Demonstrates: dictionary operations, datetime handling
        
        Args:
            data: Dictionary with record data
        Returns:
            Inserted record with ID and timestamps
        """
        if not isinstance(data, dict):
            raise DatabaseException("Data must be a dictionary")
        
        records = self.engine.read_table(self.name)
        
        # Create copy to avoid modifying original
        record = data.copy()
        
        # Add ID if not present
        if 'id' not in record or record['id'] is None:
            record['id'] = self._get_next_id()
        
        # Add timestamps
        now = datetime.now().isoformat()
        if 'created_at' not in record:
            record['created_at'] = now
        record['updated_at'] = now
        
        records.append(record)
        self.engine.write_table(self.name, records)
        
        return record
    
    def insert_many(self, data_list):
        """
        Insert multiple records at once
        Args:
            data_list: List of dictionaries
        Returns:
            List of inserted records
        """
        if not isinstance(data_list, list):
            raise DatabaseException("Data must be a list")
        
        records = self.engine.read_table(self.name)
        inserted = []
        
        for data in data_list:
            record = data.copy()
            
            if 'id' not in record or record['id'] is None:
                record['id'] = self._get_next_id()
            
            now = datetime.now().isoformat()
            if 'created_at' not in record:
                record['created_at'] = now
            record['updated_at'] = now
            
            records.append(record)
            inserted.append(record)
        
        self.engine.write_table(self.name, records)
        
        return inserted
    
    def find_by_id(self, record_id):
        """
        Find record by ID - READ operation
        Demonstrates: iteration, conditional logic, exception handling
        
        Args:
            record_id: ID of record to find
        Returns:
            Record dictionary
        Raises:
            RecordNotFoundException: If record not found
        """
        records = self.engine.read_table(self.name)
        
        for record in records:
            if record.get('id') == record_id:
                return record
        
        raise RecordNotFoundException(f"Record with id {record_id} not found in table '{self.name}'")
    
    def find_one(self, filters):
        """
        Find first record matching filters
        Args:
            filters: Dictionary of field:value pairs
        Returns:
            Record dictionary or None
        """
        records = self.find_all(filters)
        return records[0] if records else None
    
    def find_all(self, filters=None):
        """
        Find all records with optional filters
        Demonstrates: iteration, conditional logic, filtering
        
        Args:
            filters: Dictionary of field:value pairs (optional)
        Returns:
            List of matching records
        """
        records = self.engine.read_table(self.name)
        
        if not filters:
            return records
        
        # Apply filters
        filtered = []
        for record in records:
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(record)
        
        return filtered
    
    def update(self, record_id, data):
        """
        Update record - UPDATE operation
        Demonstrates: list comprehension, dictionary merging
        
        Args:
            record_id: ID of record to update
            data: Dictionary with fields to update
        Returns:
            Updated record
        Raises:
            RecordNotFoundException: If record not found
        """
        if not isinstance(data, dict):
            raise DatabaseException("Data must be a dictionary")
        
        records = self.engine.read_table(self.name)
        updated_record = None
        
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                # Merge data, preserving ID and created_at
                updated = record.copy()
                updated.update(data)
                updated['id'] = record_id
                updated['created_at'] = record.get('created_at')
                updated['updated_at'] = datetime.now().isoformat()
                
                records[i] = updated
                updated_record = updated
                break
        
        if updated_record is None:
            raise RecordNotFoundException(f"Record with id {record_id} not found in table '{self.name}'")
        
        self.engine.write_table(self.name, records)
        return updated_record
    
    def update_many(self, filters, data):
        """
        Update multiple records matching filters
        Args:
            filters: Dictionary of field:value pairs
            data: Dictionary with fields to update
        Returns:
            Number of records updated
        """
        records = self.engine.read_table(self.name)
        count = 0
        
        for i, record in enumerate(records):
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            
            if match:
                updated = record.copy()
                updated.update(data)
                updated['updated_at'] = datetime.now().isoformat()
                records[i] = updated
                count += 1
        
        if count > 0:
            self.engine.write_table(self.name, records)
        
        return count
    
    def delete(self, record_id):
        """
        Delete record - DELETE operation
        Demonstrates: list comprehension, filtering
        
        Args:
            record_id: ID of record to delete
        Returns:
            True if deleted
        Raises:
            RecordNotFoundException: If record not found
        """
        records = self.engine.read_table(self.name)
        original_length = len(records)
        
        # Filter out record with matching ID
        records = [r for r in records if r.get('id') != record_id]
        
        if len(records) == original_length:
            raise RecordNotFoundException(f"Record with id {record_id} not found in table '{self.name}'")
        
        self.engine.write_table(self.name, records)
        return True
    
    def delete_many(self, filters):
        """
        Delete multiple records matching filters
        Args:
            filters: Dictionary of field:value pairs
        Returns:
            Number of records deleted
        """
        records = self.engine.read_table(self.name)
        original_length = len(records)
        
        # Filter out matching records
        filtered = []
        for record in records:
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if not match:
                filtered.append(record)
        
        count = original_length - len(filtered)
        
        if count > 0:
            self.engine.write_table(self.name, filtered)
        
        return count
    
    def count(self, filters=None):
        """
        Count records matching filters
        Args:
            filters: Dictionary of field:value pairs (optional)
        Returns:
            Number of matching records
        """
        return len(self.find_all(filters))
    
    def exists(self, filters):
        """
        Check if any record matches filters
        Args:
            filters: Dictionary of field:value pairs
        Returns:
            True if at least one record matches
        """
        return self.count(filters) > 0
    
    def truncate(self):
        """
        Delete all records from table
        Returns:
            Number of records deleted
        """
        records = self.engine.read_table(self.name)
        count = len(records)
        
        self.engine.write_table(self.name, [])
        self._auto_increment_id = 0
        
        return count
    
    def __repr__(self):
        return f"Table(name='{self.name}')"

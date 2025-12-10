"""
Base Model Class
Parent class for all models
Demonstrates: OOP inheritance, abstraction
"""

from datetime import datetime
from app.database.table import Table
from app.database.query_builder import QueryBuilder


class BaseModel:
    """
    Base model class providing common functionality
    All models inherit from this class
    """
    
    table_name = None  # Override in subclasses
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self._table = Table(self.table_name) if self.table_name else None
    
    def save(self):
        """
        Save model to database
        Demonstrates: polymorphism
        """
        if not self._table:
            raise NotImplementedError("table_name must be set in subclass")
        
        data = self.to_dict()
        
        if self.id:
            # Update existing record
            result = self._table.update(self.id, data)
        else:
            # Insert new record
            result = self._table.insert(data)
            self.id = result['id']
            self.created_at = result['created_at']
        
        self.updated_at = result['updated_at']
        return self
    
    def delete(self):
        """Delete model from database"""
        if not self.id:
            raise ValueError("Cannot delete unsaved model")
        return self._table.delete(self.id)
    
    @classmethod
    def find(cls, record_id):
        """
        Find record by ID
        Demonstrates: class methods
        """
        table = Table(cls.table_name)
        data = table.find_by_id(record_id)
        return cls(**data)
    
    @classmethod
    def find_one(cls, filters):
        """Find first record matching filters"""
        table = Table(cls.table_name)
        data = table.find_one(filters)
        return cls(**data) if data else None
    
    @classmethod
    def all(cls, filters=None):
        """Get all records"""
        table = Table(cls.table_name)
        records = table.find_all(filters)
        return [cls(**r) for r in records]
    
    @classmethod
    def query(cls):
        """Get query builder for this model"""
        return QueryBuilder(Table(cls.table_name))
    
    @classmethod
    def count(cls, filters=None):
        """Count records"""
        table = Table(cls.table_name)
        return table.count(filters)
    
    def to_dict(self):
        """
        Convert model to dictionary
        Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement to_dict()")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

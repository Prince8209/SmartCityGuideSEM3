"""
Query Builder - SQL-like query interface
Provides chainable query methods for filtering, sorting, and pagination
"""

from .table import Table


class QueryBuilder:
    """
    SQL-like query builder for custom database
    Demonstrates: method chaining, builder pattern, filtering
    """
    
    def __init__(self, table):
        """
        Initialize query builder
        Args:
            table: Table instance or table name
        """
        if isinstance(table, str):
            self.table = Table(table)
        else:
            self.table = table
        
        self._filters = []
        self._order_by_field = None
        self._order_direction = 'ASC'
        self._limit_count = None
        self._offset_count = 0
        self._select_fields = None
    
    def where(self, field, operator, value):
        """
        Add WHERE clause
        Demonstrates: method chaining, conditional logic
        
        Args:
            field: Field name
            operator: Comparison operator (=, !=, >, <, >=, <=, LIKE, IN)
            value: Value to compare
        Returns:
            self for chaining
        """
        self._filters.append((field, operator, value))
        return self
    
    def where_equal(self, field, value):
        """Shorthand for WHERE field = value"""
        return self.where(field, '=', value)
    
    def where_not_equal(self, field, value):
        """Shorthand for WHERE field != value"""
        return self.where(field, '!=', value)
    
    def where_greater(self, field, value):
        """Shorthand for WHERE field > value"""
        return self.where(field, '>', value)
    
    def where_less(self, field, value):
        """Shorthand for WHERE field < value"""
        return self.where(field, '<', value)
    
    def where_in(self, field, values):
        """WHERE field IN (values)"""
        return self.where(field, 'IN', values)
    
    def where_like(self, field, pattern):
        """WHERE field LIKE pattern (case-insensitive)"""
        return self.where(field, 'LIKE', pattern)
    
    def order_by(self, field, direction='ASC'):
        """
        Add ORDER BY clause
        Args:
            field: Field to sort by
            direction: 'ASC' or 'DESC'
        Returns:
            self for chaining
        """
        self._order_by_field = field
        self._order_direction = direction.upper()
        return self
    
    def limit(self, count):
        """
        Add LIMIT clause
        Args:
            count: Maximum number of records to return
        Returns:
            self for chaining
        """
        self._limit_count = count
        return self
    
    def offset(self, count):
        """
        Add OFFSET clause
        Args:
            count: Number of records to skip
        Returns:
            self for chaining
        """
        self._offset_count = count
        return self
    
    def select(self, *fields):
        """
        Select specific fields
        Args:
            *fields: Field names to select
        Returns:
            self for chaining
        """
        self._select_fields = fields
        return self
    
    def get(self):
        """
        Execute query and return results
        Demonstrates: iteration, filtering, sorting, slicing
        
        Returns:
            List of matching records
        """
        # Get all records
        records = self.table.find_all()
        
        # Apply filters
        for field, operator, value in self._filters:
            records = self._apply_filter(records, field, operator, value)
        
        # Apply ordering
        if self._order_by_field:
            reverse = (self._order_direction == 'DESC')
            records = sorted(
                records,
                key=lambda x: x.get(self._order_by_field, ''),
                reverse=reverse
            )
        
        # Apply offset and limit
        if self._offset_count:
            records = records[self._offset_count:]
        if self._limit_count:
            records = records[:self._limit_count]
        
        # Apply field selection
        if self._select_fields:
            records = [
                {field: record.get(field) for field in self._select_fields}
                for record in records
            ]
        
        return records
    
    def first(self):
        """
        Get first matching record
        Returns:
            First record or None
        """
        results = self.limit(1).get()
        return results[0] if results else None
    
    def count(self):
        """
        Count matching records
        Returns:
            Number of matching records
        """
        # Don't apply limit/offset for count
        records = self.table.find_all()
        
        for field, operator, value in self._filters:
            records = self._apply_filter(records, field, operator, value)
        
        return len(records)
    
    def exists(self):
        """
        Check if any records match
        Returns:
            True if at least one record matches
        """
        return self.count() > 0
    
    def _apply_filter(self, records, field, operator, value):
        """
        Apply single filter to records
        Demonstrates: conditional logic, string operations
        
        Args:
            records: List of records to filter
            field: Field name
            operator: Comparison operator
            value: Value to compare
        Returns:
            Filtered list of records
        """
        filtered = []
        
        for record in records:
            field_value = record.get(field)
            
            if operator == '=':
                if field_value == value:
                    filtered.append(record)
            
            elif operator == '!=':
                if field_value != value:
                    filtered.append(record)
            
            elif operator == '>':
                if field_value is not None and field_value > value:
                    filtered.append(record)
            
            elif operator == '<':
                if field_value is not None and field_value < value:
                    filtered.append(record)
            
            elif operator == '>=':
                if field_value is not None and field_value >= value:
                    filtered.append(record)
            
            elif operator == '<=':
                if field_value is not None and field_value <= value:
                    filtered.append(record)
            
            elif operator == 'LIKE':
                if field_value and value.lower() in str(field_value).lower():
                    filtered.append(record)
            
            elif operator == 'IN':
                if field_value in value:
                    filtered.append(record)
            
            elif operator == 'NOT IN':
                if field_value not in value:
                    filtered.append(record)
        
        return filtered
    
    def paginate(self, page=1, per_page=10):
        """
        Paginate results
        Args:
            page: Page number (1-indexed)
            per_page: Records per page
        Returns:
            Dictionary with pagination info and data
        """
        total = self.count()
        total_pages = (total + per_page - 1) // per_page  # Ceiling division
        
        offset = (page - 1) * per_page
        records = self.offset(offset).limit(per_page).get()
        
        return {
            'data': records,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    
    def __repr__(self):
        return f"QueryBuilder(table='{self.table.name}')"


class QueryHelper:
    """
    Helper class for common query patterns
    Demonstrates: static methods, utility functions
    """
    
    @staticmethod
    def search(table, search_term, fields):
        """
        Search across multiple fields
        Args:
            table: Table instance
            search_term: Term to search for
            fields: List of field names to search in
        Returns:
            List of matching records
        """
        query = QueryBuilder(table)
        
        # This is a simplified OR search
        # In a real implementation, we'd need proper OR support
        all_results = []
        seen_ids = set()
        
        for field in fields:
            results = QueryBuilder(table).where_like(field, search_term).get()
            for record in results:
                if record.get('id') not in seen_ids:
                    all_results.append(record)
                    seen_ids.add(record.get('id'))
        
        return all_results
    
    @staticmethod
    def find_recent(table, limit=10, date_field='created_at'):
        """
        Find most recent records
        Args:
            table: Table instance
            limit: Number of records to return
            date_field: Field to sort by
        Returns:
            List of recent records
        """
        return QueryBuilder(table).order_by(date_field, 'DESC').limit(limit).get()

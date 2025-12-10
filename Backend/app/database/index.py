"""
Index Manager for Fast Lookups
Uses Binary Search Tree for indexing
"""

import json
from pathlib import Path
from app.data_structures.binary_search_tree import BinarySearchTree


class IndexManager:
    """
    Manages indexes for fast lookups using BST
    Demonstrates: BST usage, file operations, indexing
    """
    
    def __init__(self, table_name, index_path="app/storage/indexes"):
        """
        Initialize index manager
        Args:
            table_name: Name of table to index
            index_path: Directory for index files
        """
        self.table_name = table_name
        self.index_path = Path(index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory indexes (BST for each indexed field)
        self.indexes = {}
    
    def create_index(self, field_name, records=None):
        """
        Create index on a field using BST
        Demonstrates: BST usage, iteration
        
        Args:
            field_name: Field to index
            records: List of records to index (optional)
        """
        bst = BinarySearchTree()
        
        if records:
            for record in records:
                key = record.get(field_name)
                if key is not None:
                    record_id = record.get('id')
                    
                    # BST stores key -> list of record IDs (for non-unique fields)
                    existing = bst.search(key)
                    if existing:
                        if record_id not in existing:
                            existing.append(record_id)
                        bst.insert(key, existing)
                    else:
                        bst.insert(key, [record_id])
        
        self.indexes[field_name] = bst
        self._save_index(field_name)
    
    def add_to_index(self, record):
        """
        Add record to all indexes
        Args:
            record: Record dictionary to index
        """
        record_id = record.get('id')
        
        for field_name, bst in self.indexes.items():
            key = record.get(field_name)
            if key is not None:
                existing = bst.search(key)
                if existing:
                    if record_id not in existing:
                        existing.append(record_id)
                    bst.insert(key, existing)
                else:
                    bst.insert(key, [record_id])
        
        # Save updated indexes
        for field_name in self.indexes:
            self._save_index(field_name)
    
    def remove_from_index(self, record):
        """
        Remove record from all indexes
        Args:
            record: Record dictionary to remove
        """
        record_id = record.get('id')
        
        for field_name, bst in self.indexes.items():
            key = record.get(field_name)
            if key is not None:
                existing = bst.search(key)
                if existing and record_id in existing:
                    existing.remove(record_id)
                    if existing:
                        bst.insert(key, existing)
                    else:
                        bst.delete(key)
        
        # Save updated indexes
        for field_name in self.indexes:
            self._save_index(field_name)
    
    def lookup(self, field_name, key):
        """
        Fast lookup using index
        Demonstrates: BST search, O(log n) lookup
        
        Args:
            field_name: Indexed field name
            key: Key to search for
        Returns:
            List of record IDs matching key
        """
        if field_name not in self.indexes:
            return []
        
        result = self.indexes[field_name].search(key)
        return result if result else []
    
    def range_lookup(self, field_name, min_key, max_key):
        """
        Range lookup using index
        Args:
            field_name: Indexed field name
            min_key: Minimum key (inclusive)
            max_key: Maximum key (inclusive)
        Returns:
            List of record IDs in range
        """
        if field_name not in self.indexes:
            return []
        
        # Get all items in sorted order
        items = self.indexes[field_name].inorder_traversal()
        
        record_ids = []
        for key, ids in items:
            if min_key <= key <= max_key:
                record_ids.extend(ids)
        
        return record_ids
    
    def drop_index(self, field_name):
        """
        Drop index on field
        Args:
            field_name: Field to drop index for
        """
        if field_name in self.indexes:
            del self.indexes[field_name]
            
            # Delete index file
            index_file = self._get_index_file(field_name)
            if index_file.exists():
                index_file.unlink()
    
    def list_indexes(self):
        """
        List all indexed fields
        Returns:
            List of field names
        """
        return list(self.indexes.keys())
    
    def _get_index_file(self, field_name):
        """Get path to index file"""
        return self.index_path / f"{self.table_name}_{field_name}.json"
    
    def _save_index(self, field_name):
        """
        Save index to file
        Demonstrates: file writing, BST serialization
        """
        if field_name not in self.indexes:
            return
        
        bst = self.indexes[field_name]
        index_data = bst.inorder_traversal()
        
        index_file = self._get_index_file(field_name)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
    
    def _load_index(self, field_name):
        """
        Load index from file
        Demonstrates: file reading, BST reconstruction
        """
        index_file = self._get_index_file(field_name)
        
        if not index_file.exists():
            return None
        
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        bst = BinarySearchTree()
        for key, value in index_data:
            bst.insert(key, value)
        
        return bst
    
    def load_all_indexes(self):
        """Load all indexes from files"""
        for index_file in self.index_path.glob(f"{self.table_name}_*.json"):
            field_name = index_file.stem.replace(f"{self.table_name}_", "")
            bst = self._load_index(field_name)
            if bst:
                self.indexes[field_name] = bst
    
    def rebuild_indexes(self, records):
        """
        Rebuild all indexes from records
        Args:
            records: List of all records
        """
        for field_name in list(self.indexes.keys()):
            self.create_index(field_name, records)
    
    def __repr__(self):
        return f"IndexManager(table='{self.table_name}', indexes={self.list_indexes()})"

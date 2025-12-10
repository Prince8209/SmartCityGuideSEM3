"""
Custom Hash Table Implementation
Used for: Fast lookups, caching, indexing
Average Time Complexity: O(1) for insert, search, delete
"""


class HashTable:
    """
    Custom Hash Table using separate chaining for collision resolution
    Demonstrates: hashing, collision handling, load factor management
    """
    
    def __init__(self, initial_size=100):
        self.size = initial_size
        self.table = [[] for _ in range(self.size)]
        self._count = 0
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """
        Hash function to convert key to index
        Demonstrates: abstraction, string/number handling
        """
        if isinstance(key, str):
            # String hashing using polynomial rolling hash
            hash_value = 0
            for i, char in enumerate(key):
                hash_value += ord(char) * (31 ** i)
            return hash_value % self.size
        elif isinstance(key, int):
            return key % self.size
        else:
            # For other types, use Python's built-in hash
            return hash(key) % self.size
    
    def put(self, key, value):
        """
        Insert or update key-value pair - O(1) average
        Args:
            key: Hashable key
            value: Associated value
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self._count += 1
        
        # Check if resize needed
        if self._load_factor() > self.load_factor_threshold:
            self._resize()
    
    def get(self, key, default=None):
        """
        Get value by key - O(1) average
        Args:
            key: Key to search for
            default: Default value if key not found
        Returns:
            Value associated with key, or default
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def delete(self, key):
        """
        Delete key-value pair - O(1) average
        Returns: True if deleted, False if not found
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return True
        
        return False
    
    def contains(self, key):
        """Check if key exists in hash table"""
        return self.get(key) is not None
    
    def _load_factor(self):
        """Calculate current load factor"""
        return self._count / self.size
    
    def _resize(self):
        """
        Resize hash table when load factor exceeds threshold
        Demonstrates: dynamic resizing, rehashing
        """
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self._count = 0
        
        # Rehash all existing items
        for bucket in old_table:
            for key, value in bucket:
                self.put(key, value)
    
    def keys(self):
        """Return list of all keys"""
        result = []
        for bucket in self.table:
            for k, v in bucket:
                result.append(k)
        return result
    
    def values(self):
        """Return list of all values"""
        result = []
        for bucket in self.table:
            for k, v in bucket:
                result.append(v)
        return result
    
    def items(self):
        """Return list of all (key, value) tuples"""
        result = []
        for bucket in self.table:
            for k, v in bucket:
                result.append((k, v))
        return result
    
    def clear(self):
        """Remove all items"""
        self.table = [[] for _ in range(self.size)]
        self._count = 0
    
    def is_empty(self):
        """Check if hash table is empty"""
        return self._count == 0
    
    def __len__(self):
        """Return number of items"""
        return self._count
    
    def __contains__(self, key):
        """Support 'in' operator"""
        return self.contains(key)
    
    def __getitem__(self, key):
        """Support bracket notation for getting: table[key]"""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value
    
    def __setitem__(self, key, value):
        """Support bracket notation for setting: table[key] = value"""
        self.put(key, value)
    
    def __delitem__(self, key):
        """Support del operator: del table[key]"""
        if not self.delete(key):
            raise KeyError(f"Key '{key}' not found")
    
    def __repr__(self):
        items = self.items()
        return f"HashTable({dict(items)})"
    
    def __str__(self):
        items = {k: v for k, v in self.items()}
        return f"HashTable({items})"


class LRUCache:
    """
    Least Recently Used Cache using HashTable
    Demonstrates: practical application of hash table
    """
    
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.cache = HashTable(capacity)
        self.access_order = []  # Track access order
    
    def get(self, key):
        """Get value and mark as recently used"""
        value = self.cache.get(key)
        
        if value is not None:
            # Move to end (most recently used)
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
        
        return value
    
    def put(self, key, value):
        """Put value and evict least recently used if needed"""
        # If key exists, update and mark as recently used
        if key in self.cache:
            self.cache.put(key, value)
            self.access_order.remove(key)
            self.access_order.append(key)
            return
        
        # If cache is full, evict least recently used
        if len(self.cache) >= self.capacity:
            lru_key = self.access_order.pop(0)
            self.cache.delete(lru_key)
        
        # Add new item
        self.cache.put(key, value)
        self.access_order.append(key)
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_order = []
    
    def __len__(self):
        return len(self.cache)

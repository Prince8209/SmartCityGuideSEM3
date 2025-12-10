"""
Custom LinkedList Implementation
Used for: Itinerary items, user history, ordered collections
"""


class Node:
    """Node class for LinkedList - demonstrates OOP encapsulation"""
    
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """
    Custom LinkedList implementation from scratch
    Demonstrates: OOP, iteration, conditional execution
    """
    
    def __init__(self):
        self.head = None
        self._size = 0
    
    def append(self, data):
        """
        Add element to end of list - O(n)
        Demonstrates: iteration, conditional logic
        """
        new_node = Node(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self._size += 1
    
    def prepend(self, data):
        """Add element to beginning - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def insert_at(self, index, data):
        """Insert element at specific index"""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current = self.head
        
        for i in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def delete(self, data):
        """
        Delete first occurrence of element
        Returns: True if deleted, False if not found
        """
        if not self.head:
            return False
        
        # If head needs to be deleted
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        
        # Search for element
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at(self, index):
        """Delete element at specific index"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.head = self.head.next
            self._size -= 1
            return
        
        current = self.head
        for i in range(index - 1):
            current = current.next
        
        current.next = current.next.next
        self._size -= 1
    
    def find(self, data):
        """
        Find element and return its node
        Returns: Node if found, None otherwise
        """
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None
    
    def get(self, index):
        """Get element at specific index"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        current = self.head
        for i in range(index):
            current = current.next
        
        return current.data
    
    def to_list(self):
        """Convert LinkedList to Python list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def reverse(self):
        """Reverse the linked list in place"""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def clear(self):
        """Clear all elements"""
        self.head = None
        self._size = 0
    
    def is_empty(self):
        """Check if list is empty"""
        return self.head is None
    
    def __len__(self):
        """Return size of list - demonstrates magic methods"""
        return self._size
    
    def __iter__(self):
        """Make LinkedList iterable - demonstrates iterator protocol"""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def __repr__(self):
        """String representation"""
        items = self.to_list()
        return f"LinkedList({items})"
    
    def __str__(self):
        """User-friendly string representation"""
        items = " -> ".join(str(item) for item in self)
        return f"[{items}]" if items else "[]"

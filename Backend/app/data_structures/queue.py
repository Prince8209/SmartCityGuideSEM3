"""
Custom Queue Implementation (FIFO - First In First Out)
Used for: Request processing, task scheduling, breadth-first search
"""


class Queue:
    """
    Custom Queue implementation using Python list
    Demonstrates: FIFO principle, basic queue operations
    """
    
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        """
        Add item to rear of queue - O(1)
        Args:
            item: Any data to add to queue
        """
        self._items.append(item)
    
    def dequeue(self):
        """
        Remove and return front item - O(n) but acceptable for small queues
        Returns:
            Front item from queue
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from empty queue")
        return self._items.pop(0)
    
    def front(self):
        """
        Return front item without removing - O(1)
        Returns:
            Front item from queue
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek empty queue")
        return self._items[0]
    
    def rear(self):
        """
        Return rear item without removing - O(1)
        Returns:
            Rear item from queue
        """
        if self.is_empty():
            raise IndexError("Cannot peek empty queue")
        return self._items[-1]
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self._items) == 0
    
    def size(self):
        """Return number of items in queue"""
        return len(self._items)
    
    def clear(self):
        """Remove all items from queue"""
        self._items = []
    
    def to_list(self):
        """Return queue contents as list (front to rear)"""
        return self._items.copy()
    
    def __len__(self):
        """Return queue size"""
        return len(self._items)
    
    def __bool__(self):
        """Return True if queue is not empty"""
        return not self.is_empty()
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Queue({self._items})"
    
    def __str__(self):
        """User-friendly representation"""
        if self.is_empty():
            return "Queue: []"
        items = " <- ".join(str(item) for item in self._items)
        return f"Queue: [FRONT {items} REAR]"


class PriorityQueue:
    """
    Priority Queue implementation
    Items with higher priority are dequeued first
    Demonstrates: advanced data structure, sorting
    """
    
    def __init__(self):
        self._items = []  # List of (priority, item) tuples
    
    def enqueue(self, item, priority=0):
        """
        Add item with priority
        Args:
            item: Data to add
            priority: Priority level (higher = more important)
        """
        self._items.append((priority, item))
        # Keep sorted by priority (descending)
        self._items.sort(key=lambda x: x[0], reverse=True)
    
    def dequeue(self):
        """
        Remove and return highest priority item
        Returns:
            Highest priority item
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from empty priority queue")
        priority, item = self._items.pop(0)
        return item
    
    def front(self):
        """Return highest priority item without removing"""
        if self.is_empty():
            raise IndexError("Cannot peek empty priority queue")
        return self._items[0][1]
    
    def is_empty(self):
        """Check if priority queue is empty"""
        return len(self._items) == 0
    
    def size(self):
        """Return number of items"""
        return len(self._items)
    
    def clear(self):
        """Remove all items"""
        self._items = []
    
    def __len__(self):
        return len(self._items)
    
    def __repr__(self):
        return f"PriorityQueue({self._items})"


class CircularQueue:
    """
    Circular Queue with fixed size
    Demonstrates: array-based implementation, modulo arithmetic
    """
    
    def __init__(self, max_size=10):
        self.max_size = max_size
        self._items = [None] * max_size
        self._front = 0
        self._rear = -1
        self._count = 0
    
    def enqueue(self, item):
        """Add item to circular queue"""
        if self.is_full():
            raise OverflowError("Queue is full")
        
        self._rear = (self._rear + 1) % self.max_size
        self._items[self._rear] = item
        self._count += 1
    
    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self.max_size
        self._count -= 1
        return item
    
    def front(self):
        """Return front item"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[self._front]
    
    def is_empty(self):
        """Check if queue is empty"""
        return self._count == 0
    
    def is_full(self):
        """Check if queue is full"""
        return self._count == self.max_size
    
    def size(self):
        """Return current size"""
        return self._count
    
    def __len__(self):
        return self._count

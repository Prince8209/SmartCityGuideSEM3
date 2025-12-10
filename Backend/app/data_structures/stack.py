"""
Custom Stack Implementation (LIFO - Last In First Out)
Used for: Undo/redo operations, backtracking, expression evaluation
"""


class Stack:
    """
    Custom Stack implementation using Python list
    Demonstrates: LIFO principle, exception handling
    """
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """
        Add item to top of stack - O(1)
        Args:
            item: Any data to push onto stack
        """
        self._items.append(item)
    
    def pop(self):
        """
        Remove and return top item - O(1)
        Returns:
            Top item from stack
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        """
        Return top item without removing - O(1)
        Returns:
            Top item from stack
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """
        Check if stack is empty
        Demonstrates: conditional execution
        """
        return len(self._items) == 0
    
    def size(self):
        """Return number of items in stack"""
        return len(self._items)
    
    def clear(self):
        """Remove all items from stack"""
        self._items = []
    
    def to_list(self):
        """Return stack contents as list (top to bottom)"""
        return self._items[::-1]
    
    def __len__(self):
        """Return stack size - demonstrates magic methods"""
        return len(self._items)
    
    def __bool__(self):
        """Return True if stack is not empty"""
        return not self.is_empty()
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Stack({self._items})"
    
    def __str__(self):
        """User-friendly representation"""
        if self.is_empty():
            return "Stack: []"
        items = " | ".join(str(item) for item in reversed(self._items))
        return f"Stack: [TOP {items} BOTTOM]"


class UndoRedoStack:
    """
    Specialized stack for undo/redo operations
    Demonstrates: inheritance, practical application
    """
    
    def __init__(self, max_size=50):
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.max_size = max_size
    
    def do_action(self, action):
        """
        Perform new action
        Args:
            action: Action to perform (dict with 'type' and 'data')
        """
        self.undo_stack.push(action)
        self.redo_stack.clear()  # Clear redo stack on new action
        
        # Limit stack size
        if self.undo_stack.size() > self.max_size:
            # Remove oldest action (bottom of stack)
            temp = Stack()
            while self.undo_stack.size() > 1:
                temp.push(self.undo_stack.pop())
            self.undo_stack.clear()
            while not temp.is_empty():
                self.undo_stack.push(temp.pop())
    
    def undo(self):
        """
        Undo last action
        Returns:
            Action that was undone
        """
        if self.undo_stack.is_empty():
            raise IndexError("Nothing to undo")
        
        action = self.undo_stack.pop()
        self.redo_stack.push(action)
        return action
    
    def redo(self):
        """
        Redo last undone action
        Returns:
            Action that was redone
        """
        if self.redo_stack.is_empty():
            raise IndexError("Nothing to redo")
        
        action = self.redo_stack.pop()
        self.undo_stack.push(action)
        return action
    
    def can_undo(self):
        """Check if undo is available"""
        return not self.undo_stack.is_empty()
    
    def can_redo(self):
        """Check if redo is available"""
        return not self.redo_stack.is_empty()

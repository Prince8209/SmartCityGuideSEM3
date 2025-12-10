"""
Custom Binary Search Tree Implementation
Used for: Indexing, fast lookups, sorted data storage
Average Time Complexity: O(log n) for search, insert, delete
"""


class TreeNode:
    """Node class for Binary Search Tree"""
    
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value is not None else key
        self.left = None
        self.right = None
    
    def __repr__(self):
        return f"TreeNode(key={self.key}, value={self.value})"


class BinarySearchTree:
    """
    Custom Binary Search Tree implementation
    Demonstrates: recursion, tree traversal, OOP
    """
    
    def __init__(self):
        self.root = None
        self._size = 0
    
    def insert(self, key, value=None):
        """
        Insert key-value pair into BST
        Args:
            key: Comparable key for ordering
            value: Associated value (defaults to key)
        """
        if value is None:
            value = key
        
        if self.root is None:
            self.root = TreeNode(key, value)
            self._size += 1
        else:
            self._insert_recursive(self.root, key, value)
    
    def _insert_recursive(self, node, key, value):
        """
        Recursive insertion - demonstrates recursion
        """
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_recursive(node.right, key, value)
        else:
            # Update existing key
            node.value = value
    
    def search(self, key):
        """
        Search for key in BST
        Returns: Value if found, None otherwise
        Demonstrates: conditional execution, recursion
        """
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        """Recursive search"""
        if node is None:
            return None
        
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def contains(self, key):
        """Check if key exists in BST"""
        return self.search(key) is not None
    
    def delete(self, key):
        """
        Delete key from BST
        Returns: True if deleted, False if not found
        """
        if not self.contains(key):
            return False
        
        self.root = self._delete_recursive(self.root, key)
        self._size -= 1
        return True
    
    def _delete_recursive(self, node, key):
        """Recursive deletion"""
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node to delete found
            
            # Case 1: No children
            if node.left is None and node.right is None:
                return None
            
            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Case 3: Two children
            # Find minimum in right subtree
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.key)
        
        return node
    
    def _find_min(self, node):
        """Find minimum node in subtree"""
        while node.left is not None:
            node = node.left
        return node
    
    def _find_max(self, node):
        """Find maximum node in subtree"""
        while node.right is not None:
            node = node.right
        return node
    
    def min_key(self):
        """Get minimum key in tree"""
        if self.root is None:
            return None
        return self._find_min(self.root).key
    
    def max_key(self):
        """Get maximum key in tree"""
        if self.root is None:
            return None
        return self._find_max(self.root).key
    
    def inorder_traversal(self):
        """
        Inorder traversal (Left -> Root -> Right)
        Returns sorted list of (key, value) tuples
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self):
        """
        Preorder traversal (Root -> Left -> Right)
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        """Recursive preorder traversal"""
        if node:
            result.append((node.key, node.value))
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        """
        Postorder traversal (Left -> Right -> Root)
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        """Recursive postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append((node.key, node.value))
    
    def height(self):
        """Get height of tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Recursive height calculation"""
        if node is None:
            return 0
        return 1 + max(
            self._height_recursive(node.left),
            self._height_recursive(node.right)
        )
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None
    
    def size(self):
        """Return number of nodes"""
        return self._size
    
    def clear(self):
        """Remove all nodes"""
        self.root = None
        self._size = 0
    
    def to_dict(self):
        """Convert BST to dictionary"""
        result = {}
        for key, value in self.inorder_traversal():
            result[key] = value
        return result
    
    def __len__(self):
        return self._size
    
    def __contains__(self, key):
        """Support 'in' operator"""
        return self.contains(key)
    
    def __repr__(self):
        items = self.inorder_traversal()
        return f"BinarySearchTree({items})"

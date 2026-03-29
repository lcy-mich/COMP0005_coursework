# Scapegoat tree by Logan
# A scapegoat tree is a type of self-balancing BST
# Unlike AVl, it does NOT rebalance on every insert
# Rather, is occasionally rebuids the entire subtree

# Essentially, after inserting into a node:
# 1. Check if the tree is "too deep"
# 2. If yes, find an unbalanced ancestor (scapegoat)
# 3. Rebuild that subtree into a balanced BST

import time
import random
import string

class Node:
    def __init__ (self, key):
        self.key   = key
        self.left  = None
        self.right = None

class ScapegoatTree:
    def __init__ (self, alpha=2/3):
        self.root     = None
        self.n        = 0 # the current number of nodes in the tree
        self.max_size = 0
        self.alpha    = alpha
        # Alpha = 2/3 means that no subtree can be
        # more than ~66% of the tree's total size
        # therefore changing alpha affects performance trade-offs
        # between rebuilding frequency and tree height

    # Standard BST insertion without balancing
    # "path" is used to trace to the root of the subtree (the scapegoat)
    def _insert (self, node, key, path):
        if node is None:
            new_node = Node(key)
            path.append(new_node)
            return new_node
        
        path.append(node)
        
        if key < node.key:
            node.left  = self._insert(node.left, key, path)
        else:
            node.right = self._insert(node.right, key, path)

        return node
    
    # Finds the root / scapegoat node by tracking from bottom to top
    def _find_scapegoat (self, path):
        for i in range (len(path)-1, -1, -1):
            node = path[i]
            left_size  = self._size(node.left)
            right_size = self._size(node.right)
            total_size = 1 + left_size + right_size

            if max(left_size, right_size) > self.alpha * total_size:
                return i
        return None
    
    # Returns the total number of nodes in a subtree
    def _size (self, node):
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)
    
    # Convert a tree into a list in sorted order
    def _in_order (self, node, arr):
        if node is None:
            return
        self._in_order(node.left, arr)
        arr.append(node)
        self._in_order(node.right, arr)

    # Takes a sorted list of nodes and builds a perfectly balanced BST
    def _build_balanced_tree (self, nodes, start, end):
        if start > end:
            return None
        
        mid  = (start+end) // 2
        root = nodes[mid]

        root.left  = self._build_balanced_tree(nodes, start, mid-1)
        root.right = self._build_balanced_tree(nodes, mid+1, end)

        return root
    
    # Rebuild subtree
    def _rebuild (self, node):
        nodes = []
        self._in_order(node, nodes)
        return self._build_balanced_tree(nodes, 0, len(nodes)-1)
    
    # Returns the tree's height
    def _height (self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))
    
    # Computes the maximum allowed height depending on alpha
    # Due to library restrictions, logarithms were approximated using iterative multiplication.
    # As a result it may be slightly less accurate
    def _log_alpha (self, n):
        if n <= 1:
            return 0
        
        height = 0
        value  = 1
        base   = 1 / self.alpha

        while value < n:
            value *= base
            height += 1
        
        return height
    
    # Standard BST insert but updates size and checks if the tree is too tall
    # If yes, then it rebuilds the whole tree
    def insert (self, key):
        path = []
        self.root = self._insert(self.root, key, path)

        self.n += 1
        self.max_size = max(self.max_size, self.n)
        
        if len(path) > self._log_alpha(self.n):
            scapegoat_index = self._find_scapegoat(path)

            if scapegoat_index is not None:
                scapegoat = path[scapegoat_index]

                # rebuild the subtree
                new_subtree = self._rebuild(scapegoat)

                # attach to its parent node
                if scapegoat_index == 0:
                    self.root = new_subtree
                else:
                    parent = path[scapegoat_index - 1]

                    if parent.left == scapegoat:
                        parent.left = new_subtree
                    else:
                        parent.right = new_subtree

    # Standard BST search
    def search (self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False


# Simple Tests
tree = ScapegoatTree()

tree.insert("mango")
tree.insert("apple")
tree.insert("banana")

print("Search for 'apple': ", tree.search("apple")) # True
print("Search for 'grape': ", tree.search("grape")) # False

# ----------------------------------------

tree2 = ScapegoatTree()

numInserts = 100

for i in range(numInserts):
    tree2.insert(str(i))

print("Height of the tree after ", numInserts, " inserts: ", tree2._height(tree2.root))

# ----------------------------------------

tree3 = ScapegoatTree()

start = time.time()

for i in range(1000):
    tree3.insert(str(i))

end = time.time()

print("Insert time: ", end - start)

# ----------------------------------------

def random_string(length=5):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

tree4 = ScapegoatTree()

data = [random_string() for _ in range(100)]

for s in data:
    tree4.insert(s)

# Verify that all of the strings actually exist
print("All strings exist? ", all(tree4.search(s) for s in data))
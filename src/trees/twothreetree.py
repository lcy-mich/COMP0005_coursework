# made w/ <3 by me
# might be a little ugly but i like to convince myself its pretty
# ts took me 3 hours to grind... im either stupid or maybe its cus i shower too often

class multi_key_node:
    
    parent : multi_key_node | None
    keys : list[str]
    children : list[multi_key_node] | None 

    def __init__(self, parent : multi_key_node | None, keys : list[str], children : list[multi_key_node] | None):
        self.parent = parent
        self.keys = keys
        self.children = children

        if self.children:
            for child in self.children:
                if child:
                    child.parent = self

    def insertKey(self, index : int, newKey : str) -> None:
        self.keys.insert(index, newKey)

    def addKey(self, newKey : str) -> None:
        self.keys.append(newKey)
        self.keys.sort()

    def appendChild(self, child : multi_key_node) -> None:
        if not self.children: self.children = []
        self.children.append(child)

    def insertChild(self, index : int, child : multi_key_node) -> None:
        if not self.children : self.children = []
        self.children.insert(index, child)
    
    def childIndex(self) -> int:
        assert self.parent
        return self.parent.children.index(self) if self.parent.children else -1

    def hasChildren(self) -> bool:
        return self.childCount() > 0
    
    def childCount(self) -> int:
        return len(self.children) if self.children else 0
    
    def isTwoNode(self) -> bool:
        return len(self.keys) == 1
    
    def isThreeNode(self) -> bool:
        return len(self.keys) == 2
    
    def isTempFourNode(self) -> bool:
        return len(self.keys) == 3
    
    def getKey(self) -> str:
        assert self.isTwoNode()
        return self.keys[0]
    
    def getLeftKey(self) -> str:
        assert self.isThreeNode() or self.isTempFourNode()
        return self.keys[0]
    
    def getRightKey(self) -> str:
        assert self.isThreeNode() or self.isTempFourNode()
        return self.keys[-1]
    
    def getMidKey(self) -> str:
        assert self.isTempFourNode()
        return self.keys[1]
    
    def getLeft(self) -> multi_key_node | None:
        if self.children and self.childCount() >= 2:
            return self.children[0]
        return None
    
    def getRight(self) -> multi_key_node | None:
        if self.children and self.childCount() >= 2:
            return self.children[-1]
        return None
    
    def getMid(self) -> multi_key_node | None:
        if self.children and self.isThreeNode():
            return self.children[1]
        return None
    
    def getMidLeft(self) -> multi_key_node | None:
        if self.children and self.isTempFourNode():
            return self.children[1]
        return None
    
    def getMidRight(self) -> multi_key_node | None:
        if self.children and self.isTempFourNode():
            return self.children[2]
        return None
    
    def hasKey(self, *keys : str) -> bool:
        for key in keys:
            if key in self.keys:
                return True
        return False

class two_three_tree:
    def __init__(self, root_key : str | None):
        self.root = multi_key_node(parent=None, keys=[root_key], children=None) if root_key else None
        # self.mem = {}

    # def memoize(self, f):
    #     def inner(self, val):
    #         if val not in self.mem:
    #             self.mem[val] = f(val)
    #         return self.mem[val]
    #     return inner

    def get(self, needle : str , node : multi_key_node | None = None, returnLastFound : bool = False) -> multi_key_node | None:
        # compare search key against those in node
        # find interval containing search key
        # follow associated link (recursively)

        if not node: # initial setup to start search from root
            return self.get(needle, self.root, returnLastFound) 
        
        if node.hasKey(needle): # check if node is correct
            return node
        
        if not node.hasChildren(): # check children exist
            return node if returnLastFound else None

        if node.isTwoNode():
            if needle < node.getKey():
                return self.get(needle, node.getLeft(), returnLastFound)
            else:
                return self.get(needle, node.getRight(), returnLastFound)
            
        if node.isThreeNode():            
            leftKey = node.getLeftKey()
            rightKey = node.getRightKey()
            
            if needle < leftKey:
                return self.get(needle, node.getLeft(), returnLastFound)
            if needle > rightKey:
                return self.get(needle, node.getRight(), returnLastFound)
            else:
                return self.get(needle, node.getMid(), returnLastFound)
            
    def splitChildren(self, node : multi_key_node, parent : multi_key_node, index : int) -> multi_key_node:
        assert node.isTempFourNode()

        leftChild = multi_key_node(
            parent = parent,
            keys=[node.getLeftKey()], 
            children = []
        )
        if node.getLeft(): leftChild.appendChild(node.getLeft())  # type: ignore
        if node.getMidLeft(): leftChild.appendChild(node.getMidLeft()) # type: ignore

        rightChild = multi_key_node(
            parent = parent, 
            keys=[node.getRightKey()],
            children = []
        )
        if node.getMidRight(): rightChild.appendChild(node.getMidRight())  # type: ignore
        if node.getRight(): rightChild.appendChild(node.getRight()) # type: ignore

        if parent.children:
            parent.children.pop(index)
        parent.insertChild(index, leftChild)
        parent.insertChild(index + 1, rightChild)
        del node
        return parent

    def put(self, newKey : str):
        # cases
        # case 1 :
        #   insert new key in a 2-node
        #       transform 2-node into a 3-node
        # case 2 :
        #   insert the new key in a 3-node
        #       add new key to a 3-node to make temp 4-node
        #       move middle key of 4-node into its parent node
        #       repeat up the tree as necessary
        #       if you reach the root and it's a 4-node, split into 3 2-nodes
        #          

        if self.root == None:
            self.root = multi_key_node(parent=None, keys=[newKey], children=None)
            return

        lastNode : multi_key_node = self.get(newKey, returnLastFound = True) # type: ignore
        assert lastNode #should always exist

        if lastNode.hasKey(newKey):
            return #already in tree
        
        if lastNode.isTwoNode():
            lastNode.addKey(newKey)
            return
        
        lastNode.addKey(newKey)

        while lastNode and lastNode.isTempFourNode():
            midKey = lastNode.getMidKey()

            if not lastNode.parent: # lastnode is root node
                newRoot = multi_key_node(parent = None, keys=[midKey], children=None)
                leftChild = multi_key_node(parent=newRoot, keys=[lastNode.getLeftKey()], children=[])
                rightChild = multi_key_node(parent=newRoot, keys=[lastNode.getRightKey()], children=[])
                if lastNode.getLeft():
                    leftChild.appendChild(lastNode.getLeft()) # type: ignore
                if lastNode.getMidLeft():
                    leftChild.appendChild(lastNode.getMidLeft()) # type: ignore
                if lastNode.getMidRight():
                    rightChild.appendChild(lastNode.getMidRight()) # type: ignore
                if lastNode.getRight():
                    rightChild.appendChild(lastNode.getRight()) # type: ignore
                newRoot.children = [leftChild, rightChild]
                self.root = newRoot
                break

            parent = lastNode.parent
            childIndex = lastNode.childIndex()
            parent.insertKey(childIndex, midKey)
                            
            self.splitChildren(lastNode, lastNode.parent, childIndex)
            lastNode = lastNode.parent

        
        



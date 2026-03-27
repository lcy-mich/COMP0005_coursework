# thanks to Ricky Zhang for making this
# all i changed was insertElement -> put and searchElement -> get

class LLRBBSTNode:
    def __init__(self, element):
        self.element = element
        self.is_red = True
        self.left = None
        self.right = None


class LLRBBST(AbstractSearchInterface):
    def __init__(self):
        self.root = None

    def _rotate_left(self, n):
        x = n.right
        n.right = x.left
        x.left = n
        x.is_red = n.is_red
        n.is_red = True
        return x

    def _rotate_right(self, n):
        x = n.left
        n.left = x.right
        x.right = n
        x.is_red = n.is_red
        n.is_red = True
        return x

    def _flip_color(self, n):
        n.is_red = True
        n.left.is_red = False
        n.right.is_red = False

    def _put(self, n, element):
        inserted = False

        if n.element == element:
            return n, False
        elif element < n.element:
            if n.left:
                n.left, inserted = self._put(n.left, element)
            else:
                n.left = LLRBBSTNode(element)
                inserted = True
        elif element > n.element:
            if n.right:
                n.right, inserted = self._put(n.right, element)
            else:
                n.right = LLRBBSTNode(element)
                inserted = True

        if n.right and n.right.is_red and (n.left is None or not n.left.is_red):
            n = self._rotate_left(n)
        if n.left and n.left.left and n.left.is_red and n.left.left.is_red:
            n = self._rotate_right(n)
        if n.left and n.right and n.left.is_red and n.right.is_red:
            self._flip_color(n)

        return n, inserted

    def _get(self, n, element):
        if n.element == element:
            return True
        elif element < n.element and n.left:
            return self._get(n.left, element)
        elif element > n.element and n.right:
            return self._get(n.right, element)
        else:
            return False

    def put(self, element):
        if self.root is None:
            self.root = LLRBBSTNode(element)
            return True
        self.root, inserted = self._put(self.root, element)
        return inserted

    def get(self, element):
        if self.root is None:
            return False
        return self._get(self.root, element)

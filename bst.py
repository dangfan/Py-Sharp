class treeNode:
    def __init__(self, key = None, data = None, left = None, right = None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right

class binarySearchTree:
    def __init__(self):
        self.root = None

    def search(self, key):
        return self.__search(self.root, key)

    def __search(self, node, key):
        if node == None:
            return None
        if key < node.key:
            return self.__search(node.left, key)
        elif key > node.key:
            return self.__search(node.right, key)
        else:
            return node

    def insert(self, key, data):
        self.root = self.__insert(self.root, key, data)

    def __insert(self, node, key, data):
        if node == None:
            return treeNode(key, data)
        if key < node.key:
            node.left = self.__insert(node.left, key, data)
        elif key > node.key:
            node.right = self.__insert(node.right, key, data)
        return node

    def travel(self):
        self.items = []
        self.__travel(self.root)
        return self.items

    def __travel(self, node):
        if node != None:
            self.__travel(node.left)
            self.items.append(node.data)
            self.__travel(node.right)

i, t = 0, binarySearchTree()
while i < 10:
    t.insert(i * 3, 'd' + str(i))
    i = i + 1
print t.travel()
for i in xrange(1, 10):
    t.insert(i * 2, 't' + str(i))
print t.travel()
if 2 in xrange(1, 10):
    for i in xrange(1, 10):
        t.insert(i, 'f' + str(i))
print t.travel()
print t.search(-1)
print t.search(4).data

# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
      tree
      ----
        1    <-- root
     /     \
    2       3
  /   \    / \
 4     5  6   7    <-- leaves

 This is a complete tree (all node are as left as possible)

 A tree with all nodes either have 2 or 0 children

 Traversal:
    process of visiting(checking || updating) each node

    Orders:
        Depth-first search(DFS):
            Pre-order:      1 -> 2 -> 4 -> 5 -> 3 -> 6 -> 7
                Start from root, keep going to left, if can't go left anymore, move one to right

            In-order:       4 -> 2 -> 5 -> 1 -> 6 -> 3 -> 7
                Start from deepest left node, then move to the right

            Post-order:     4 -> 2 -> 5 -> 6 -> 3 -> 7 -> 1
                Start from left, then move to right, then move to root.


        Breadth-first search(BFS):
            Level-order traversal:      1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
                Using queue to enqueue(append first) and dequeue(pop last)
                --> [1] (pop 1 || append leaves under 1)
                --> [3, 2] (pop 2 || append leaves under 2)
                --> [6, 7, 3] (pop 3 || append leaves under 3)
                --> [4, 5, 6, 7]

            Reverse level-order traversal:      4 -> 5 -> 6 -> 7 -> 2 -> 3 -> 1
                Reading from left to right || Using Queue and stack
                --> Push the root to the stack and enqueue root's leaves from right to left
                    stack: [1]                      Queue: [2, 3]
                --> Dequeue 3 and push it to stack and enqueue(reversed) it's child
                    stack: [1, 3]                   Queue: [2, 7, 6]
                --> Dequeue 2 and push it to stack and enqueue(reversed) it's child
                    stack: [1, 3, 2]                Queue: [7, 6, 5, 4]
                --> Dequeue 7 and push it to stack
                    stack: [1, 3, 2, 7]             Queue: [6, 5, 4]
                --> Dequeue 6 and push it to stack
                    stack: [1, 3, 2, 7, 6]          Queue: [5, 4]
                --> Repeat
                    stack: [1, 3, 2, 7, 6, 5, 4]
                --> Pop from the stack

Height:
    Height is 2 (count the # of arrows/edges) || 1 -> 2 -> 4

Size:
    Traverse through the tree
"""


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        return self.stack[-1].value

    def __len__(self):
        return self.size()

    def size(self):
        return len(self.stack)


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.insert(0, item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop()

    def is_empty(self):
        return not self.queue

    def peek(self):
        return self.queue[-1].value

    def __len__(self):
        return self.size()

    def size(self):
        return len(self.queue)


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        # points to left child
        self.right = None
        # points to right child


class Tree:
    def __init__(self, root):
        self.root = Node(root)
        # convert data passed in and setting it to the root of the tree

    def print_tree(self, traversal_type):
        if traversal_type == "preorder":
            return self.pre_order_print(self.root, "")
        elif traversal_type == "inorder":
            return self.in_order_print(self.root, "")
        elif traversal_type == "postorder":
            return self.post_order_print(self.root, "")
        elif traversal_type == "levelorder":
            return self.level_order_print(self.root)
        elif traversal_type == "rlevelorder":
            return self.reverse_level_order_print(self.root)
        else:
            print(f"Traversal type {traversal_type} unsupported")
            return False

    def pre_order_print(self, start, traversal):
        """Root --> Left --> Right"""
        if start:
            # if it's not None
            traversal += (str(start.value) + " -> ")
            print(traversal)

            traversal = self.pre_order_print(start.left, traversal)
            # recurse to deepest left leaf,
            # if start.left = None, returns traversal itself,
            # if start.left != None, add start.left to traversal and continue recusing

            traversal = self.pre_order_print(start.right, traversal)
            # recurse to the right leaf, if start.right = None, returns traversal itself

        return traversal

    def pre_order_print_2(self, node):
        # more concise
        if node:
            return f"{node.value} -> {self.pre_order_print_2(node.left)}{self.pre_order_print_2(node.right)}"
        return ""

    def in_order_print(self, start, traversal):
        """Left --> Root --> Right"""
        if start:
            traversal = self.in_order_print(start.left, traversal)

            traversal += (str(start.value) + " -> ")
            print(traversal)

            traversal = self.in_order_print(start.right, traversal)
        return traversal

    def in_order_print_2(self, node):
        # more concise
        if node:
            return f"{self.in_order_print_2(node.left)}{node.value} -> {self.in_order_print_2(node.right)}"
        return ""

    def post_order_print(self, start, traversal):
        """Left --> Right --> Root"""
        if start:
            traversal = self.post_order_print(start.left, traversal)
            traversal = self.post_order_print(start.right, traversal)

            traversal += (str(start.value) + " -> ")
            print(traversal)
        return traversal

    def post_order_print_2(self, node):
        # more concise
        if node:
            return f"{self.post_order_print_2(node.left)}{self.post_order_print_2(node.right)}{node.value} -> "
        return ""

    @staticmethod
    def level_order_print(start):
        """top left --> bottom right"""
        if start:
            queue = Queue()
            queue.enqueue(start)

            traversal = ""
            while len(queue):
                traversal += str(queue.peek()) + " -> "
                print(traversal)

                node = queue.dequeue()
                if node.left:
                    queue.enqueue(node.left)
                if node.right:
                    queue.enqueue(node.right)
            return traversal

    @staticmethod
    def reverse_level_order_print(start):
        """bottom left --> top right"""
        if start:
            queue = Queue()
            queue.enqueue(start)

            stack = Stack()
            traversal = ""
            while len(queue):
                node = queue.dequeue()
                stack.push(node)

                if node.right:
                    queue.enqueue(node.right)
                if node.left:
                    queue.enqueue(node.left)

            while len(stack):
                node = stack.pop()
                traversal += str(node.value) + " -> "
                print(traversal)

            return traversal

    def height(self, start):
        if start:
            l_height = self.height(start.left)
            r_height = self.height(start.right)
            return 1 + max(l_height, r_height)
        return -1

    def get_height(self):
        return print(self.height(self.root))

    def size(self):
        if self.root:
            stack = Stack()
            stack.push(self.root)

            size = 1
            while stack:
                node = stack.pop()
                if node.left:
                    stack.push(node.left)
                    size += 1
                if node.right:
                    stack.push(node.right)
                    size += 1
            print(size)
            return size
        return 0

    def recursive_size(self, node):
        if node:
            return 1 + self.recursive_size(node.left) + self.recursive_size(node.right)
        return 0


"""
         1
       /   \
      2     3
     / \   / \
    4   5 6   7
"""

tree = Tree(1)
# initialize the Tree with root value of 2

tree.root.left = Node(2)
tree.root.right = Node(3)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)
tree.root.right.left = Node(6)
tree.root.right.right = Node(7)

tree.print_tree("preorder")
print(tree.pre_order_print_2(tree.root))
tree.print_tree("inorder")
print(tree.in_order_print_2(tree.root))
tree.print_tree("postorder")
print(tree.post_order_print_2(tree.root)) # not working
tree.print_tree("levelorder")
tree.print_tree("rlevelorder")

tree.get_height()
print(tree.height(tree.root))
# both will work

tree.size()
print(tree.recursive_size(tree.root))

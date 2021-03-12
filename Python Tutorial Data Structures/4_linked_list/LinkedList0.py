class Node(object):

    def __init__(self, d, n=None):
        self.data = d
        self.next_node = n

    def get_next(self):
        return self.next_node

    def set_next(self, n):
        self.next_node = n

    def get_data(self):
        return self.data

    def set_data(self, d):
        self.data = d


class LinkedList(object):

    def __init__(self, r=None):
        self.root = r
        self.size = 0

    def get_size(self):
        return self.size

    def display(self):
        l = []
        this_node = self.root
        while this_node:
            l.append(this_node.get_data())
            this_node = this_node.get_next()
            # move on to the next node
        print(l)

    def add_front(self, d):
        new_node = Node(d, self.root)
        self.root = new_node
        self.size += 1

    def remove(self, d):
        this_node = self.root
        prev_node = None

        while this_node:
            if this_node.get_data() == d:
                # found data to be removed
                if prev_node:
                    # if prev_node is not None
                    prev_node.set_next(this_node.get_next())
                    # disconnect this node and connect next node with previous node
                else:
                    # if prev_node is None
                    self.root = this_node.get_next()
                    # it's the 1st node to be removed, so no previous node
                self.size -= 1
                return "Removed"
            else:
                prev_node = this_node
                # backup previous node
                this_node = this_node.get_next()
                # move forward 1 node
        return "Not found"

    def find(self, d):
        this_node = self.root
        while this_node:
            if this_node.get_data() == d:
                return d
            else:
                this_node = this_node.get_next()
        return None


myList = LinkedList()
myList.add_front(5)
myList.add_front(8)
myList.add_front(12)
myList.display()
print("size = " + str(myList.get_size()))
myList.remove(8)
print("size = " + str(myList.get_size()))
print(myList.remove(12))
print("size = " + str(myList.get_size()))
print(myList.find(5))

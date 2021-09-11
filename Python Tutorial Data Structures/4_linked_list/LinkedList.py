# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

class node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class linked_list:
    def __init__(self):
        self.head = node()
        self.size = 0

    def append(self, data):
        self.size += 1
        new_node = node(data)
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            # advance 1 node forward
        cur.next = new_node
        # connect the next node with this node

    def length(self):
        return self.size

    def display(self):
        elems = []
        cur_node = self.head
        while cur_node.next is not None:
            cur_node = cur_node.next
            elems.append(cur_node.data)
        print(elems)

    def printMiddle(self):
        count = 0
        mid = self.head
        heads = self.head

        while heads is not None:
            # Update mid, when 'count'
            # is odd number
            if count & 1:
                mid = mid.next
            count += 1
            heads = heads.next

        # If empty list is provided
        if mid is not None:
            print("The middle element is ", mid.data)


my_list = linked_list()

for i in [2, 5, 2, 465, 123, 6, 2, 8, 6, 5, 64]:
    my_list.append(i)

print("length: ", my_list.length())
my_list.printMiddle()
my_list.display()

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_front(self, node):
        node.prev = None
        node.next = self.head

        if self.head:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node

    def move_to_front(self, node):
        if self.head is node:
            return

        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if self.tail is node:
            self.tail = node.prev

        #mover al frente
        node.prev = None
        node.next = self.head

        if self.head:
            self.head.prev = node
        self.head = node

    def pop_back(self):
        if not self.tail:
            return None
        node = self.tail
        if self.tail == self.head:
            self.head = None
            self.tail = None
        else:
            self.tail = node.prev
            self.tail.next = None
        node.prev = None
        return node
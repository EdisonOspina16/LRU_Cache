from typing import Generic, TypeVar
T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList(Generic[T]):

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

        node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if not node.next:
            self.tail = node.prev
        node.prev = None
        self.add_to_front(node)

    def pop_back(self):
        if not self.tail:
            return None
        if self.tail == self.head:
            node = self.head
            self.tail = None
            self.head = None
            return node
        tail = self.tail
        self.tail = tail.prev
        self.tail.next = None
        return tail

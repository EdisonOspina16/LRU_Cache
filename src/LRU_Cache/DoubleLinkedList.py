from typing import Generic, TypeVar
T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next: DoublyLinkedList | None = None
        self.prev: DoublyLinkedList | None = None


class DoublyLinkedList(Generic[T]):
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_front(self, node):
        if not self.head:
            self.head = node
            self.tail = node
            return

        self.head.prev = node
        node.next = self.head
        self.head = node

    def move_to_front(self, node):

        if self.head is node:
            return

        node.prev.next = node.next
        if node.next:
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

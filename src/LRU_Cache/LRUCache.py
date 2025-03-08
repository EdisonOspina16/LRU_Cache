from DoubleLinkedList import DoublyLinkedList
from DoubleLinkedList import Node


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = dict()
        self.list = DoublyLinkedList()
        self.len = 0

    def get(self, key):
        node = self.cache.get(key)
        if node is not None:
            self.list.move_to_front(node)
            return node.value
        else:
            return None

    def put(self, key, value):
        node = self.cache.get(key)
        if node is not None:
            node.value = value
            self.list.move_to_front(node)
            return

        if self.len >= self.capacity:
            node_to_drop = self.list.pop_back()
            if not node_to_drop:
                return
            del (self.cache[node_to_drop.key])
            self.len -= 1

        new_node = Node(key, value)
        self.cache[key] = new_node
        self.list.add_to_front(new_node)
        self.len += 1

from DoubleLinkedList import DoublyLinkedList


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = dict()
        self.queue = DoublyLinkedList()
        self.len = 0

    def get(self, key):
        node = self.cache.get(key)
        if node is not None:
            self.queue.move_to_front(node)
            return node.value
        else:
            return -1

    def put(self, key, value):
        node = self.cache.get(key)
        if node is not None:
            node.value = value
            self.queue.move_to_front(node)
            return

        if self.len >= self.capacity:
            node_to_drop = self.queue.pop_back()
            if not node_to_drop:
                return
            del (self.cache[node_to_drop.key])
            self.len -= 1

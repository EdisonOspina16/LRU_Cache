from DoubleLinkedList import DoublyLinkedList
from DoubleLinkedList import Node


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = dict()
        self.list = DoublyLinkedList()
        self.size = 0

    def get(self, key):
        node = self.cache.get(key)
        if node is not None:
            self.list.move_to_front(node)
            return node.value
        return None

    def put(self, key, value):
        node = self.cache.get(key)
        if node is not None:
            # si la clave ya existe, actualiza el valor y moverlo al frente
            node.value = value
            self.list.move_to_front(node)
            return

        if self.size >= self.capacity:
            #si la cache esta llena, elimina el menos usado (tail)
            node_to_remove = self.list.pop_back()
            if\
                    node_to_remove:
                del (self.cache[node_to_remove.key])
                self.size -= 1

        #agregar nuevo nodo al frente
        new_node = Node(key, value)
        self.cache[key] = new_node
        self.list.add_to_front(new_node)
        self.size += 1
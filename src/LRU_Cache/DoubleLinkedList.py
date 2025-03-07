class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None  # punteros al nodo anterior y siguiente en la lista.
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None  # referencia al primer nodo
        self.tail = None   # referencia al ultimo nodo

    def add_to_front(self, node):  # Inserta un nodo al inicio de la lista
        node.prev = None
        node.next = self.head  # Conectar el nuevo nodo al head actual

        if self.head:
            self.head.prev = node  # Asegurar que el head actual apunte al nuevo nodo

        self.head = node  # Actualizar head al nuevo nodo

        if self.tail is None:  # Si la lista estaba vacía, tail también debe apuntar al nuevo nodo
            self.tail = node

    def move_to_front(self, node):

        if self.head is node:  # Si el nodo ya esta al frente, no hacemos nada
            return

        node.prev.next = node.next
        if node.next:  # Si no es el ultimo
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

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None  #punteros al nodo anterior y siguiente en la lista.
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None  #referencia al primer nodo
        self.tail = None   #referencia al ultimo nodo

    def add_to_front(self, node):  #Inserta un nodo al inicio de la lista
        if not self.head:   #verifica si la lista esta vacia
            self.head = node
            self.tail = node
            return

        self.head.prev = node #Se asigna el nodo previo del nodo que es actualmente head
        node.next = self.head #nuevo nodo apunta al head
        self.head = node #nodo se convierte en el nuevo head

    def move_to_front(self, node):
        if self.head is node:
            return
        node.prev.next = node.next
        if node.next: #Si no es el ultimo
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












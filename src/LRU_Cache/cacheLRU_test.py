import unittest
from DoubleLinkedList import DoublyLinkedList
from LRUCache import LRUCache
from DoubleLinkedList import Node


class TestNode(unittest.TestCase):
    def test_node_creation(self):
        node = Node(1, 'A')
        self.assertEqual(node.key, 1)
        self.assertEqual(node.value, 'A')
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = DoublyLinkedList()

    def test_add_to_front(self):
        node = Node(1, 'A')
        self.list.add_to_front(node)
        self.assertEqual(self.list.head, node)
        self.assertEqual(self.list.tail, node)

    def test_move_to_front(self):
        node1 = Node(1, 'A')
        node2 = Node(2, 'B')
        self.list.add_to_front(node1)
        self.list.add_to_front(node2)
        self.list.move_to_front(node1)
        self.assertEqual(self.list.head, node1)

    def test_pop_back(self):
        node1 = Node(1, 'A')
        node2 = Node(2, 'B')
        self.list.add_to_front(node1)
        self.list.add_to_front(node2)
        popped_node = self.list.pop_back()
        self.assertEqual(popped_node, node1)
        self.assertEqual(self.list.tail, node2)

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(capacity=2)

    def test_put_and_get(self):
        self.cache.put(1, 'A')
        self.assertEqual(self.cache.get(1), 'A')

    def test_cache_eviction(self):
        self.cache.put(1, 'A')
        self.cache.put(2, 'B')
        self.cache.put(3, 'C')  # Debería remover el 1
        self.assertIsNone(self.cache.get(1))
        self.assertEqual(self.cache.get(2), 'B')
        self.assertEqual(self.cache.get(3), 'C')

    def test_update_existing_key(self):
        self.cache.put(1, 'A')
        self.cache.put(1, 'Updated')
        self.assertEqual(self.cache.get(1), 'Updated')

if __name__ == '__main__':
    unittest.main()

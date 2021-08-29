from bst import Bst, BstNodeFindLocation
import random
import timeit
import unittest


class TestBst(unittest.TestCase):

    def test_insert(self):
        bst = Bst()
        self.assertTrue(bst.insert(5))
        self.assertFalse(bst.insert(5))

    def test_contains(self):
        bst = Bst()
        self.assertFalse(5 in bst)
        bst.insert(5)
        self.assertFalse(4 in bst)
        self.assertTrue(5 in bst)
        self.assertFalse(6 in bst)

    def test_count(self):
        bst = Bst()
        self.assertEqual(len(bst), 0)
        bst.insert(5)
        self.assertEqual(len(bst), 1)
        bst.insert(5)

    def test_delete_random(self):
        bst = TestBst.setup_bst()
        values_to_delete = {value for value in bst}
        while len(bst) > 0:
            value_to_delete = values_to_delete.pop()
            self.assertIsNotNone(bst.find(value_to_delete).node)
            del bst[value_to_delete]
            self.assertIsNone(bst.find(value_to_delete).node)
        self.assertEqual(len(values_to_delete), 0)

    def test_delete_root(self):
        bst = TestBst.setup_bst(3)
        bst.balance()
        while bst.root is not None:
            value = bst.root.value
            self.assertEqual(bst.find(value).location, BstNodeFindLocation.FOUND_SELF)
            del bst[value]
            self.assertEqual(bst.find(value).location, BstNodeFindLocation.NOT_FOUND)

    def test_enumerate(self):
        bst = Bst()
        length = 7
        random_values = random.sample(range(length), length)
        sorted_values = [iteration for iteration in range(length)]
        for random_value in random_values:
            bst.insert(random_value)
        enumerated_values = list()
        for node in bst:
            enumerated_values.append(node)
        self.assertTrue(all(sorted_value == enumerated_value for sorted_value, enumerated_value in zip(sorted_values, enumerated_values)))

    def test_find(self):
        bst = Bst()
        self.assertEqual(bst.find(5).location, BstNodeFindLocation.NOT_FOUND)
        bst.insert(5)
        bst.insert(6)
        bst.insert(4)
        self.assertEqual(bst.find(3).location, BstNodeFindLocation.NOT_FOUND)
        self.assertEqual(bst.find(3).node, None)
        self.assertEqual(bst.find(4).location, BstNodeFindLocation.FOUND_ON_LEFT)
        self.assertEqual(bst.find(4).node, bst.root)
        self.assertEqual(bst.find(5).location, BstNodeFindLocation.FOUND_SELF)
        self.assertEqual(bst.find(5).node, bst.root)
        self.assertEqual(bst.find(6).location, BstNodeFindLocation.FOUND_ON_RIGHT)
        self.assertEqual(bst.find(6).node, bst.root)
        self.assertEqual(bst.find(7).location, BstNodeFindLocation.NOT_FOUND)
        self.assertEqual(bst.find(7).node, None)

    @staticmethod
    def ideal_node_count(depth):
        """
        Returns the ideal count of nodes that will result in a perfectly balanced tree
        :param depth: The desired depth of the tree
        :return: The ideal count of nodes
        """
        if depth == 0:
            return 0
        if depth == 1:
            return 1
        return TestBst.ideal_node_count(depth - 1) * 2 + 1

    @staticmethod
    def setup_bst(depth=6):
        """
        Sets up a `Bst` with a random set of nodes that, when balanced, results in the desired depth
        :param depth: The depth of the resulting `Bst`, after balancing
        :return: Returns a `Bst` with a random set of nodes that, when balanced, results in the desired depth
        """
        bst = Bst()
        node_count = TestBst.ideal_node_count(depth)
        values = random.sample(range(node_count * 2), node_count)
        for value in values:
            if not bst.insert(value):
                raise ValueError(f'{value} has already been inserted!')
        return bst


def profile_bst_balance(iterations=10000):
    """
    Tests the Bst.balance() method
    :param iterations: The number of iterations to profile
    """
    setup = '''
from bst_tests import TestBst
import logging
logging.disable(logging.WARNING)
bst = TestBst.setup_bst()
    '''
    test_code = '''
bst.balance()
    '''
    print(f'bst_balance performance: {timeit.timeit(stmt=test_code, setup=setup, number=iterations)}s')


def perform_balance(bst):
    """
    Performs a balance of the input bst
    :param bst: The tree to balance
    """
    print("Before balance")
    bst.print_tree()
    bst.balance()
    print("After balance")
    bst.print_tree()

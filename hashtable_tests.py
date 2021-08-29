from hashtable import HashTable
import random
import timeit
import unittest


class TestHashTable(unittest.TestCase):

    def test_setitem_and_count(self):
        hashtable = HashTable()
        self.assertEqual(len(hashtable), 0)
        hashtable["5"] = 5
        self.assertEqual(len(hashtable), 1)
        hashtable["6"] = 6
        self.assertEqual(len(hashtable), 2)
        hashtable["5"] = 5
        self.assertEqual(len(hashtable), 2)

    def test_getitem(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertEqual(hashtable["5"], 5)

    def test_contains(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertTrue("5" in hashtable)

    def test_delete(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertEqual(hashtable["5"], 5)
        del hashtable["5"]
        self.assertIsNone(hashtable["5"])

    def test_set_none(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertEqual(hashtable["5"], 5)
        hashtable["5"] = None
        self.assertIsNone(hashtable["5"])

    def test_iteration(self):
        # Set up the table, with keys and values
        hashtable = HashTable()
        values = [value for value in range(10)]
        keys = [f'{values}' for values in values]
        for key, value in zip(keys, values):
            hashtable[key] = value
        # Now test the actual iteration
        for pair in hashtable:
            self.assertTrue(pair[0] in keys)
            self.assertTrue(pair[1] in values)

    def test_keys(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertEqual(hashtable.keys, {"5"})

    def test_values(self):
        hashtable = HashTable()
        hashtable["5"] = 5
        self.assertEqual(hashtable.values, [5])

    def test_load_factor(self):
        bucket_increment = 32
        # Try 3 different load factors that hit edge cases with the bucket count
        for load_factor in [0.74, 0.75, 0.76]:
            # Set up the hashtable with the desired load_factor and bucket_increment
            hashtable = HashTable(load_factor, bucket_increment)
            self.assertEqual(len(hashtable._HashTable__buckets), bucket_increment)
            # Add just enough items to remain within the load factor with respect to the existing bucket_increment
            limit = int(bucket_increment / load_factor)
            for index in range(limit):
                hashtable[f'{index}'] = index
            self.assertEqual(len(hashtable._HashTable__buckets), bucket_increment)
            # Now add one more item and watch the bucket count increase by the bucket_increment
            hashtable[f'{limit}'] = limit
            self.assertEqual(len(hashtable._HashTable__buckets), bucket_increment * 2)

    @staticmethod
    def setup_hashtable(items, load_factor):
        values = random.sample(range(items), items)
        keys = [f'{values}' for values in values]
        hashtable = HashTable(load_factor)
        for index in range(items):
            hashtable[keys[index]] = values[index]
        return hashtable

    @staticmethod
    def confirm_hashtable(hashtable, keys, values):
        # First verify the count
        if len(hashtable) != len(keys) != len(values):
            return False
        # Now verify that the values for all keys match
        if not all((hashtable[key] == value for key, value in zip(keys, values))):
            return False
        # Next, verify removals
        even_keys = keys[::2]
        odd_keys = keys[1::2]
        for key in odd_keys:
            del hashtable[key]
        if not all((key not in hashtable for key in odd_keys)):
            return False
        if not all((key in hashtable for key in even_keys)):
            return False
        # Finally, verify the reduced count
        even_values = values[::2]
        if len(hashtable) != len(even_keys) != len(even_values):
            return False
        # Finally, verify what's left
        if not all((hashtable[key] == value for key, value in zip(even_keys, even_values))):
            return False
        # All tests passed
        return True


def profile_hashtable(iterations=10000):
    """
    Tests the HashTable class
    :param iterations: The number of iterations to profile
    """
    setup = '''
from hashtable_tests import TestHashTable
import logging
logging.disable(logging.WARNING)
    '''
    test_code = '''
hashtable = TestHashTable.setup_hashtable(44, 0.7)  # this will result in 1 re-balance
keys = list()
values = list()
for pair in hashtable:
    keys.append(pair[0])
    values.append(pair[1])
TestHashTable.confirm_hashtable(hashtable, keys, values)
    '''
    print(f'HashTable performance: {timeit.timeit(stmt=test_code, setup=setup, number=iterations)}s')

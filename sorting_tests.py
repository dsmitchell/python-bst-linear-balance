import random
import sorting
import timeit
import unittest


class TestSorting(unittest.TestCase):

    def test_bubble_sort(self):
        random_list = self.setup_list(99)
        sorting.bubble_sort(random_list)
        self.assertTrue(self.confirm_sort(random_list))

    def test_merge_sort(self):
        random_list = self.setup_list(99)
        sorting.merge_sort(random_list)
        self.assertTrue(self.confirm_sort(random_list))

    def test_sort_performance(self):
        results = self.profile_sorting()
        self.assertGreater(results[0], results[1])

    @staticmethod
    def setup_list(length):
        """
        Sets up a randomly ordered list using the provided length
        :param length: The desired length of the list
        :return: Returns the randomly ordered list containing `length` elements
        """
        return random.sample(range(length), length)

    @staticmethod
    def confirm_sort(elements):
        """
        Confirms that the input list of elements is sorted, where the index of the element equals the value of the element
        :param elements: The input list of elements
        :return: Returns True if every element's value matches the index of the element. Otherwise False
        """
        return all((index == element for index, element in enumerate(elements)))

    @staticmethod
    def profile_sorting(iterations=1000):
        """
        Tests the performance of the bubble_sort() and merge_sort() methods
        :param iterations: The number of iterations to profile
        """
        setup = '''
import sorting
from sorting_tests import TestSorting
        '''
        test_code = '''
elements = TestSorting.setup_list(99)
sorting.bubble_sort(elements)
        '''
        bubble_sort_performance = timeit.timeit(stmt=test_code, setup=setup, number=iterations)
        test_code = '''
elements = TestSorting.setup_list(99)
sorting.merge_sort(elements)
        '''
        merge_sort_performance = timeit.timeit(stmt=test_code, setup=setup, number=iterations)
        return bubble_sort_performance, merge_sort_performance

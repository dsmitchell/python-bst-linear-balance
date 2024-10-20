# This python script demonstrates the linear-time BST balancing algorithm
import logging

from bst_tests import TestBst, perform_balance, profile_bst_balance


def test_trees():
    bst = TestBst.setup_bst(6)
    perform_balance(bst)
    perform_balance(bst)
    profile_bst_balance()


# The main script
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.disable(logging.NOTSET)
    test_trees()

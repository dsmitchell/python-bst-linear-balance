# This is a sample Python script.
import logging
import unittest
import useful_tools
from bst_tests import TestBst, perform_balance, profile_bst_balance
from hashtable_tests import TestHashTable, profile_hashtable
from sorting_tests import TestSorting
from sorting import bubble_sort, merge_sort

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.edaplayground.com/x/T_Qj


def test_hashtable():
    hashtable = TestHashTable.setup_hashtable(46, 0.7)  # this will result in 1 re-balance
    print(f'hashtable count before: {len(hashtable)}')
    keys = list()
    values = list()
    for pair in hashtable:
        keys.append(pair[0])
        values.append(pair[1])
    if not TestHashTable.confirm_hashtable(hashtable, keys, values):
        print("Hashtable not working!")
    print(f'hashtable count after: {len(hashtable)}')
    profile_hashtable()


def test_sorting():
    elements = TestSorting.setup_list(15)
    elements2 = elements.copy()
    print(f'unsorted list = {elements}')
    bubble_sort(elements)
    print(f'  bubble sort = {elements}')
    if not TestSorting.confirm_sort(elements):
        print("Bubble Sort Unsuccessful!")

    merge_sort(elements2)
    print(f'   merge sort = {elements2}')
    if not TestSorting.confirm_sort(elements2):
        print("Merge Sort Unsuccessful!")

    print("profiling sort algorithms...")
    results = TestSorting.profile_sorting()
    print(f' - bubble sort performance: {results[0]}')
    print(f' - merge sort performance: {results[1]}')


def test_trees():
    bst = TestBst.setup_bst(6)
    perform_balance(bst)
    perform_balance(bst)
    profile_bst_balance()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    target = 16
    paths_to_target = useful_tools.paths_to_target
    paths = paths_to_target(target, {2, 4, 6, 10})
    print(f'paths({paths_to_target.call_count} => {len(paths)}) = {paths}')
    for path in paths:
        current = 0
        description = f'{current}'
        for hop in path:
            current += hop
            description += f' + {hop} => {current}'
        if current == target:
            print(f'Path success: {description}')
        else:
            raise ValueError(f'Path didn\'t reach destination: {description}')

    steps = 10
    paths_to_steps = useful_tools.paths_to_steps
    paths = useful_tools.paths_to_steps(steps, {1, 3, 6})
    print(f'paths({paths_to_steps.call_count} => {len(paths)}) = {paths}')
    for path in paths:
        current = 0
        description = f'{current}'
        for hop in path:
            current += hop
            description += f' + {hop} => {current}'
        if current == steps:
            print(f'Path success: {description}')
        else:
            raise ValueError(f'Path didn\'t reach destination: {description}')

    # useful_tools.find_target_pairs()
    #
    logging.disable(logging.DEBUG)
    test_hashtable()
    #
    # logging.disable(logging.NOTSET)
    # test_sorting()
    #
    logging.disable(logging.NOTSET)
    test_trees()
    #
    # unittest.main()

    # user_phrase = input("Enter a phrase: ")
    # result = useful_tools.pound_pound(user_phrase)
    # print(f'result = {result}')
    # try:
    #     user_input = useful_tools.get_user_input()
    #     keys = user_input.keys()
    #     for key in keys:
    #         print(f'{key} = {user_input[key]}')
    #     useful_tools.poem(user_input)
    # except ValueError as err:
    #     print(f'ValueError: {err}')
    # finally:
    #     print("Finally done")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

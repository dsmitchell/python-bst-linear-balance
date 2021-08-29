import logging
from enum import Enum

from call_counter import CallCounter

# Configure bst logging
logger = logging.getLogger(__name__)


class Bst:
    """
    A class representing a Binary Search Tree
    """

    def __init__(self):
        """
        Initializes a new instance of the Bst tree
        """
        self._count = 0
        self._root = None

    def __iter__(self):
        return BstNodeValueIterator(self._root)

    def __contains__(self, item):
        if self._root is None:
            return False
        node_find_info = self._root.find(item)
        return node_find_info.location != BstNodeFindLocation.NOT_FOUND

    def __len__(self):
        return self._count

    @property
    def root(self):
        return self._root

    # Manipulations

    def __delitem__(self, item):
        if self._root:
            new_root = self._root.delete_with_new_head(item, None)
            self._root = new_root[0]
            self._count += new_root[1]

    def balance(self):
        """
        Balances the tree using an O(N) algorithm
        """
        if self._root:
            node_list = [node for node in self.in_order_node_generator()]
            logger.debug(f'Node List({len(node_list)})={node_list}')
            # self.root = self.__mid_node_reapplying_children_with_slice(tuple(node_list))
            pickup_tree = self.__mid_node_reapplying_children_with_range
            self._root = pickup_tree(tuple(node_list), 0, len(node_list)-1)
            logger.debug(f'Pickup Tree calls={pickup_tree.call_count}')
            pickup_tree.reset()

    def print_tree(self):
        """
        Prints the tree to the console
        :param include_empty_leaves: Whether to print the blank leaves as ---
        """
        if self._root:
            for generated in self.reverse_order_value_depth_generator():
                prefix = ""
                for index in range(generated[1]):
                    prefix += "\t"
                print(f'{prefix}{generated[0]}')
        else:
            print("empty")

    def reverse_order_value_depth_generator(self):
        if self._root:
            for result in self.__reverse_order_value_depth_generator_helper(self._root, 0):
                yield result

    def __reverse_order_value_depth_generator_helper(self, node, depth):
        if node.right:
            for right in self.__reverse_order_value_depth_generator_helper(node.right, depth + 1):
                yield right
        yield node.value, depth
        if node.left:
            for left in self.__reverse_order_value_depth_generator_helper(node.left, depth + 1):
                yield left

    def in_order_node_generator(self):
        for result in self.__in_order_node_generator_helper(self._root):
            yield result

    def __in_order_node_generator_helper(self, node):
        if node.left:
            for left in self.__in_order_node_generator_helper(node.left):
                yield left
        yield node
        if node.right:
            for right in self.__in_order_node_generator_helper(node.right):
                yield right

    def find(self, item):
        """
        Finds the node containing the value
        :param item: The item to locate
        :return: Returns a BstNodeFindInfo pointing to the item, if found
        """
        if self._root:
            return self._root.find(item)
        return BstNodeFindInfo(None, BstNodeFindLocation.NOT_FOUND)

    def insert(self, value):
        """
        Inserts the new value into the tree
        :param value: The value to insert
        :return: Returns whether the insert was successful (a unique value was inserted)
        """
        if self._root:
            inserted = self._root.insert(value)
            if inserted:
                self._count += 1
            return inserted
        else:
            self._root = BstNode(value)
            self._count = 1
            return True

    @CallCounter.count_calls
    def __mid_node_reapplying_children_with_slice(self, node_slice):
        """
        Recursively reapplies the children of the middle BstNode in the node_list and returns the updated BstNode
        :param node_slice: The list of nodes with which to reapply the left and right children
        :return: Returns the middle node of node_slice, if present, otherwise None
        """
        size = len(node_slice)
        if size == 0:
            return None
        mid_index = size // 2
        mid_node = node_slice[mid_index]
        mid_node.left = self.__mid_node_reapplying_children_with_slice(node_slice[:mid_index])
        mid_node.right = self.__mid_node_reapplying_children_with_slice(node_slice[mid_index+1:])
        return mid_node

    @CallCounter.count_calls
    def __mid_node_reapplying_children_with_range(self, node_list, start_index, end_index):
        """
        Recursively reapplies the children of a BstNode in the node_list given the range
        and returns the updated BstNode (or None)
        :param node_list: The list of nodes with which to reapply the left and right children
        :param start_index: The start of the desired range to update
        :param end_index: The end of the desired range to update
        :return: Returns the middle node of the desired range (if valid for supplied start and end indices)
        """
        if start_index > end_index:
            return None
        mid_index = (start_index + end_index) // 2
        mid_node = node_list[mid_index]
        mid_node.left = self.__mid_node_reapplying_children_with_range(node_list, start_index, mid_index-1)
        mid_node.right = self.__mid_node_reapplying_children_with_range(node_list, mid_index+1, end_index)
        return mid_node


class BstNode:
    """
    A class representing a node in a Binary Search Tree
    """

    def __init__(self, value):
        """
        Creates a new BstNode with no children
        :param value: The value of the Node
        """
        self._value = value
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.value == other.value

    # Override the custom print representation of the BstNode
    def __repr__(self):
        return f'BstNode({self._value})'

    @property
    def value(self):
        return self._value

    def insert(self, value):
        """
        Inserts the provided value into the Bst as a BstNode
        :param value: The value of the new BstNode
        :return: Whether the insert resulted in a new BstNode being created. False if the value already exists
        """
        if self.value == value:
            return False
        elif value < self.value:
            if self.left:
                return self.left.insert(value)
            else:
                self.left = BstNode(value)
                return True
        else:
            if self.right:
                return self.right.insert(value)
            else:
                self.right = BstNode(value)
                return True

    def delete_with_new_head(self, value, parent):
        count_change = 0
        if self.value > value and self.left:
            self.left, count_change = self.left.delete_with_new_head(value, self)
        elif self.value < value and self.right:
            self.right, count_change = self.right.delete_with_new_head(value, self)
        elif self.value == value:  # self will be deleted. Adjust and return the new head of tree
            result = None
            if parent and self == parent.left:
                if self.right:
                    self.right.min_node().left = self.left
                    result = self.right
                elif self.left:
                    result = self.left
            elif parent and self == parent.right:
                if self.left:
                    self.left.max_node().right = self.right
                    result = self.left
                elif self.right:
                    result = self.right
            elif parent is None:
                if self.right:
                    self.right.min_node().left = self.left
                    result = self.right
                elif self.left:
                    self.left.max_node().right = self.right
                    result = self.left
            del self
            return result, -1
        # Any case that hits here should return self (it is the new head)
        return self, count_change

    def find(self, value):
        """
        Finds the node containing the value
        :param value: The value to search
        :return: Returns a BstNode along with a BstNodeFindInfo to locate the node containing the value, otherwise None
        """
        if self.value == value:
            return BstNodeFindInfo(self, BstNodeFindLocation.FOUND_SELF)
        elif value < self.value and self.left:
            left_find = self.left.find(value)
            if left_find.location == BstNodeFindLocation.FOUND_SELF:
                return BstNodeFindInfo(self, BstNodeFindLocation.FOUND_ON_LEFT)
            elif left_find.location != BstNodeFindLocation.NOT_FOUND:
                return left_find
        elif value > self.value and self.right:
            right_find = self.right.find(value)
            if right_find.location == BstNodeFindLocation.FOUND_SELF:
                return BstNodeFindInfo(self, BstNodeFindLocation.FOUND_ON_RIGHT)
            elif right_find.location != BstNodeFindLocation.NOT_FOUND:
                return right_find
        return BstNodeFindInfo(None, BstNodeFindLocation.NOT_FOUND)

    def max_node(self):
        if self.right:
            return self.right.max_node()
        return self

    def min_node(self):
        if self.left:
            return self.left.min_node()
        return self


class BstNodeFindInfo:

    def __init__(self, node, location):
        self._node = node
        self._location = location

    @property
    def node(self):
        return self._node

    @property
    def location(self):
        return self._location


class BstNodeFindLocation(Enum):
    FOUND_ON_LEFT = 1  # Return value is parent, desired node is on left
    FOUND_ON_RIGHT = 2  # Return value is parent, desired node is on right
    FOUND_SELF = 3  # Return value is self, which is the desired node
    NOT_FOUND = 4  # Desired value not found


class BstNodeIterator:

    def __init__(self, node):
        self.node = node
        self.traversing_right = False
        self.iterator = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.node is None:
            raise StopIteration  # This should not happen unless the root node of Bst is None
        if not self.traversing_right:
            try:
                if self.iterator is None:
                    # Prevent another allocation if we know that the left node is None
                    if self.node.left is None:
                        self.traversing_right = True
                        return self.node
                    self.iterator = BstNodeIterator(self.node.left)
                return self.iterator.__next__()
            except StopIteration:
                self.iterator = None
                self.traversing_right = True
                return self.node
        if self.traversing_right:
            if self.iterator is None:
                # Prevent another allocation if we know that the right node is None
                if self.node.right is None:
                    raise StopIteration
                self.iterator = BstNodeIterator(self.node.right)
            return self.iterator.__next__()


class BstNodeValueIterator(BstNodeIterator):

    def __next__(self):
        result = super().__next__()
        return result.value

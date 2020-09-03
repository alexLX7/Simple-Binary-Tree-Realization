import sys
from time import sleep
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import random
import json
import string


class FileHandler():
    def __init__(self):
        super().__init__()

    def print_data(self, data: dict):
        for k, v in data.items():
            print('{}: {}'.format(k, v))

    def write_list_to_file(self, path: str, tree_as_list: list):
        try:
            with open(path, 'w', encoding="utf-8") as f:
                for item in tree_as_list:
                    f.write("{}\n".format(item))
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None

    def write_json_file(self, path: str, data: dict, indent=4):
        try:
            with open(path, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=indent)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None

    def write_json_file_wo_indent(self, path: str, data: dict):
        try:
            with open(path, 'w', encoding="utf-8") as f:
                json.dump(data, f)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None

    def read_json_file(self, path: str):
        try:
            with open(path) as f:
                data = json.load(f)
            return data
        except:
            print("Error: cannot read the data from the file with this path:")
            print("Path: " + str(path))
        return None


class AVL:
    """Base Class representing a Binary Search Tree Structure"""

    class AVLNode:
        """Private class for storing linked nodes with values and references to their siblings"""

        def __init__(self, value):
            """Node Constructor with 3 attributes"""
            self._value = value     # value being added
            # left sibling node (if val less than parent)
            self._left = None
            # right sibling node (if val greater than parent)
            self._right = None
            self._height = 0

    def __init__(self):
        """Binary Tree Constructor (creates an empty binary tree)"""
        self._root = None     # Binary tree root

    def get_root(self):
        return self._root

    def insert_element(self, value):
        """Method to insert an element into the BST"""
        self._root = self._insert_element(
            value, self._root)  # insert an element, calls recursive function

    def _insert_element(self, value, node):
        """Private method to Insert elements recursively"""
        # if node._value == value:  # if we come across a value already in the list
        #    raise ValueError
        if node is None:
            return AVL.AVLNode(value)
        if value:
            if value < node._value:
                node._left = self._insert_element(value, node._left)
            elif value > node._value:  # if a right node child node exists
                node._right = self._insert_element(value, node._right)
        return self.balance(node)

    def get_height_by_value(self, value):
        """Returns Height if value is in tree"""
        current_node = self._root
        while current_node is not None:
            if value == current_node._value:
                return self.height(current_node)  # found
            elif value < current_node._value:
                current_node = current_node._left
            else:
                current_node = current_node._right
        return None

    def find(self, value):
        """Return True if value is in tree"""
        current_node = self._root
        if type(value) == type(self._root):
            while current_node is not None:
                if value == current_node._value:
                    return True  # found
                elif value < current_node._value:
                    current_node = current_node._left
                else:
                    current_node = current_node._right
        return None

    def find_parent(self, value):
        """Non-recursive parent finder, uses a while loop"""
        current_node = self._root
        while current_node._value is not None:
            if current_node._left._value == value or current_node._right._value == value:
                break
            elif value < current_node._value:
                current_node = current_node._left
            else:
                current_node = current_node._right
        return current_node  # test with ._value

    def parent_finder(self, value):
        """Method to find parent, calls recursive method: _parent_finder"""
        if self._root is not None:
            return self._parent_finder(value, self._root)
        else:
            raise ValueError('The Binary Tree is Empty')

    def _parent_finder(self, value, node):
        """Private Recursive Method find calls"""
        if node._left._value == value or node._right._value == value:
            return node  # test with ._value
        elif value < node._value and node._left is not None:
            return self._parent_finder(value, node._left)
        else:
            return self._parent_finder(value, node._right)

    def remove_element(self, value):
        """Method to remove elements from Binary Tree, calls recursive method: _remove_element"""
        self._root = self._remove_element(value, self._root)

    def _remove_element(self, value, node):
        """Private, recursive method that removes a specified value from the binary tree.
        This method calls get_min and _remove_min when the node to be removed has two children"""
        if node is None:
            return node
        if value < node._value:
            node._left = self._remove_element(value, node._left)
        elif value > node._value:
            node._right = self._remove_element(value, node._right)
        elif node._left is not None and node._right is not None:  # 2 kids
            temp = self.get_min(node._right)
            node._value = temp._value
            node._right = self._remove_element(temp._value, node._right)
        elif node._left is None:  # One right child
            node = node._right
        else:                     # One left child
            node = node._left
        return self.balance(node)

    def balance(self, node):
        allowed_balance = 1
        if node is None:
            return node
        if self.height(node._left) - self.height(node._right) > allowed_balance:
            if self.height(node._left._left) >= self.height(node._left._right):
                node = self._rotate_with_left_child(node)
            else:
                node = self._double_with_left_child(node)
        else:
            if self.height(node._right) - self.height(node._left) > allowed_balance:
                if self.height(node._right._right) >= self.height(node._right._left):
                    node = self._rotate_with_right_child(node)
                else:
                    node = self._double_with_right_child(node)
        node._height = self.height(node)
        return node

    def _rotate_with_left_child(self, k2):
        k1 = k2._left
        k2._left = k1._right
        k1._right = k2
        k2._height = self.height(k2)
        k1._height = self.height(k1)
        return k1

    def _rotate_with_right_child(self, k1):
        k2 = k1._right
        k1._right = k2._left
        k2._left = k1
        k1._height = self.height(k1)
        k2._height = self.height(k2)
        return k2

    def _double_with_left_child(self, k3):
        k3._left = self._rotate_with_right_child(k3._left)
        return self._rotate_with_left_child(k3)

    def _double_with_right_child(self, k1):
        k1._right = self._rotate_with_left_child(k1._right)
        return self._rotate_with_right_child(k1)

    def get_min(self, node):
        while node._left is not None:
            node = node._left
        return node

    def in_order(self):
        """Returns Binary Search Tree as a String in in-order, call recursive _in_order method"""
        if self._root is None:
            return '[ ]'
        else:
            return "[ " + self._in_order(self._root)[:-2] + " ]"

    def _in_order(self, node):
        return_string = ""
        if node is not None:
            return_string = self._in_order(node._left)
            return_string = return_string + str(node._value) + ", "
            return_string = return_string + self._in_order(node._right)
        return return_string

    def pre_order_to_list(self, _list: list):
        """Returns Binary Search Tree as a String in pre-order, call recursive _pre_order method"""
        if self._root is None:
            return []
        else:
            return self._pre_order_to_list(self._root, _list)

    def _pre_order_to_list(self, node, _list: list):
        if node is not None:
            _list.append(node._value)
            self._pre_order_to_list(node._left, _list)
            self._pre_order_to_list(node._right, _list)
        return _list

    def pre_order(self):
        """Returns Binary Search Tree as a String in pre-order, call recursive _pre_order method"""
        if self._root is None:
            return '[ ]'
        else:
            return "[ " + self._pre_order(self._root)[:-2] + " ]"

    def _pre_order(self, node):
        return_string = ""
        if node is not None:
            return_string = str(node._value) + ", "
            return_string = return_string + self._pre_order(node._left)
            return_string = return_string + self._pre_order(node._right)
        return return_string

    def post_order(self):
        """Returns Binary Search Tree as a String in post-order, call recursive _post_order method"""
        if self._root is None:
            return '[ ]'
        else:
            return "[ " + self._post_order(self._root)[:-2] + " ]"

    def _post_order(self, node):
        return_string = ""
        if node is not None:
            return_string = self._post_order(node._left)
            return_string = return_string + self._post_order(node._right)
            return_string = return_string + str(node._value) + ", "
        return return_string

    def height(self, node):
        if node is None:
            return 0
        else:
            left_depth = self.height(node._left)
            right_depth = self.height(node._right)
            if left_depth > right_depth:
                return left_depth + 1
            else:
                return right_depth + 1

    def get_height(self):
        return self._get_height(self._root)

    def _get_height(self, node):
        if node is None:
            return 0
        else:
            left_depth = self._get_height(node._left)
            right_depth = self._get_height(node._right)
            if left_depth > right_depth:
                return left_depth + 1
            else:
                return right_depth + 1

    def __str__(self):
        return self.in_order()

    def get_list_of_needed_values(self, N):  # N means a sum of digits of node
        _list = self.pre_order_to_list([])
        _list_of_needed_values = []
        d = {}
        try:
            for _, v in enumerate(_list):
                _sum = 0
                _sum = sum(int(ch) for ch in str(v) if ch.isdigit())
                if _sum > N:
                    d[v] = self.get_height_by_value(v)
        except:
            print("Error: There are not only digits in the Tree but also non-digit chars")
        return d

    def get_average_height(self):  # N means a sum of digits of node
        _list = self.pre_order_to_list([])
        _list_of_heights = []
        value_to_return = 0
        try:
            for _, v in enumerate(_list):
                _list_of_heights.append(self.get_height_by_value(v))
            value_to_return = sum(_list_of_heights) / len(_list_of_heights)
        except:
            pass
        return value_to_return

    def print_dict(self, d: dict):
        if d:
            for k, v in d.items():
                print(k, v)
        else:
            print('Empty dictionary of values with height')


class Node:
    def __init__(self, x):
        super().__init__()
        self.v = x
        self.l = None
        self.r = None

    def __repr__(self):
        return "Node: {v}, {l}, {r}".format(v=self.v, l=self.l, r=self.r)


class Tree:
    def __init__(self, _type: type):
        super().__init__()
        self.root = None
        self._type = _type

    def get_root(self):
        return self.root

    def _check_type_of_element(self, val):
        if self._type == int:
            return self._try_to_cast_int(val)
        if self._type == float:
            return self._try_to_cast_float(val)
        if self._type == str:
            return self._try_to_cast_str(val)

    def _try_to_cast_int(self, val):
        try:
            return int(val)
        except:
            return None

    def _try_to_cast_float(self, val):
        try:
            return float(val)
        except:
            return None

    def _try_to_cast_str(self, val):
        try:
            return str(val)
        except:
            return None

    def add(self, val):
        value = self._check_type_of_element(val)
        if value:
            if(self.root == None):
                self.root = Node(value)
            else:
                self._add(value, self.root)

    def _add(self, val, node):
        if(val < node.v):
            if(node.l != None):
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if(node.r != None):
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if(self.root != None):
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if(val == node.v):
            return node
        elif(val < node.v and node.l != None):
            self._find(val, node.l)
        elif(val > node.v and node.r != None):
            self._find(val, node.r)

    def delete_tree(self):
        self.root = None

    def print_tree(self):
        if(self.root != None):
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node != None:
            self._print_tree(node.l)
            print(str(node.v), end='-')
            self._print_tree(node.r)

    def print_tree_level(self):
        tree_list = self.get_tree_as_list()
        current = 0
        for i in range(self.get_len()):
            for j in range(current, current + 2**i):
                val = '_' if tree_list[j] == None else tree_list[j]
                print(val, end=' ')
            current += 2**i
            print()

    def pretty_print_tree(self):
        self._pretty_print_tree(self.root)

    def _pretty_print_tree(self, node, prefix="", isLeft=True):
        if not node:
            print("Empty Tree")
            return
        if node.r:
            self._pretty_print_tree(
                node.r, prefix + ("│   " if isLeft else "    "), False)
        print(prefix + ("└── " if isLeft else "┌── ") + str(node.v))
        if node.l:
            self._pretty_print_tree(
                node.l, prefix + ("    " if isLeft else "│   "), True)

    def _pretty_print_tree_to_the_list(self, list_to_print, node, prefix="", isLeft=True):
        if not node:
            list_to_print.append("Empty Tree")
            return
        if node.r:
            self._pretty_print_tree_to_the_list(
                list_to_print, node.r, prefix + ("│   " if isLeft else "    "), False)
        list_to_print.append(
            prefix + ("└── " if isLeft else "┌── ") + str(node.v))
        if node.l:
            self._pretty_print_tree_to_the_list(
                list_to_print, node.l, prefix + ("    " if isLeft else "│   "), True)

    def pretty_print_tree_to_the_list(self):
        list_to_print = []
        self._pretty_print_tree_to_the_list(list_to_print, self.root)
        return list_to_print

    def _pretty_print_tree_to_the_list_double_spaces(self, list_to_print, node, prefix="", isLeft=True):
        if not node:
            list_to_print.append("Empty Tree")
            return
        if node.r:
            self._pretty_print_tree_to_the_list_double_spaces(
                list_to_print, node.r, prefix + ("│      " if isLeft else "         "), False)
        list_to_print.append(
            prefix + ("└──  " if isLeft else "┌──  ") + str(node.v))
        if node.l:
            self._pretty_print_tree_to_the_list_double_spaces(
                list_to_print, node.l, prefix + ("         " if isLeft else "│      "), True)

    def pretty_print_tree_to_the_list_double_spaces(self):
        list_to_print = []
        self._pretty_print_tree_to_the_list_double_spaces(
            list_to_print, self.root)
        return list_to_print

    def get_tree_as_list(self):
        size = 0
        for i in range(self.get_len()):
            size += 2**i
        # print(str(size))
        # the maximum size of a python list on a 32 bit system is 536,870,912 elements
        res = [None] * size
        return self._get_tree_as_list(self.root, 0, res)

    def _get_tree_as_list(self, node, i, res):
        if node == None:
            return res
        else:
            res[i] = node.v
            self._get_tree_as_list(node.l, 2*i+1, res)
            self._get_tree_as_list(node.r, 2*i+2, res)
            return res

    def get_len(self):
        return self._get_len(self.root, 0)

    def _get_len(self, node, length):
        if node == None:
            return length
        else:
            length += 1
            return max(self._get_len(node.l, length), self._get_len(node.r, length))

    def make_from_list(self, t_list):
        assert len(t_list) > 0
        size = 0
        i = 0
        while size < len(t_list):
            size += 2**i
            i += 1
        t_list += [None] * (size - len(t_list))

        self.root = Node(t_list[0])
        self._make_from_list(self.root, t_list, 0)

        return

    def _make_from_list(self, node, t_list, i):
        node.val = t_list[i]
        if (2*i + 1) < len(t_list):
            if t_list[2*i + 1] != None:
                node.l = Node(t_list[2*i + 1])
                self._make_from_list(node.l, t_list, 2*i + 1)
            if t_list[2*i + 2] != None:
                node.r = Node(t_list[2*i + 2])
                self._make_from_list(node.r, t_list, 2*i + 2)
        return

    def insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.v:
            node.l = self.insert(node.l, key)
        else:
            node.r = self.insert(node.r, key)
        return node

    def min_value_node(self, node):
        current = node
        while(current.l):
            current = current.l
        return current

    def delete_node(self, root, val):
        if not root:
            return root
        key = self._check_type_of_element(val)
        if key:
            if key < root.v:
                root.l = self.delete_node(root.l, key)
            elif(key > root.v):
                root.r = self.delete_node(root.r, key)
            else:
                if not root.l:
                    temp = root.r
                    root = None
                    return temp
                elif not root.r:
                    temp = root.l
                    root = None
                    return temp
                temp = self.min_value_node(root.r)
                root.v = temp.v
                root.r = self.delete_node(root.r, temp.v)
        return root

    def search(self, value_to_seach):
        found = self.find(value_to_seach)
        if found:
            print("Found: " + str(value_to_seach))
            print(str(found))
            return found
        else:
            print("Haven't found.")
            return None

    def get_list_of_nodes_by_iteration_over_tree(self):
        tree_as_list = []
        self._iterate_over_all_nodes(self.root, tree_as_list)
        # print(tree_as_list)
        return tree_as_list

    def _iterate_over_all_nodes(self, node: Node, l: list):
        if not node:
            return
        if not node.l and not node.r:
            return
        if node.l:
            l.append(node.l)
            self._iterate_over_all_nodes(node.l, l)
        if node.r:
            l.append(node.r)
            self._iterate_over_all_nodes(node.r, l)

    def print_leaves_without_nodes(self, node: Node):
        if not node:
            return
        if not node.l and not node.r:
            print(node.v)
            return
        if node.l:
            self.print_leaves_without_nodes(node.l)
        if node.r:
            self.print_leaves_without_nodes(node.r)

    def _process_frequency(self):
        d = {}
        tree_as_list = self.get_tree_as_list()
        count, itm = 0, ''
        for item in reversed(tree_as_list):
            if item:
                d[item] = d.get(item, 0) + 1
                if d[item] >= count:
                    count, itm = d[item], item
        return d

    def print_the_most_frequent_element(self):
        list_of_frequency = list(reversed(self._get_list_of_frequency()))

        counter = 0
        if list_of_frequency:
            for i, v in enumerate(list_of_frequency):
                print('Value: ' + str(v[0]) + ', frequency: ' + str(v[1]))
                if v[1] > counter:
                    counter = v[1]

        raw_list_of_most_common_elements = []
        for i, v in enumerate(list_of_frequency):
            if v[1] == counter:
                raw_list_of_most_common_elements.append(v[1])

        list_of_counters = []
        for value in raw_list_of_most_common_elements:
            if value not in list_of_counters:
                list_of_counters.append(value)

        list_of_most_common_elements = []
        for i, v in enumerate(list_of_frequency):
            for _, _v in enumerate(list_of_counters):
                if v[1] == _v:
                    list_of_most_common_elements.append([v[0], v[1]])
        return list_of_most_common_elements

    def _get_list_of_frequency(self):
        dict_frequency = self._process_frequency()
        raw_list_of_frequency = []
        for key, value in sorted(dict_frequency.items(), key=lambda item: item[1]):
            raw_list_of_frequency.append([key, value])

        list_of_frequency = []
        for v in raw_list_of_frequency:
            list_of_frequency.append([v[0], v[1]])

        return list_of_frequency

    def get_list_of_frequency(self):
        return list(reversed(self._get_list_of_frequency()))

    def print_a_few_most_frequent_elements(self):
        number_of_elements = 5
        list_of_frequency = list(reversed(self._get_list_of_frequency()))
        if list_of_frequency:
            for i, v in enumerate(list_of_frequency):
                if i < number_of_elements:
                    try:
                        print('Value: ' + str(v[0]) +
                              ', frequency: ' + str(v[1]))
                    except:
                        pass

    def print_most_frequent_element(self):
        list_of_frequency = self._get_list_of_frequency()
        if list_of_frequency:
            print('Value: ' + str(list_of_frequency[-1][0]))
            print('Frequency: ' + str(list_of_frequency[-1][1]))
        else:
            print('Tree is empty.')

    def print_list_of_frequency(self):
        list_of_frequency = self._get_list_of_frequency()
        if list_of_frequency:
            for v in reversed(list_of_frequency):
                print('Value: ' + str(v[0]) + ', frequency: ' + str(v[1]))
        else:
            print('Tree is empty.')


class TreeManager:
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()

        # for json format, saves tree as list with name 'tree_as_list'
        self._tree_name = 'tree_as_list'
        self._tree_type = 'tree_type'
        self._known_types = {"<class 'int'>": int,
                             "<class 'float'>": float, "<class 'str'>": str}
        self._from = -99  # default int/float value of elements for random creation
        self._to = 99  # default int/float value of elements for random creation
        self._min_number_of_elements = 0
        self._max_number_of_elements = 1024  # it is not actual max number

    def _generate_list_of_int_with_repetitions(self, number_of_elements: int):
        _list = [random.randint(self._from, self._to)
                 for i in range(number_of_elements)]
        return _list

    def _generate_list_of_floats_wo_repetitions(self, number_of_elements: int):
        _list = []
        seen = set()
        for i in range(number_of_elements):
            x = random.uniform(self._from, self._to)
            while x in seen:
                x = random.uniform(self._from, self._to)
            seen.add(x)
            _list.append(x)
        return _list

    def _generate_list_of_strings(self, number_of_elements: int):
        _list = []
        for x in range(number_of_elements):
            _list.append(self._generate_single_string())
        return _list

    def _generate_single_string(self, size=8):
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(size))

    def _validate_number_of_elements(self, number_of_elements: int):
        if self._min_number_of_elements <= number_of_elements < self._max_number_of_elements:
            return number_of_elements
        return 0

    def _validate_raw_data(self, raw_data: dict):
        try:
            d = {self._tree_type: raw_data[self._tree_type],
                 self._tree_name: raw_data[self._tree_name]}
            return d
        except:
            print('Error: Input is not correct.')
        return None

    def _create_tree_out_of_the_list_with_validation(self, d: dict, input_key: str, input_type: str):
        _list = d[input_key]
        _type = d[input_type]
        _var_type = self._known_types[_type]
        _tree = Tree(_var_type)
        if _list:
            for _, v in enumerate(_list):
                if isinstance(v, _var_type):
                    _tree.add(v)
        return _tree

    def _create_tree_out_of_the_list_wo_validation(self, _list: list, _type: str):
        _var_type = self._known_types[_type]
        _tree = Tree(_var_type)
        if _list:
            for _, v in enumerate(_list):
                _tree.add(v)
        return _tree

    def create_new_random_tree(self, input_type: str, number_of_elements: int):
        try:
            _number_of_elements = self._validate_number_of_elements(
                number_of_elements)
            if input_type == "<class 'int'>":
                _list = self._generate_list_of_int_with_repetitions(
                    _number_of_elements)
            if input_type == "<class 'str'>":
                _list = self._generate_list_of_strings(_number_of_elements)
            if input_type == "<class 'float'>":
                _list = self._generate_list_of_floats_wo_repetitions(
                    _number_of_elements)
            return self._create_tree_out_of_the_list_wo_validation(_list, input_type)
        except:
            print('Error: Could not generate the list.')
        return None

    def _process_the_tree(self, tree: Tree):
        # data_to_dump = {self._tree_name: tuple(tree.get_tree_as_list())} # with null
        data_to_dump = {
            self._tree_type: str(tree._type),
            self._tree_name: tuple([i for i in tree.get_tree_as_list() if i])
        }
        return data_to_dump

    def write_tree_to_json_file_as_list(self, tree: Tree, path: str):
        try:
            data_to_dump = self._process_the_tree(tree)
            self.file_handler.write_json_file(path, data_to_dump)
            return
        except:
            print('Error: Cannot write the data to the file.')
        return None

    def write_tree_to_json_file_as_list_wo_indent(self, tree: Tree, path: str):
        try:
            data_to_dump = self._process_the_tree(tree)
            self.file_handler.write_json_file_wo_indent(path, data_to_dump)
            return
        except:
            print('Error: Cannot write the data to the file.')
        return None

    def write_tree_to_file_as_tree(self, tree: Tree, path: str):
        try:
            tree_as_list = tree.pretty_print_tree_to_the_list()
            self.file_handler.write_list_to_file(path, tree_as_list)
            return
        except:
            print('Error: Cannot write the data to the file.')
        return None

    def read_tree_from_json_file(self, path: str):
        try:
            data = self.file_handler.read_json_file(path)
            return self._create_tree_out_of_the_list_with_validation(
                self._validate_raw_data(data), self._tree_name, self._tree_type)
        except:
            print('Error: Cannot read the data from the file.')
        return None


class GlobalVariables:
    def __init__(self):
        self._dict_eng = dict(  # usage: self._global_variables.default_dict.get('
            yes='Yes',
            no='No',
            instance='Instance ',
            file='File',
            open='Open...',
            close_project='Close Project',
            export_instance_as_png='Export instance as PNG',
            instructions='Instructions',
            show_instructions='Show instructions',
            about='About',
            show_about='Show about',
            save_file='Save File',
            open_project='Open Project',
            options='Options',
            additional_options_of_the_instance='Additional options',
            update_the_output='Update the output',
            clear_the_output='Clear the output',
            create_int_tree='Create tree (int)',
            create_float_tree='Create tree (float)',
            create_str_tree='Create tree (str)',
            delete_element='Delete element',
            add_element='Add element',
            export_tree_as_list='Save binary tree (as *.json)',
            export_avl_tree_as_list='Save AVL tree (as *.json)',
            export_tree_as_tree='Save binary tree (as *.txt)',
            export_avl_tree_as_tree='Save AVL tree (as *.txt)',
            import_tree='Import tree from the file',
            import_avl_tree='Import AVL tree from the file',
            print_average_height_of_avl_tree='Print average height of AVL tree',
            average_height_of_avl_tree='Average height of AVL tree: ',
            tree_type='Type of tree elements: ',
            pretty_print_tree_to_text_edit='Show the tree',
            pretty_print_avl_tree_to_text_edit='Show the AVL tree',
            delete_tree='Delete the tree',
            print_most_frequent_elements='Print a few the most frequent elements',
            print_list_of_frequency='Print the list of frequency',
            print_list_of_needed_values='Print list of values, which sum of digits is more than N',
            value='Value: ',
            frequency='Frequency: ',
            height='Height: ',
            confirm_your_choice='Confirm Your choice',
            are_you_sure_you_want_to_delete='Are you sure you want to delete all instances?',
            add_a_new_instance_menu='Add a new instance menu',
            delete_all_instances='Delete all instances',
            confirm_exit='Confirm exit',
            are_you_sure_you_want_to_exit='Are you sure you want to exit?',
            about_window_title='About',
            about_window_creators_name='Pavlov Alex',
            about_window_creators_github='https://github.com/alexLX7 \n\n(https://github.com/alexLAP7 is the old link)'
        )
        self._dict_rus = dict(
            yes='Да',
            no='Нет',
            instance='Экземпляр объекта ',
            file='Файл',
            open='Открыть...',
            close_project='Закрыть проект',
            export_instance_as_png='Экспортировать как PNG',
            instructions='Инструкции',
            show_instructions='Показать инструкции',
            about='Об авторе',
            show_about='Показать информацию об авторе',
            save_file='Сохранить файл',
            open_project='Открыть проект',
            options='Настройки',
            additional_options_of_the_instance='Дополнительные настройки',
            update_the_output='Обновить отображение',
            clear_the_output='Очистить окно вывода',
            create_int_tree='Создать дерево (int)',
            create_float_tree='Создать дерево (float)',
            create_str_tree='Создать дерево (str)',
            delete_element='Удалить элемент',
            add_element='Добавить элемент',
            export_tree_as_list='Экспортировать дерево (*.json)',
            export_avl_tree_as_list='Экспортировать АВЛ дерево (*.json)',
            export_tree_as_tree='Экспортировать дерево (*.txt)',
            export_avl_tree_as_tree='Экспортировать АВЛ дерево (*.txt)',
            import_tree='Импортировать дерево из файла',
            import_avl_tree='Импортировать АВЛ дерево из файла',
            print_average_height_of_avl_tree='Отобразить среднюю высоту АВЛ дерева',
            average_height_of_avl_tree='Средняя высота АВЛ дерева: ',
            tree_type='Тип элементов дерева: ',
            pretty_print_tree_to_text_edit='Отобразить дерево',
            pretty_print_avl_tree_to_text_edit='Отобразить АВЛ дерево',
            delete_tree='Удалить дерево',
            print_most_frequent_elements='Отобразить самые часто встречающиеся элементы',
            print_list_of_frequency='Отобразить все элементы с количеством их повторений',
            print_list_of_needed_values='Отобразить элементы, сумма цифр которых больше N',
            value='Значение: ',
            frequency='Количество повторов: ',
            height='Уровень: ',
            confirm_your_choice='Подтвердите свой выбор',
            are_you_sure_you_want_to_delete='Вы уверены, что хотите удалить все объекты?',
            add_a_new_instance_menu='Добавить меню для нового экземпляра объекта',
            delete_all_instances='Удалить все экземпляры объектов',
            confirm_exit='Подтвердите выход',
            are_you_sure_you_want_to_exit='Вы уверены, что хотите выйти?',
            about_window_title='Об авторе',
            about_window_creators_name='Павлов Александр',
            about_window_creators_github='https://github.com/alexLX7 \n\n(https://github.com/alexLAP7 is the old link)'
        )
        self.default_dict = self._dict_rus
        self.default_dict = self._dict_eng


class MenuInstance:
    def __init__(self):
        self._global_variables = GlobalVariables()
        # without id you couldn't get proper instance by call from another class
        self.id_of_instance = 0
        self.name = self._global_variables.default_dict.get(
            'instance')  # name of the instance
        self.tree = Tree(int)
        self.avl_tree = Tree(int)
        self.number_of_elements = 0
        self.element_name = ''
        self.value_to_check_the_sum_of_digits_of_node = 0


class GrowingTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.heightMin = 40
        self.heightMax = 40

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)
        if len(self.document().toPlainText()) > 50:  # 50 is number of chars
            self.textCursor().deletePreviousChar()


# dynamically expandable box of gui elements
class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):

        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

    @QtCore.pyqtSlot()
    def on_pressed(self):

        sleep(0.25)  # slows down so it won't lag because of users spam
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):

        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(300)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(300)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class Connector:
    def __init__(self):
        self._global_variables = GlobalVariables()
        self.list_of_widgets = []
        self.list_of_menu_instances = []
        self.number_of_menu_instances = 0
        self.current_widget_to_export = None


class InstructionWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(InstructionWindow, self).__init__(parent)
        self._global_variables = GlobalVariables()
        self.init_layout()

    def init_layout(self):
        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        w.setLayout(layout)

        self.title = self._global_variables.default_dict.get('instructions')
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,
                         self.windowWidth, self.windowHeight)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        layout.addWidget(scroll)
        scrollContents = QtWidgets.QWidget()
        scroll.setWidget(scrollContents)
        text_layout = QtWidgets.QVBoxLayout(scrollContents)
        # font = QtGui.QFont()
        # font.setPointSize(11)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_text = QLabel()
        label_text.setText(
            self._global_variables.default_dict.get('instructions'))
        vbox.addWidget(label_text)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)
        vbox.addItem(verticalSpacer)
        text_layout.addWidget(frame)


class AboutWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self._global_variables = GlobalVariables()
        self.title = self._global_variables.default_dict.get(
            'about_window_title')
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,
                         self.windowWidth, self.windowHeight)

        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        w.setLayout(layout)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_creator_name = QLabel()
        creator_name = self._global_variables.default_dict.get(
            'about_window_creators_name')
        label_creator_name.setText(creator_name)
        vbox.addWidget(label_creator_name)

        label_creator_github = QLabel()
        creator_github = self._global_variables.default_dict.get(
            'about_window_creators_github')
        label_creator_github.setText(creator_github)
        vbox.addWidget(label_creator_github)

        vbox.setAlignment(Qt.AlignCenter)
        layout.addWidget(frame)


class Application(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._global_variables = GlobalVariables()
        self.title = 'Application'
        self.setWindowTitle(self.title)
        self.connector = None

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_edit.setFont(font)
        self.setCentralWidget(self.text_edit)

        self.instruction_window = InstructionWindow()
        self.about_window = AboutWindow()

        self.showMaximized()
        self.mainMenu = QMenuBar(self)
        self.setMenuBar(self.mainMenu)

        self.set_a_project()

        menu_file = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('file'))

        file_action_export_as_png = menu_file.addAction(
            self._global_variables.default_dict.get('export_instance_as_png'))
        file_action_export_as_png.triggered.connect(
            self.export_instance_as_png)

        file_action_close = menu_file.addAction(
            self._global_variables.default_dict.get('close_project'))
        file_action_close.triggered.connect(self.close_application)

        menu_instructions = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('instructions'))
        instructions_action_show = menu_instructions.addAction(
            self._global_variables.default_dict.get('show_instructions'))
        instructions_action_show.triggered.connect(self.show_instructions)

        menu_about = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('about'))
        about_action_show = menu_about.addAction(
            self._global_variables.default_dict.get('show_about'))
        about_action_show.triggered.connect(self.show_about)

    def export_instance_as_png(self):
        try:
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            self._global_variables.default_dict.get(
                                                                'save_file'),
                                                            '.png', "Image (*.png *.jpg *.tif)")
            if name:
                img = self.connector.current_widget_to_export.grab()
                img.save(name)
        except:
            print(
                'Oops! An Error: There is a problem with a file, which you have tried to save.')

    def show_instructions(self):
        self.instruction_window.show()

    def show_about(self):
        self.about_window.show()

    def close_a_project(self):
        try:
            self.close_application()
        except:
            pass

    def set_options_dock(self):
        self.dockWidget = QDockWidget(
            self._global_variables.default_dict.get('options'), self)
        self.connector.list_of_widgets.append(self.dockWidget)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                    QtWidgets.QDockWidget.DockWidgetMovable)
        widget = QWidget(self.dockWidget)
        qvbox_layout = QVBoxLayout(widget)
        qvbox_layout.setSpacing(1)
        qvbox_layout.setContentsMargins(2, 2, 2, 2)
        widget.setLayout(qvbox_layout)

        button = QPushButton()
        button_update_the_output = QPushButton()
        button_update_the_output.setText(
            self._global_variables.default_dict.get('clear_the_output'))
        button_update_the_output.setStyleSheet(
            'QPushButton {background-color:rgb(170, 255, 0); color: black;}')
        qvbox_layout.addWidget(button_update_the_output)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        qvbox_layout.addWidget(scroll)
        scrollContents = QtWidgets.QWidget()
        scroll.setWidget(scrollContents)

        self.QVBox_layout_of_dock_options = QtWidgets.QVBoxLayout(
            scrollContents)
        font = QtGui.QFont()
        font.setPointSize(11)

        def button_update_the_output_clicked(arg):
            self.clear_textedit()

        button_update_the_output.clicked.connect(
            button_update_the_output_clicked)

        def button_add_a_new_instance_menu_new_clicked(arg):
            self.set_option_fields()

        def button_delete_all_clicked(arg):
            msg = QMessageBox()
            msg.setWindowTitle(
                self._global_variables.default_dict.get('confirm_your_choice'))
            msg.setText(self._global_variables.default_dict.get(
                'are_you_sure_you_want_to_delete'))
            okButton = msg.addButton(self._global_variables.default_dict.get('yes'),
                                     QMessageBox.AcceptRole)
            msg.addButton(self._global_variables.default_dict.get(
                'no'), QMessageBox.RejectRole)
            msg.exec()
            if msg.clickedButton() == okButton:
                self.text_edit.clear()
                self.connector.list_of_menu_instances.clear()
                self.connector.number_of_menu_instances = 0
                self.connector.current_widget_to_export = None
                self.statusBar().showMessage("")
                self.dockWidget.close()
                self.set_options_dock()
            else:
                pass

        button_add_a_new_instance_menu = QPushButton()
        button_add_a_new_instance_menu.setText(
            self._global_variables.default_dict.get('add_a_new_instance_menu'))
        button_add_a_new_instance_menu.clicked.connect(
            button_add_a_new_instance_menu_new_clicked)
        qvbox_layout.addWidget(button_add_a_new_instance_menu)

        button_delete_all = QPushButton()
        button_delete_all.setText(
            self._global_variables.default_dict.get('delete_all_instances'))
        button_delete_all.clicked.connect(button_delete_all_clicked)
        qvbox_layout.addWidget(button_delete_all)

        self.dockWidget.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

    def set_option_fields(self):

        instance_menu = MenuInstance()
        instance_menu.id_of_instance = self.connector.number_of_menu_instances
        self.connector.number_of_menu_instances = \
            self.connector.number_of_menu_instances + 1
        self.connector.list_of_menu_instances.append(instance_menu)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)

        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)
        name = GrowingTextEdit()
        name.setText(instance_menu.name +
                     str(self.connector.number_of_menu_instances))
        self.connector.list_of_menu_instances[instance_menu.id_of_instance].name = name.toPlainText(
        )
        name.setMinimumHeight(27)
        name.setMaximumHeight(27)

        def name_changed():
            try:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].name = name.toPlainText()
            except:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].name = 'Incorrect symbols in name'

        name.textChanged.connect(name_changed)

        def update_info_label():
            info_label.setText(
                self._global_variables.default_dict.get('tree_type') + str(
                    self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree._type))

        def print_tree():
            update_info_label()
            self.text_edit.clear()
            tree_as_list = self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.pretty_print_tree_to_the_list_double_spaces()
            for i, v in enumerate(tree_as_list):
                self.text_edit.append(v)

        def update_avl_tree():
            avl = AVL()
            # _avl_tree_as_list = self.connector.list_of_menu_instances[
            #     instance_menu.id_of_instance].tree.get_tree_as_list()
            # [i for i in tree.get_tree_as_list() if i]
            _avl_tree_as_list = [i for i in self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.get_tree_as_list() if i]
            for i, v in enumerate(_avl_tree_as_list):
                avl.insert_element(v)
            pre_order = avl.pre_order_to_list([])
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].avl_tree.delete_tree(
            )
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].avl_tree._type = \
                self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree._type
            if pre_order:
                for _, v in enumerate(pre_order):
                    self.connector.list_of_menu_instances[instance_menu.id_of_instance].avl_tree.add(
                        v)

        def print_avl_tree():
            update_info_label()
            self.text_edit.clear()
            update_avl_tree()
            tree_as_list = self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].avl_tree.pretty_print_tree_to_the_list_double_spaces()
            for i, v in enumerate(tree_as_list):
                self.text_edit.append(v)

        def print_list(list_of_frequency: list, number_of_elements: int):
            self.text_edit.clear()
            if list_of_frequency:
                for i, v in enumerate(list_of_frequency):
                    if i < number_of_elements:
                        try:
                            self.text_edit.append(
                                self._global_variables.default_dict.get('value') + str(v[0]) + ', ' +
                                self._global_variables.default_dict.get('frequency') + str(v[1]))
                        except:
                            pass

        def _print_list(list_of_frequency):
            self.text_edit.clear()
            if list_of_frequency:
                for i, v in enumerate(list_of_frequency):
                    try:
                        self.text_edit.append(
                            self._global_variables.default_dict.get('value') + str(v[0]) + ', ' +
                            self._global_variables.default_dict.get('frequency') + str(v[1]))
                    except:
                        pass

        def print_dict(_dict: dict):
            self.text_edit.clear()
            for v, h in _dict.items():
                try:
                    self.text_edit.append(
                        self._global_variables.default_dict.get('value') + str(v) + ', ' +
                        self._global_variables.default_dict.get('height') + str(h))
                except:
                    pass

        button_pretty_print_tree_to_text_edit = QPushButton()
        button_pretty_print_tree_to_text_edit.setText(
            self._global_variables.default_dict.get('pretty_print_tree_to_text_edit'))

        def button_pretty_print_tree_to_text_edit_clicked(arg):
            print_tree()
        button_pretty_print_tree_to_text_edit.clicked.connect(
            button_pretty_print_tree_to_text_edit_clicked)

        button_pretty_print_avl_tree_to_text_edit = QPushButton()
        button_pretty_print_avl_tree_to_text_edit.setText(
            self._global_variables.default_dict.get('pretty_print_avl_tree_to_text_edit'))

        def button_pretty_print_avl_tree_to_text_edit_clicked(arg):
            if self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].avl_tree.pretty_print_tree_to_the_list_double_spaces():
                print_avl_tree()
        button_pretty_print_avl_tree_to_text_edit.clicked.connect(
            button_pretty_print_avl_tree_to_text_edit_clicked)

        def set_number_of_elements():
            spinBox.setMaximum(400)
            if spinBox.value() <= spinBox.value():
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].number_of_elements = int(
                        str(spinBox.value()))

        spinBox = QSpinBox()
        spinBox.valueChanged.connect(set_number_of_elements)
        vbox.addWidget(spinBox)

        button_create_int_tree = QPushButton()
        button_create_int_tree.setText(
            self._global_variables.default_dict.get('create_int_tree'))

        def button_create_int_tree_clicked(arg):
            tree_manager = TreeManager()
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree =\
                tree_manager.create_new_random_tree("<class 'int'>", self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].number_of_elements)
            update_avl_tree()
            print_tree()
        button_create_int_tree.clicked.connect(button_create_int_tree_clicked)
        vbox.addWidget(button_create_int_tree)

        button_create_float_tree = QPushButton()
        button_create_float_tree.setText(
            self._global_variables.default_dict.get('create_float_tree'))

        def button_create_float_tree_clicked(arg):
            tree_manager = TreeManager()
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree =\
                tree_manager.create_new_random_tree("<class 'float'>", self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].number_of_elements)
            update_avl_tree()
            print_tree()
        button_create_float_tree.clicked.connect(
            button_create_float_tree_clicked)
        vbox.addWidget(button_create_float_tree)

        button_create_str_tree = QPushButton()
        button_create_str_tree.setText(
            self._global_variables.default_dict.get('create_str_tree'))

        def button_create_str_tree_clicked(arg):
            tree_manager = TreeManager()
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree =\
                tree_manager.create_new_random_tree("<class 'str'>", self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].number_of_elements)
            update_avl_tree()
            print_tree()
        button_create_str_tree.clicked.connect(button_create_str_tree_clicked)
        vbox.addWidget(button_create_str_tree)

        empty_label_0 = QLabel('')
        vbox.addWidget(empty_label_0)

        element_name = GrowingTextEdit()
        element_name.setText('')
        element_name.setMinimumHeight(27)
        element_name.setMaximumHeight(27)

        def element_name_changed():
            try:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].element_name = element_name.toPlainText()
            except:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].element_name = 'Incorrect symbols in element_name'

        element_name.textChanged.connect(element_name_changed)
        vbox.addWidget(element_name)

        button_add_element = QPushButton()
        button_add_element.setText(
            self._global_variables.default_dict.get('add_element'))

        def button_add_element_clicked(arg):
            tree_manager = TreeManager()
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree.add(
                self.connector.list_of_menu_instances[instance_menu.id_of_instance].element_name)
            element_name.setText('')
            update_avl_tree()
            print_tree()
        button_add_element.clicked.connect(button_add_element_clicked)
        vbox.addWidget(button_add_element)

        button_delete_element = QPushButton()
        button_delete_element.setText(
            self._global_variables.default_dict.get('delete_element'))

        def button_delete_element_clicked(arg):
            tree_manager = TreeManager()
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree.delete_node(
                self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree.root,
                self.connector.list_of_menu_instances[instance_menu.id_of_instance].element_name)
            element_name.setText('')
            update_avl_tree()
            print_tree()
        button_delete_element.clicked.connect(button_delete_element_clicked)
        vbox.addWidget(button_delete_element)

        empty_label_1 = QLabel('')
        vbox.addWidget(empty_label_1)

        button_import_tree = QPushButton()
        button_import_tree.setText(
            self._global_variables.default_dict.get('import_tree'))

        def button_import_tree_clicked(arg):
            try:
                filename, _ = QFileDialog.getOpenFileName(self,
                                                          self._global_variables.default_dict.get(
                                                              'open_project'), '',
                                                          "Json Files (*.json)",
                                                          options=QFileDialog.DontUseNativeDialog)
                if (filename):
                    tree_manager = TreeManager()
                    self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree = \
                        tree_manager.read_tree_from_json_file(filename)
            except:
                print('Oops! An Error: There is a problem with a file, which you have tried to open.\n'
                      ' Make sure, it has the right extension')
            print_tree()
        button_import_tree.clicked.connect(button_import_tree_clicked)
        vbox.addWidget(button_import_tree)

        # button_import_avl_tree = QPushButton()
        # button_import_avl_tree.setText(
        #     self._global_variables.default_dict.get('import_avl_tree'))
        # def button_import_avl_tree_clicked(arg):
        #     try:
        #         filename, _ = QFileDialog.getOpenFileName(self,
        #                                                    self._global_variables.default_dict.get(
        #                                                        'open_project'),'',
        #                                                     "Json Files (*.json)",
        #                                                   options=QFileDialog.DontUseNativeDialog)
        #         if (filename):
        #             tree_manager = TreeManager()
        #             self.connector.list_of_menu_instances[instance_menu.id_of_instance].avl_tree = \
        #                 tree_manager.read_tree_from_json_file(filename)
        #     except:
        #         print('Oops! An Error: There is a problem with a file, which you have tried to open.\n'
        #             ' Make sure, it has the right extension')
        #     print_avl_tree()
        # button_import_avl_tree.clicked.connect(button_import_avl_tree_clicked)
        # vbox.addWidget(button_import_avl_tree)

        button_export_tree_as_tree = QPushButton()
        button_export_tree_as_tree.setText(
            self._global_variables.default_dict.get('export_tree_as_tree'))

        def button_export_tree_as_tree_clicked(arg):
            try:
                name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                self._global_variables.default_dict.get(
                                                                    'save_file'),
                                                                '.txt', 'Txt Files (*.txt)')
                if name:
                    tree_manager = TreeManager()
                    tree_manager.write_tree_to_file_as_tree(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].tree, name)
                    print_tree()
            except:
                print(
                    'Oops! An Error: There is a problem with a file, which you have tried to save.')

        button_export_tree_as_tree.clicked.connect(
            button_export_tree_as_tree_clicked)
        vbox.addWidget(button_export_tree_as_tree)

        button_export_avl_tree_as_tree = QPushButton()
        button_export_avl_tree_as_tree.setText(
            self._global_variables.default_dict.get('export_avl_tree_as_tree'))

        def button_export_avl_tree_as_tree_clicked(arg):
            try:
                name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                self._global_variables.default_dict.get(
                                                                    'save_file'),
                                                                '.txt', 'Txt Files (*.txt)')
                if name:
                    tree_manager = TreeManager()
                    tree_manager.write_tree_to_file_as_tree(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].avl_tree, name)
                    print_avl_tree()
            except:
                print(
                    'Oops! An Error: There is a problem with a file, which you have tried to save.')

        button_export_avl_tree_as_tree.clicked.connect(
            button_export_avl_tree_as_tree_clicked)
        vbox.addWidget(button_export_avl_tree_as_tree)

        button_export_tree_as_list = QPushButton()
        button_export_tree_as_list.setText(
            self._global_variables.default_dict.get('export_tree_as_list'))

        def button_export_tree_as_list_clicked(arg):
            try:
                name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                self._global_variables.default_dict.get(
                                                                    'save_file'),
                                                                '.json', 'Json Files (*.json)')
                if name:
                    tree_manager = TreeManager()
                    tree_manager.write_tree_to_json_file_as_list(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].tree, name)
                    print_tree()
            except:
                print(
                    'Oops! An Error: There is a problem with a file, which you have tried to save.')

        button_export_tree_as_list.clicked.connect(
            button_export_tree_as_list_clicked)
        vbox.addWidget(button_export_tree_as_list)

        button_export_avl_tree_as_list = QPushButton()
        button_export_avl_tree_as_list.setText(
            self._global_variables.default_dict.get('export_avl_tree_as_list'))

        def button_export_avl_tree_as_list_clicked(arg):
            try:
                name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                self._global_variables.default_dict.get(
                                                                    'save_file'),
                                                                '.json', 'Json Files (*.json)')
                if name:
                    tree_manager = TreeManager()
                    tree_manager.write_tree_to_json_file_as_list(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].avl_tree, name)
                    print_avl_tree()
            except:
                print(
                    'Oops! An Error: There is a problem with a file, which you have tried to save.')

        button_export_avl_tree_as_list.clicked.connect(
            button_export_avl_tree_as_list_clicked)
        vbox.addWidget(button_export_avl_tree_as_list)

        empty_label_2 = QLabel('')
        vbox.addWidget(empty_label_2)

        button_print_average_height = QPushButton()
        button_print_average_height.setText(
            self._global_variables.default_dict.get('print_average_height_of_avl_tree'))

        def button_print_average_height_clicked(arg):
            self.text_edit.clear()
            avl = AVL()
            _avl_tree_as_list = [i for i in self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.get_tree_as_list() if i]
            for i, v in enumerate(_avl_tree_as_list):
                avl.insert_element(v)
            average_height = avl.get_average_height()
            self.text_edit.append(self._global_variables.default_dict.get(
                'average_height_of_avl_tree') + str(average_height))

        button_print_average_height.clicked.connect(
            button_print_average_height_clicked)
        vbox.addWidget(button_print_average_height)

        button_print_most_frequent_element = QPushButton()
        button_print_most_frequent_element.setText(
            self._global_variables.default_dict.get('print_most_frequent_elements'))

        def button_print_most_frequent_element_clicked(arg):
            tree_manager = TreeManager()
            # list_of_frequency = self.connector.list_of_menu_instances[
            #     instance_menu.id_of_instance].tree.get_list_of_frequency()
            list_of_frequency = self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.print_the_most_frequent_element()
            # print_list(list_of_frequency, 5)
            _print_list(list_of_frequency)
        button_print_most_frequent_element.clicked.connect(
            button_print_most_frequent_element_clicked)
        vbox.addWidget(button_print_most_frequent_element)

        button_print_list_of_frequency = QPushButton()
        button_print_list_of_frequency.setText(
            self._global_variables.default_dict.get('print_list_of_frequency'))

        def button_print_list_of_frequency_clicked(arg):
            tree_manager = TreeManager()
            list_of_frequency = self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.get_list_of_frequency()
            print_list(list_of_frequency, len(list_of_frequency))
        button_print_list_of_frequency.clicked.connect(
            button_print_list_of_frequency_clicked)
        vbox.addWidget(button_print_list_of_frequency)

        def set_value_to_check_the_sum_of_digits_of_node():
            spinBox_value_to_check_the_sum_of_digits_of_node.setMaximum(100)
            if spinBox_value_to_check_the_sum_of_digits_of_node.value(
            ) <= spinBox_value_to_check_the_sum_of_digits_of_node.value():
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].value_to_check_the_sum_of_digits_of_node = float(
                        str(spinBox_value_to_check_the_sum_of_digits_of_node.value()))

        spinBox_value_to_check_the_sum_of_digits_of_node = QDoubleSpinBox()
        spinBox_value_to_check_the_sum_of_digits_of_node.valueChanged.connect(
            set_value_to_check_the_sum_of_digits_of_node)
        vbox.addWidget(spinBox_value_to_check_the_sum_of_digits_of_node)

        button_print_list_of_needed_values = QPushButton()
        button_print_list_of_needed_values.setText(
            self._global_variables.default_dict.get('print_list_of_needed_values'))

        def button_print_list_of_needed_values_clicked(arg):
            avl = AVL()
            _avl_tree_as_list = [i for i in self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].tree.get_tree_as_list() if i]
            for i, v in enumerate(_avl_tree_as_list):
                avl.insert_element(v)
            print_dict(avl.get_list_of_needed_values(self.connector.list_of_menu_instances[
                instance_menu.id_of_instance].value_to_check_the_sum_of_digits_of_node))
        button_print_list_of_needed_values.clicked.connect(
            button_print_list_of_needed_values_clicked)
        vbox.addWidget(button_print_list_of_needed_values)

        empty_label_3 = QLabel('')
        vbox.addWidget(empty_label_3)

        button_delete_tree = QPushButton()
        button_delete_tree.setText(
            self._global_variables.default_dict.get('delete_tree'))

        def button_delete_tree_clicked(arg):
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].tree.delete_tree(
            )
            self.connector.list_of_menu_instances[instance_menu.id_of_instance].avl_tree.delete_tree(
            )
            print_tree()
        button_delete_tree.clicked.connect(button_delete_tree_clicked)
        vbox.addWidget(button_delete_tree)

        content = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(content)
        box = CollapsibleBox(self._global_variables.default_dict.get(
            'additional_options_of_the_instance'))

        info_label = QLabel('')
        update_info_label()

        vlay.addWidget(name)
        vlay.addWidget(info_label)
        vlay.addWidget(button_pretty_print_tree_to_text_edit)
        vlay.addWidget(button_pretty_print_avl_tree_to_text_edit)
        vlay.addWidget(box)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)
        vlay.addItem(verticalSpacer)

        box.setContentLayout(vbox)
        vlay.addStretch()

        frame_ = QtWidgets.QFrame()
        frame_.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)

        frame_.setLayout(vlay)
        self.QVBox_layout_of_dock_options.addWidget(frame_)

    def set_a_project(self):
        if self.connector is None:
            self.connector = Connector()
            self.connector.current_widget_to_export = self.text_edit
            self.set_options_dock()

    def clear_textedit(self):
        self.text_edit.clear()

    def close_application(self):
        msg = QMessageBox()
        msg.setWindowTitle(
            self._global_variables.default_dict.get('confirm_exit'))
        msg.setText(self._global_variables.default_dict.get(
            'are_you_sure_you_want_to_exit'))
        okButton = msg.addButton(self._global_variables.default_dict.get('yes'),
                                 QMessageBox.AcceptRole)
        msg.addButton(self._global_variables.default_dict.get(
            'no'), QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() == okButton:
            sys.exit()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.close_application()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    myapp = Application()
    myapp.show()
    sys.exit(app.exec_())

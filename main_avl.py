class AVL:
    """Base Class representing a Binary Search Tree Structure"""

    class AVLNode:
        __slots__ = ["_value", "_height", "_left", "_right"]
        """Private class for storing linked nodes with values and references to their siblings"""
        def __init__(self, value):
            """Node Constructor with 3 attributes"""
            self._value = value     # value being added
            self._left = None       # left sibling node (if val less than parent)
            self._right = None      # right sibling node (if val greater than parent)
            self._height = 0

    def __init__(self):
        """Binary Tree Constructor (creates an empty binary tree)"""
        self._root = None     # Binary tree root

    def get_root(self):
        return self._root

    def insert_element(self, value):
        """Method to insert an element into the BST"""
        self._root = self._insert_element(value, self._root)  # insert an element, calls recursive function

    def _insert_element(self, value, node):
        """Private method to Insert elements recursively"""
        # if node._value == value:  # if we come across a value already in the list
        #    raise ValueError
        if node is None:
            return AVL.AVLNode(value)
        # if node._value == value:  # if we come across a value already in the list
        #    node._right = self._insert_element(value, node._right)
        if value < node._value:
             node._left = self._insert_element(value, node._left)
        elif value > node._value:  # if a right node child node exists
            node._right = self._insert_element(value, node._right)
        node._height = self.height(node)
        return self.balance(node)

    def get_height_by_value(self, value):
        """Returns Height if value is in tree"""
        current_node = self._root
        while current_node is not None:
            if value == current_node._value:
                return self.height(current_node) # found
            elif value < current_node._value:
                current_node = current_node._left
            else:
                current_node = current_node._right
        return None # "Value not Found in Tree!"

    def find(self, value):
        """Return True if value is in tree"""
        current_node = self._root
        if type(value) == type(self._root):
            while current_node is not None:
                if value == current_node._value:
                    return True # found
                elif value < current_node._value:
                    current_node = current_node._left
                else:
                    current_node = current_node._right
        return None # "Value not Found in Tree!"

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
        elif node._left is not None and node._right is not None: # 2 kids
            temp = self.get_min(node._right)
            node._value = temp._value
            node._right = self._remove_element(temp._value, node._right)
        elif node._left is None:  # One right child
            node = node._right
                #del temp
        else:                     # One left child
            node = node._left
        # node._height = self.height(node)
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
    
    def get_list_of_needed_values(self, N): # N means a sum of digits of node
        _list = self.pre_order_to_list([])
        _list_of_needed_values = []
        d = {}
        try:
            for _, v in enumerate(_list):
                _sum = 0
                # for i in str(v):
                #     _sum += int(i)
                _sum = sum(int(ch) for ch in str(v) if ch.isdigit())
                if _sum > N:
                    # _list_of_needed_values.append(v)
                    # _list_of_needed_values.append([v, self.get_height_by_value(v)])
                    d[v] = self.get_height_by_value(v)
        except:
            print("Error: There are not only digits in the Tree but also non-digit chars")
        return d
        # return _list_of_needed_values

    def get_average_height(self): # N means a sum of digits of node
        _list = self.pre_order_to_list([])
        _list_of_heights = []
        value_to_return = 0
        try:
            for _, v in enumerate(_list):
                _list_of_heights.append(self.get_height_by_value(v))
            value_to_return = sum(_list_of_heights) / len(_list_of_heights)
        except:
            print("Error: There are not only digits in the Tree but also non-digit chars")
        return value_to_return

    def print_dict(self, d: dict):
        if d:
            for k, v in d.items():
                print(k, v)
        else:
            print('Empty dictionary of values with height')


if __name__ == '__main__':
    # avl = AVL()
    # #print("Height of Tree; " + str(avl.height(avl)))
    
    # avl.insert_element(60)
    # avl.insert_element(64)
    # avl.insert_element(63)
    # avl.insert_element(60)
    # avl.insert_element(60)
    # avl.insert_element(61)
    
    # avl.insert_element(40)
    # avl.insert_element(95)
    # avl.insert_element(87)
    # avl.insert_element(44)
    # avl.insert_element(6)
    # avl.insert_element(61)
    # avl.insert_element(9)
    # avl.insert_element(60)
    # avl.insert_element(28)
    # avl.insert_element(15)
    # avl.remove_element(61)
    
    # avl.insert_element(60)
    # avl.insert_element(64)
    # avl.insert_element(63)
    # avl.insert_element(60)
    # avl.insert_element(60)
    # avl.insert_element(61)
    
    # # avl.insert_element(8.4)
    # # avl.insert_element(28.6)
    # # avl.insert_element(15.4)
    # # avl.insert_element(43.6)
    # # avl.insert_element(10.4)
    # # avl.insert_element(8.6)
    # # avl.insert_element(9.4)
    # # avl.insert_element(23.6)
    
    # # avl.insert_element("Hey")
    # # avl.insert_element("How")
    # # avl.insert_element("Are")
    # # avl.insert_element("You")
    # # avl.insert_element("&^?")
    
    # a = avl.get_root()
    # print("Height of Tree: " + str(avl.height(a)))
    # print("Printing Tree (Pre-Order): " + str(avl.pre_order()))
    # print("-------------------")
    # print("Printing Tree (In-Order): " + str(avl.in_order()))
    # print("-------------------")
    
    # print(avl.pre_order_to_list([]))
    
    # d = avl.get_list_of_needed_values(1)
    # avl.print_dict(d)
    
    # print(avl.find(60))
    
    # ================
    
    import random
    _from = -99
    _to = 99
    _number_of_elements = 400
    _list = [random.randint(_from, _to) for i in range(_number_of_elements)]
    avl = AVL()
    
    for i, v in enumerate(_list):
        avl.insert_element(v)

    print(avl.pre_order_to_list([]))
    print()

    # print("Height of Tree; " + str(avl.height(avl)))
    
    
    
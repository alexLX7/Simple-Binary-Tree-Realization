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
        list_to_print.append(prefix + ("└── " if isLeft else "┌── ") + str(node.v))
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
        list_to_print.append(prefix + ("└──  " if isLeft else "┌──  ") + str(node.v))
        if node.l:
            self._pretty_print_tree_to_the_list_double_spaces(
                list_to_print, node.l, prefix + ("         " if isLeft else "│      "), True)

    def pretty_print_tree_to_the_list_double_spaces(self):
        list_to_print = []
        self._pretty_print_tree_to_the_list_double_spaces(list_to_print, self.root)
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
                root.r = self.delete_node(root.r , temp.v) 
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
                        print('Value: ' + str(v[0]) + ', frequency: ' + str(v[1]))
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
        
        self._tree_name = 'tree_as_list' # for json format, saves tree as list with name '_tree_name'
        self._tree_type = 'tree_type'
        self._known_types = {"<class 'int'>": int, "<class 'float'>": float, "<class 'str'>": str}
        self._from = 0 # default int/float value of elements for random creation
        self._to = 30 # default int/float value of elements for random creation
        self._min_number_of_elements = 0
        self._max_number_of_elements = 1024 # it is not actual max number
    
    def _generate_list_of_int_with_repetitions(self, number_of_elements: int):
        _list = [random.randint(self._from, self._to) for i in range(number_of_elements)]
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
            _number_of_elements = self._validate_number_of_elements(number_of_elements)
            if input_type == "<class 'int'>":
                _list = self._generate_list_of_int_with_repetitions(_number_of_elements) 
            if input_type == "<class 'str'>":
                _list = self._generate_list_of_strings(_number_of_elements)    
            if input_type == "<class 'float'>":
                _list = self._generate_list_of_floats_wo_repetitions(_number_of_elements)
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


def demo():
    
    tree_0 = Tree(int) # empty tree, Nodes will be 'int' type 
    
    tree_manager = TreeManager()
    tree_1 = tree_manager.create_new_random_tree(str(int), 10) # create a new random Tree(int)
    tree_manager.write_tree_to_json_file_as_list(tree_1, 'saved_tree.json')
    
    tree_2 = tree_manager.read_tree_from_json_file('saved_tree.json')
    tree_manager.write_tree_to_file_as_tree(tree_2, 'saved_tree.txt')
    tree_2.pretty_print_tree()
    tree_2.print_a_few_most_frequent_elements()
    tree_2.print_most_frequent_element()
    tree_2.print_list_of_frequency()
    
    tree_3 = tree_manager.create_new_random_tree(str(int), 3)
    tree_3.add('123') # added '123' as new Node with value of int('123') to the leaf
    tree_3.pretty_print_tree()
    tree_3.delete_node(tree_3.root, '123')
    # Deletion starts from the root, removing the furthest Node with value int('123')
    tree_3.pretty_print_tree()


if __name__ == "__main__":
    
    demo()
    
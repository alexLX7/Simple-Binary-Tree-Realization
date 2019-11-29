import random
import time
import json
import string


class FileHandler():
    def __init__(self):
        super().__init__() 
    
    def print_data(self, data: dict):
        for k, v in data.items():
                    print('{}: {}'.format(k, v))
    
    def write_json_file(self, path: str, data: dict, indent=4):
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=indent)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
    
    def write_json_file_wo_indent(self, path: str, data: dict):
        try:
            with open(path, 'w') as f:
                json.dump(data, f)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
    
    def write_to_file_as_tree(self, current_tree, path: str):
        # pretty_print_to_txt
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
    def __init__(self):
        super().__init__()
        self.root = None

    def get_root(self):
        return self.root

    def add(self, val):
        if(self.root == None):
            self.root = Node(val)
        else:
            self._add(val, self.root)

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

        # original
        print(prefix + ("└── " if isLeft else "┌── ") + str(node.v))
        
        # debug
        # print(prefix + ("└── " if isLeft else "┌── ") + str(node.v) + ' (' +str(type(node.v)) +')')

        if node.l:
            self._pretty_print_tree(
                node.l, prefix + ("    " if isLeft else "│   "), True)

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
    
    def delete_node(self, root, key): 
        if not root: 
            return root  
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
        
    def _most_frequent(self):
        d = {}
        List = self.get_tree_as_list()
        count, itm = 0, ''
        for item in reversed(List):
            if item:
                d[item] = d.get(item, 0) + 1
                if d[item] >= count:
                    count, itm = d[item], item

        # print(itm)
        # print(count)
        # print()

        raw_list_of_frequency = []
        for key, value in sorted(d.items(), key=lambda item: item[1]):
            # print("%s: %s" % (key, value))
            raw_list_of_frequency.append([key, value])

        list_of_frequency = []
        for v in raw_list_of_frequency:
            list_of_frequency.append([v[0], v[1]])
        
        # for v in reversed(raw_list_of_frequency):
        #     list_of_frequency.append([v[0], v[1]])
        #     # print('Value: ' + str(v[0]) + ', frequency: ' + str(v[1]))

        return list_of_frequency
    
    def print_most_frequent_element(self):
        list_of_frequency = self._most_frequent()
        if list_of_frequency:
            print('Value: ' + str(list_of_frequency[-1][0]))
            print('Frequency: ' + str(list_of_frequency[-1][1]))
        else:
            print('list_of_frequency is empty')
    
    def print_list_of_frequency(self):
        list_of_frequency = self._most_frequent()
        if list_of_frequency:
            for v in reversed(list_of_frequency):
                print('Value: ' + str(v[0]) + ', frequency: ' + str(v[1]))
        else:
            print('list_of_frequency is empty')


class TreeValidator:
    def __init__(self, raw_data):
        super().__init__()
        self._valid_input = True
        self.tree_as_list = None
        
        data = self._check_validation_of_main_components(raw_data)
        if data:
            self._init(data)
        else:
            self._valid_input = False
    
    def _init(self, data: dict):
        self.tree_as_list = data['tree_as_list'] 
    
    def _check_validation_of_main_components(self, raw_data: dict):
        try:
            dict_to_return = {
                'tree_as_list': raw_data['tree_as_list']
            }
            return dict_to_return
        except:
            print('Error: Input is not correct.')
        return None


class TreeManager:  
    def __init__(self):
        super().__init__()
        self.tree = Tree()
        self._list = None
        self._from = 0
        self._to = 30
    
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
        if 0 < number_of_elements < 1024: 
            return number_of_elements
        return None
    
    def create_new_random_tree(self, type_to_check: str, number_of_elements: int):
        try:
            if self._validate_number_of_elements(number_of_elements):
                if type_to_check == 'int':
                    self._list = self._generate_list_of_int_with_repetitions(number_of_elements) 
                if type_to_check == 'str':
                    self._list = self._generate_list_of_strings(number_of_elements)    
                if type_to_check == 'float':
                    self._list = self._generate_list_of_floats_wo_repetitions(number_of_elements)
                for i, v in enumerate(self._list):
                    self.tree.add(v)
        except:
            print('Error: Could not generate the list.')
        return self.tree
    
    # def create_new_tree_from_imported_list_from_file(self):
    #     tree = self.file_manager.import_from_file()
    #     if tree:
    #         self.list_of_trees.append(tree) 
    #         # print()   
    #     else:
    #         print('Could not created tree')
    
    def print_tree(self, _id: int):
        self.list_of_trees[_id].pretty_print_tree()    


def demo():
    # =================
    # just a demo 
    # =================
    start = time.time()

    # samples
    # int with repetitions
    # _list = [random.randint(15, 25) for x in range(15)]
    # _list = [random.randint(1, 1000) for x in range(1000)]
    # int
    # _list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 36, 37, 38, 39]
    # _list = [21, 20, 18, 20, 19, 23, 20, 21, 17, 19, 19, 22, 17, 16, 17]
    _list = [20, 21, 20, 18, 19, 23, 21, 22, 20, 24, 17, 19, 21, 20, 19, 18, 22, 17, 20, 16, 17]
    # int without repeat
    # _list = random.sample(range(1,20), 10)
    # floats
    # _list = sample_floats(0, 10, 20) # this function is now a method in TreeManager Class which is under construction
    # strings
    # _list = ['ha', 'hc', 'hp', 'ah', 'b', 'y', 'hp', 'f', 'a', 'c', 'x']
    
    t = Tree()
    print(_list)
    print()
    for i, v in enumerate(_list):
        t.add(v)

    # print before deletion
    t.pretty_print_tree()    

    print('Tried to delete Nodes with value "21" 4 times')
    t.delete_node(t.root, 21)
    t.delete_node(t.root, 21)
    t.delete_node(t.root, 21)  # deleted all 3 Nodes with value 21
    t.delete_node(t.root, 21)  # wouldn't do anything if there is no any Node with this value
    print()
    
    # print after deletion
    t.pretty_print_tree()    

    # freq
    t.print_most_frequent_element()
    print()
    t.print_list_of_frequency()
    print("Process time: " + str(time.time() - start))  # Process time: 0.007252693176269531


if __name__ == "__main__":
    
    print()
    tm = TreeManager()
    _t = tm.create_new_random_tree('str', 50)
    _t.pretty_print_tree()
    
    # =================
    
    # _list = [20, 21, 20, 18, 19, 23, 21, 22, 20, 24, 17, 19, 21, 20, 19, 18, 22, 17, 20, 16, 17]
    
    # # _list = [random.randint(1, 1000) for x in range(500)]
    
    # t = Tree()
    # for i, v in enumerate(_list):
    #     t.add(v)
    # # t.pretty_print_tree()

    # # data_to_dump = {'tree_as_list': tuple(t.get_tree_as_list())} # with null
    # data_to_dump = {'tree_as_list': tuple([i for i in t.get_tree_as_list() if i])}
    
    # file_handler = FileHandler()
    # # file_handler.print_data(data_to_dump)
    # file_handler.write_json_file('input_0.json', data_to_dump)
    # file_handler.write_json_file_wo_indent('input_1.json', data_to_dump)
    # data = file_handler.read_json_file('input_1.json')
    
    # tree_validator = TreeValidator(data)
    # t_2 = Tree()
    # for i, v in enumerate(tree_validator.tree_as_list):
    #     # print(v)
    #     if v:
    #         t_2.add(v)
    # # t_2.pretty_print_tree()
    
    # =================
    # Design of possible GUI
    # leftside dock 
    # buttons:
    #
    # -trees-
    # buttons below
    # create tree from scratch
    # import tree from file
    # buttons for each tree instance
    # print tree to file as list
    # print tree to file as tree
    # delete current tree
    #
    # -nodes- (for each tree)
    # add node
    # delete node
    # check existance of node
    #
    # -functions- (for each tree)
    # print most freq element
    # print freq for current tree
    # 
    # 
    # rightside subwindow
    # textedit:
    # 
    # be able to clear textedit
    # readonly
    # =================
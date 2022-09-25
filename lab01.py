import numpy as np
 
INPUT_FILENAME = "test.dat"
 
class Node:
    def __init__(self, value, parent, childs):
        self.value = value
        self.parent = parent
        self.childs = childs

    def add_child(self, child):
        self.childs.append(child)
 
class MatrixBuilder:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.matrix = np.zeros(self.get_matrix_shape(), dtype=int)
 
    def get_matrix_shape(self):
        matrix_width = 0
 
        for x in self.data:
            matrix_width = int(max(x)) if int(max(x)) > matrix_width else matrix_width
 
        return (len(self.data), matrix_width)
 
    def get_matrix(self):
        counter = 0
        for x in self.data:
            for y in x:
                self.matrix[counter, y - 1] = 1 # input file indexing from 1
            counter = counter + 1
 
        return self.matrix
 
    def load_data(self):
        loaded_data = open(self.filename, 'r').read().splitlines()
        loaded_data_list = []
 
        for line in loaded_data:
            splitted_line = line.split(' ')
            filtered_list = list(filter(None, splitted_line)) # filtering empty string ('')
            loaded_data_list.append(list(map(int, filtered_list))) # parse into integers
 
        return loaded_data_list

class Tree():
    def __init__(self, headers, root):
        self.headers = headers
        self.root = root

    def generate_tree(self, node, depth=0):
        if depth > 3:
            return

        for x in range(node.value + 1, self.headers[-1] + 1):
            new_node = Node(x, node, [])
            self.generate_tree(new_node, depth+1)
            node.add_child(new_node)

    def print_tree(self):
        for x in self.root.childs:
            print(x.value)
            for y in x.childs:
                print("----" + str(y.value))
                for z in y.childs:
                    print("--------" + str(z.value))

def main():
    matrix_builder = MatrixBuilder(INPUT_FILENAME)
    matrix = matrix_builder.get_matrix()

    root = Node(0, None, [])
    tree = Tree(list(range(1, len(matrix[0]) + 1)), root)

    tree.generate_tree(tree.root)
    tree.print_tree()

if __name__ == "__main__":
    main()
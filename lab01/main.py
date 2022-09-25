import numpy as np
 
INPUT_FILENAME = "test.dat"

# chess.dat trios 17 223
 
# https://wikimedia.org/api/rest_v1/media/math/render/svg/56af28fde7223928b137f59d5cb1ce9bd62ce33b

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


    def get_pairs(self):
        pairs = []
        for x in self.root.childs:
            for y in x.childs:
                pairs.append((y.value, x.value))

        return pairs

    def get_trios(self):
        trios = []
        for x in self.root.childs:
            for y in x.childs:
                for z in y.childs:
                    trios.append((z.value, y.value, x.value))
        return trios

class SupportConfidenceFinder():
    def __init__(self, matrix, pairs, trios, support):
        self.matrix = matrix
        self.pairs = pairs
        self.trios = trios
        self.support = support

    def get_support_single(self, single):
        count = 0
        for x in self.matrix:
            if x[single - 1] == 1:
                count = count + 1

        return count / len(self.matrix)

    def get_support_pair(self, pair):
        count = 0
        for x in self.matrix:
            if x[pair[0] - 1] == 1 and x[pair[1] - 1] == 1:
                count = count + 1
    
        return count / len(self.matrix)

    def get_support_trio(self, trio):
        count = 0
        for x in self.matrix:
            if x[trio[0] - 1] == 1 and x[trio[1] - 1] == 1 and x[trio[2] - 1] == 1:
                count = count + 1
    
        return count / len(self.matrix)


    def sort_items(self, items):
        items_list = list(items)
        items_list.sort(key=self.get_support_single)
        return tuple(items_list)
    
    def get_supported_pairs(self):
        supported_pairs = []
        for x in self.pairs:

            if self.get_support_pair(x) > self.support:
                support = self.get_support_pair(x)
                items = self.sort_items(x)
                # return items with confidence
                supported_pairs.append([items, round(support / self.get_support_single(items[0]), 2)])

        return supported_pairs

    def get_supported_trios(self):
        supported_trios = []
        for x in self.trios:
            support = self.get_support_trio(x)
            if support > self.support:
                items = self.sort_items(x)
                supported_trios.append([items, round(support / self.get_support_pair((items[0], items[1])),2)])
        
        return supported_trios

def main():
    matrix_builder = MatrixBuilder(INPUT_FILENAME)
    matrix = matrix_builder.get_matrix()

    root = Node(0, None, [])
    tree = Tree(list(range(1, len(matrix[0]) + 1)), root)

    tree.generate_tree(tree.root)
    # tree.print_tree()

    support_finder = SupportConfidenceFinder(matrix, tree.get_pairs(), tree.get_trios(), 0.15)
    print(support_finder.get_supported_trios())

if __name__ == "__main__":
    main()

    
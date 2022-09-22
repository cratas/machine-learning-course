#use it
np.zeros()

class Node:
  def __init__(self, value, parent, childs):
    self.value = value
    self.parent = parent
    self.childs = childs

def generate():
    pass

def main():
    default_values = [0,1,2,3]
    root = Node(None, default_values)

    print("Hello World!")

if __name__ == "__main__":
    main()
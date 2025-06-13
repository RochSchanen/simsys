from toolbox import *

header()


class device():

    def __init__(self, name):
        self.D = []
        self.name = name
        return

    def add(self, d):
        self.D.append(d)
        return d

    def display(self, indent, last):
        for i, d in enumerate(self.D):
            print(f"{indent}<{i}>")
            d.display(f'{indent}<{self.name}>', len(self.D) == i)
        return


A = device('A')

B = A.add(device('B'))
C = A.add(device('C'))
D = C.add(device('D'))

A.display('A', True)

# tree symbols display
tree_v = f"\u0020\u2502\u0020".encode("utf-8")       
tree_s = f"\u0020\u251C\u2500".encode("utf-8")
tree_l = f"\u0020\u2514\u2500".encode("utf-8")
tree_n = f"\u0020\u0020\u0020".encode("utf-8")
""

print(tree_l)
print(tree_n)
print(tree_s)
print(tree_v)


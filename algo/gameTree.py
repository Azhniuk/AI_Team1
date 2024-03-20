from copy import deepcopy
from typing import Optional, Dict, List

# current number
# next numbers
# bank points
# p1 points
# p2 points
State = Dict[int, List[int], int, int , int]



class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None):
        self.children: List[Node] = []
        self.state: State = state
        self.is_dead_end: bool = False
        self.parent: Optional[Node] = parent

    #function that generates the descendants of the node
    def expand(self):
        if self.is_terminal():
            return
        #TODO


    def is_terminal(self) -> bool:
        if len(self.state[1]) == 0 and self.state[0] in [0,2,3,5]:
            return True
        return False

    def __print__(self):
        print("Current number :",self.state[0])
        print("Next numbers   :",self.state[1])
        print("Bank points    :",self.state[2])
        print("P1 points      :",self.state[3])
        print("P2 points      :",self.state[4])


class GameTree:

    def __init__(self):
        #self.root = #TODO
        self.node_count = 0

    def generate_tree(self):
        self.__expand(self.root)


    def __expand(self, node: Node):
        node.expand()
        self.node_count += 1
        for child in node.children:
            self.__expand(child)

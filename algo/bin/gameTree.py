from copy import deepcopy
from typing import Optional, Dict, List

# current number
# bank points
# p1(human) points
# p2(bot) points
State = [int, int,int ,int]


StartNumber = 14334
humanTurn = True

StartState = [StartNumber,0,0,0]

class Node:
    def __init__(self, state: State, humanTurn: bool,parent: Optional['Node'] = None):
        self.children: List[Node] = []
        self.state: State = state
        self.humanTurn: bool = humanTurn
        self.parent: Optional[Node] = parent

    #function that generates the descendants of the node
    def expand(self):
        if self.is_terminal():
            return
        # check if divisible by 2
        if self.state[0] % 2 == 0:
            newnumber = self.state[0]//2
            newbank = self.state[1]
            hum = self.state[2]
            bot = self.state[3]

            if newnumber%2 == 0: # even
                if self.humanTurn:
                    hum += 1
                else: 
                    bot += 1
            else: # odd 
                if self.humanTurn:
                    hum -= 1
                else:
                    bot -= 1

            if newnumber%5 == 0:
                newbank+=1

            childState = [newnumber,newbank,hum,bot]
            self.children.append(Node(childState,humanTurn))

        # check if divisible by 3
        if self.state[0] % 3 == 0:
            newnumber = self.state[0]//2
            newbank = self.state[1]
            hum = self.state[2]
            bot = self.state[3]

            if newnumber%2 == 0: # even
                if self.humanTurn:
                    hum += 1
                else: 
                    bot += 1
            else: # odd 
                if self.humanTurn:
                    hum -= 1
                else:
                    bot -= 1

            if newnumber%5 == 0:
                newbank+=1

            childState = [newnumber,newbank,hum,bot]
            self.children.append(Node(childState,humanTurn))


    def is_terminal(self) -> bool:
        if self.state[0] in [0,2,3,5]:
            return True
        return False

    def __print__(self):
        print("Current number :",self.state[0])
        print("Bank points    :",self.state[1])
        print("P1 points      :",self.state[2])
        print("P2 points      :",self.state[3])


class GameTree:

    def __init__(self):
        self.root = Node(StartState,humanTurn)
        self.node_count = 0

    def generate_tree(self):
        self.__expand(self.root)


    def __expand(self, node: Node):
        node.expand()
        self.node_count += 1
        for child in node.children:
            self.__expand(child)

gt = GameTree()
gt.generate_tree();


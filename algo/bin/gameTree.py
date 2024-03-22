from typing import Optional, List
import random

# current number
# bank points
# p1(human) points
# p2(bot) points
State = [int, int,int ,int]

x = 1
while x % 6 != 0:
    x = random.randint(10000,20000)

StartNumber = x
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
            self.children.append(Node(childState,not self.humanTurn))

        # check if divisible by 3
        if self.state[0] % 3 == 0:
            newnumber = self.state[0]//3
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
            self.children.append(Node(childState,not self.humanTurn))


    def is_terminal(self) -> bool:
        if self.state[0] in [0,2,3,5]:
            return True
        return False

    def __print__(self):
        if self.humanTurn:
            print("human turn now.")
        else:
            print("bot turn now.")
        print("Current number :",self.state[0])
        print("Bank points    :",self.state[1])
        print("human points   :",self.state[2])
        print("bot points     :",self.state[3])
        print()


class GameTree:

    def __init__(self):
        self.root = Node(StartState,humanTurn)
        self.node_count = 0

    def generate_tree(self):
        self.__expand(self.root)


    def __expand(self, node: Node):
        node.expand()
        node.__print__()
        self.node_count += 1
        for child in node.children:
            self.__expand(child)

    def print_root(self):
        self.root.__print__()

    # returns a tuple, the value expected and the direction to take
    
    # for the expected value :
    # 1 means bot victory
    # -1 means human victory
    # 0 means draw

    # for the direction to take
    # 0 means take the only viable option
    # 1 means take the left aka /2
    # 2 means take the right aka /3

    def minimax(self, node=None, mini=True):
        if node == None:
            node = self.root
        n = len(node.children)
        if n == 0:
            if node.state[2] > node.state[3]: # human victory
                return -1,0
            elif node.state[2] < node.state[3]: # bot victory
                return 1,0
            else: # draw
                return 0,0
        if n == 1:
            return self.minimax(node.children[0],not mini)[0],0
        left = self.minimax(node.children[0],not mini)[0]
        right = self.minimax(node.children[1],not mini)[0]
        if left < right:
            if mini:
                return left,1
            else:
                return right,2
        else:
            if mini:
                return right,2
            else:
                return left,1



gt = GameTree()
gt.generate_tree()
print(gt.node_count)
print(gt.minimax())


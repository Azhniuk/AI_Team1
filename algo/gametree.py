import copy


class Node:
    def __init__(self, id,  number, human_score, ai_score, bank, level):
        self.id = id
        self.number = number
        self.human_score = human_score
        self.ai_score = ai_score
        self.bank = bank
        self.level = level

# Дополнительные требования к программному обеспечению
# В начале игры игровое программное обеспечение случайным образом генерирует 5 чисел в диапазоне
# от 10000 до 20000, но те, которые изначально делятся и на 3, и на 2. Игрок-человек выбирает
# с какого из сгенерированных чисел он хочет начать игру.
# Описание игры
# В начале игры дается число, выбранное игроком-человеком. У обоих игроков 0
# точки. Кроме того, в игре используется игровой банк, который изначально равен 0. Игроки делают
# последовательные ходы, деля текущее число на 2 или 3 в каждом ходе. Число можно разделить
# только если результат является целым числом. Если в результате деления получается четное число, то игрок получает 1
# балл, если число нечетное, то его баллы уменьшаются на 1 балл. С другой стороны, если число
# получается окончание на 0 или 5, тогда в банк добавляется 1 очко. Игра заканчивается, когда число 2
# или 3 приобретено. Игрок, после хода которого выпало число 2, опустошает банк, добавляя
# банк указывает на свои очки. Побеждает игрок, набравший большее количество очков в конце игры.
# Если количество очков равно, то результатом является ничья.
class Game_tree:
    def __init__(self, number):
        self.prime_node = Node(1, number, 0, 0, 0, 1)
        self.set_of_prime_nodes = []
        self.set_of_nodes = []
        self.dictionary = dict()
        self.coeffs = [2, 3]
        self.create_tree(self.prime_node)

    # def adding_node(self, Node):
    #     self.set_of_nodes.append(Node)

    def adding_node_to_layer(self, initial_node_id, end_node_id):
        self.dictionary[initial_node_id] = self.dictionary.get(initial_node_id, []) + [end_node_id]

    def generate_prime_tree(self):
        self.create_tree(self.prime_node)
        self.set_of_prime_nodes = copy.deepcopy(self.set_of_nodes)
        self.set_of_nodes.clear()

    def find_node(self, number, level):
        for i in self.set_of_prime_nodes:
            if number == i.number and level == i.level:
                return i

        return None
    # def create_tree(self, initial_node):
    #     self.set_of_nodes.append(initial_node)
    #     j = initial_node.id + 1
    #     upper_layer = [initial_node]
    #     lower_layer = []
    #     human_score = 0
    #     ai_score = 0
    #     bank_score = 0
    #     while len(upper_layer) > 0:
    #         for i in upper_layer:
    #             numbers = []
    #             number = 0
    #             if i.number != 2 and i.number != 3:
    #                 if i.number % 2 == 0:
    #                     number = i.number // self.coeffs[0]
    #                     numbers.append(number)
    #                 if i.number % 3 == 0:
    #                     number = i.number // self.coeffs[1]
    #                     numbers.append(number)
    #
    #                 for k in numbers:
    #                     if (i.level + 1) % 2 == 0:
    #                         ai_score = i.ai_score
    #                         if k % 2 == 0:
    #                             human_score = i.human_score + 1
    #                         else:
    #                             human_score = i.human_score - 1
    #
    #                         if k % 5 == 0:
    #                             bank_score = i.bank + 1
    #                         if k == 2:
    #                             human_score += bank_score
    #
    #                     else:
    #                         human_score = i.human_score
    #
    #                         if k % 2 == 0:
    #                             ai_score = i.ai_score + 1
    #                         else:
    #                             ai_score = i.ai_score - 1
    #
    #                         if k % 5 == 0:
    #                             bank_score = i.bank + 1
    #
    #                         if k == 2:
    #                             ai_score += bank_score
    #
    #                     node = Node(j, k, human_score, ai_score, bank_score, i.level + 1)
    #                     lower_layer.append(node)
    #                     self.set_of_nodes.append(node)
    #                     self.adding_node_to_layer(i.id, node.id)
    #                     j += 1
    #         upper_layer = copy.deepcopy(lower_layer)
    #         lower_layer.clear()

    # def create_tree(self, initial_node):
    #     self.set_of_nodes = [initial_node]  # Reset or initialize the node list with the initial node
    #     next_id = 2  # Assuming initial_node has ID 1
    #
    #     # Use a queue for BFS-like tree generation
    #     queue = [initial_node]
    #
    #     while queue:
    #         current_node = queue.pop(0)  # Get the first node from the queue
    #
    #         if current_node.number in [2, 3]:
    #             continue  # Skip expansion for terminal nodes
    #
    #         for coeff in self.coeffs:  # self.coeffs should be [2, 3]
    #             if current_node.number % coeff == 0:
    #                 new_number = current_node.number // coeff
    #                 human_score, ai_score, bank_score = current_node.human_score, current_node.ai_score, current_node.bank
    #
    #                 # Update scores based on the game rules
    #                 score_change = 1 if new_number % 2 == 0 else -1
    #                 if (current_node.level + 1) % 2 == 0:  # AI's turn
    #                     ai_score += score_change
    #                 else:  # Human's turn
    #                     human_score += score_change
    #
    #                 if new_number % 10 == 0 or new_number % 10 == 5:
    #                     bank_score += 1
    #
    #                 # Create a new node and add it to the tree
    #                 new_node = Node(next_id, new_number, human_score, ai_score, bank_score, current_node.level + 1)
    #                 self.set_of_nodes.append(new_node)
    #                 queue.append(new_node)
    #
    #                 next_id += 1

    def create_tree(self, initial_node):
        # Simplify the logic to avoid unnecessary complexity and focus on tree generation for valid moves.
        queue = [initial_node]
        next_id = 2  # Start ID for new nodes

        while queue:
            current_node = queue.pop(0)
            if current_node.number in [2, 3]: continue

            for coeff in self.coeffs:
                if current_node.number % coeff == 0:
                    new_number = current_node.number // coeff
                    # Assume AI and human turns alternate starting with human; adjust scoring logic accordingly.
                    is_ai_turn = current_node.level % 2 == 0
                    ai_score, human_score = current_node.ai_score, current_node.human_score
                    bank = current_node.bank + 1 if new_number % 10 == 0 or new_number % 10 == 5 else current_node.bank

                    if new_number % 2 == 0:
                        if is_ai_turn:
                            ai_score += 1
                        else:
                            human_score += 1
                    else:
                        if is_ai_turn:
                            ai_score -= 1
                        else:
                            human_score -= 1

                    new_node = Node(next_id, new_number, human_score, ai_score, bank, current_node.level + 1)
                    self.set_of_nodes.append(new_node)
                    queue.append(new_node)
                    next_id += 1

    def minimax(self, node, depth, is_maximizing_player):
        if node.number in [2, 3]:
            return self.evaluate(node), None

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for coeff in self.coeffs:
                if node.number % coeff == 0:  # Check for valid moves
                    new_node = self.simulate_move(node, coeff, is_maximizing_player)
                    eval, _ = self.minimax(new_node, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = coeff
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for coeff in self.coeffs:
                if node.number % coeff == 0:  # Check for valid moves
                    new_node = self.simulate_move(node, coeff, is_maximizing_player)
                    eval, _ = self.minimax(new_node, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = coeff
            return min_eval, best_move

    def simulate_move(self, node, coeff, is_maximizing_player):
        new_number = node.number // coeff
        # Initialize score changes based on the current move
        score_change = 1 if new_number % 2 == 0 else -1
        bank_change = 1 if new_number % 10 == 0 or new_number % 10 == 5 else 0

        if is_maximizing_player:  # AI's turn
            ai_score = node.ai_score + score_change
            human_score = node.human_score  # Human score remains unchanged
        else:  # Human's turn
            human_score = node.human_score + score_change
            ai_score = node.ai_score  # AI score remains unchanged

        # Update the bank based on the game's rules
        bank = node.bank + bank_change

        # Create and return a new node representing the state after the move
        return Node(node.id + 1, new_number, human_score, ai_score, bank, node.level + 1)

    def evaluate(self, node):
        score_diff = node.ai_score - node.human_score
        bank_bonus = node.bank if node.number == 2 else 0
        endgame_bonus = 100 if node.number == 2 else (-100 if node.number == 3 else 0)

        # Strategic consideration: Prefer even numbers, avoid 3 unless it's a winning move
        number_preference = 0
        if node.number % 2 == 0:
            number_preference = 20  # Arbitrary value to favor even numbers
        if node.number == 3:
            number_preference = -20  # Discourage ending up with 3 unless it's for a win

        return score_diff + bank_bonus + endgame_bonus + number_preference



import random
import gametree as gt
class Player:
    def __init__(self):
        self.chosen_number = 0
        self.score = 0

    def choose_number(self, number):
        self.chosen_number = number

    def add_score(self, score):
        self.score += score


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
 #10368, 11664, 12288, 13122, 13824.


class Game_Logic:
    def __init__(self):
        self.game_bank = 0
        self.current_number = 0
        self.players = [Player(), Player()]
        self.turn = 0


    def get_5_random_numbers(self):
        def gen_number():
            number = 1
            while number < 10000:
                number *= random.randint(2, 3)
                if number > 20000:
                    number = 1

            return number

        numbers = []
        while len(numbers) < 5:
            number = gen_number()
            if number not in numbers:
                numbers.append(number)

        return numbers

    def start_game(self, chosen_number):
        self.gt = gt.Game_tree(chosen_number)
        self.current_number = chosen_number

    def divide_number(self, divisor):
        if divisor in [2, 3]:
            if self.current_number % divisor == 0:
                self.current_number //= divisor

            return self.current_number
        else:
            return self.current_number

    def check_score(self):
        if self.current_number % 2 == 0:
            self.players[self.turn].add_score(1)
        else:
            self.players[self.turn].add_score(-1)

        if self.current_number % 10 == 0 or self.current_number % 10 == 5:
            self.game_bank += 1

        if self.current_number == 2:
            self.players[self.turn].add_score(self.game_bank)

        self.turn = 1 - self.turn

    def check_game_end(self):
        return self.current_number in [2, 3]

    def play_game(self):
        while not self.check_game_end():
            if self.turn % 2 == 0:  # Human player's turn
                divisor = int(input("Enter divisor 2|3: "))
                self.divide_number(divisor)
            else:
                _, coef = self.gt.minimax(self.gt.prime_node, 4, True)
                print(f"AI has chosen coefficient {coef}")
                self.divide_number(coef)
            self.check_score()
            print(f"Number: {self.current_number}\nScore Human: {self.players[0].score}\nScore AI: {self.players[1].score}\nBank: {self.game_bank}")

        player_scores = [player.score for player in self.players]

        if player_scores[0] > player_scores[1]:
            print("Player wins!")
        elif player_scores[0] < player_scores[1]:
            print("AI wins!")
        else:
            print("It's a draw!")

        return player_scores


game_logic = Game_Logic()
random_numbers = game_logic.get_5_random_numbers()

print("Numbers", random_numbers)

chosen_number = int(input("Enter chosen number: "))

game_logic.start_game(chosen_number)
final_scores = game_logic.play_game()
print("Final scores:", final_scores)
print("Bank: ", game_logic.game_bank)


#1. не генерировать истинно ранд числа поскольку существует только 8 чисел множетели которых будут только 2 или 3.
# банк не работает потому что число которое заканчивается на 0 или 5, значит у нее множитель 5, при остаточном делении 5 на 2 или 3 игра ломается. конечный результат деления не будет 2 или 3
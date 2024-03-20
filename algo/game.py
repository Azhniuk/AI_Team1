import game_tree as gt

class Player:
    def __init__(self):
        self.score = 0

    def add_score(self, score):
        self.score += score

class Game_logic:
    def __init__(self):
        self.random_number = 0
        self.players = [Player(), Player()]
        self.bank_score = 0
        self.turn = 0
        self.level = 1

    def choose_number(self):
        while self.random_number < 25 or self.random_number > 40:
            self.random_number = int(input("Enter a random number from 25 to 40: "))
            if 25 <= self.random_number <= 40:
                print(f"Your chosen number is {self.random_number}")
                self.gt = gt.Game_tree(self.random_number)
            else:
                print("Your number is out of range. Please try again.")

    def multiply_number(self):
        coef = int(input("Choose a coefficient (from 2 to 4): "))
        if coef in [2, 3, 4]:
            self.random_number *= coef
            self.check_score()
        else:
            print("Invalid coefficient. Please choose again.")

    def check_score(self):
        if self.random_number % 2 == 0:
            self.players[self.turn].add_score(-1)
        else:
            self.players[self.turn].add_score(1)

        if self.random_number % 5 == 0:
            self.bank_score += 1

        if self.random_number >= 5000:
            self.players[self.turn].add_score(self.bank_score)
            self.bank_score = 0

        self.turn = 1 - self.turn

    def check_end(self):
        return self.random_number >= 5000

    def start_game(self):
        self.choose_number()
        while not self.check_end():
            if self.turn % 2 == 0:  # Human player's turn
                print(f"----------------------------------------Player {self.turn + 1} turn----------Round: {self.level} ------------------------------")
                coef = int(input("Choose a coefficient (from 2 to 4): "))
                self.random_number *= coef
                self.check_score()
            else:  # AI's turn
                print(f"----------------------------------------Player {self.turn + 1} turn----------Round: {self.level} ------------------------------")
                coef = self.gt.move_checking(self.random_number, self.level)
                print(f"AI has chosen coefficient {coef}.")
                self.random_number *= coef
                self.check_score()

            print(f"Number: {self.random_number}\nScore Human: {self.players[0].score}\nScore AI: {self.players[1].score}\nBank: {self.bank_score}")
            self.level += 1

        if self.players[0].score > self.players[1].score:
            print("Human wins!")
        elif self.players[0].score < self.players[1].score:
            print("AI wins!")
        else:
            print("It's a draw!")

game1 = Game_logic()
game1.start_game()
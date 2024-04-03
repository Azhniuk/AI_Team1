import pygame
import random
import time


pygame.init()

def get_5_random_numbers():
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

class Node:
    def __init__(self, number, ai_hum_scores, bank, isHumanTurn, divisor):
        self.number = number
        self.ai_hum_scores = ai_hum_scores.copy()
        self.bank = bank
        self.isHumanTurn = isHumanTurn
        self.children = []
        self.divisor = divisor


class Game_tree:
    def __init__(self, number, isHumanTurn):
        self.current_node = Node(number, [0, 0], 0, not isHumanTurn, 1)
        self.create_tree(self.current_node)

    def check_score(self, node):
        if node.number in [2, 3]:
            node.ai_hum_scores[node.isHumanTurn] += node.bank
            node.bank = 0
            return node

        if node.number % 2 == 0:
            node.ai_hum_scores[node.isHumanTurn] -= 1
        else:
            node.ai_hum_scores[node.isHumanTurn] += 1
        if node.number % 5 == 0:
            node.bank += 1
        return node

    def check_win(self, node):
        return node.number in [2, 3]

    def create_tree(self, node):
        if self.check_win(node):
            return

        for divisor in [2, 3]:
            if node.number % divisor == 0:
                new_number = node.number // divisor
                new_node = self.check_score(
                    Node(new_number, node.ai_hum_scores, node.bank, not node.isHumanTurn, divisor=divisor))
                node.children.append(new_node)
                self.create_tree(new_node)

    def make_move(self, divisor):
        if divisor == 2 or divisor == 3:
            for child in self.current_node.children:
                if child.divisor == divisor:
                    self.current_node = child
                    return True
        return False


class Game_logic:
    def __init__(self, number, isHumanTurn):
        self.gt = Game_tree(number, isHumanTurn)
        self.nodes_visited = 0

    def alpha_beta(self, node, depth, alpha, beta, maximizing_playerTurn):
        self.nodes_visited += 1

        if depth == 0 or self.gt.check_win(node):
            return node.ai_hum_scores[False] - node.ai_hum_scores[True]

        if maximizing_playerTurn:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.alpha_beta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.alpha_beta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move_alpha_beta(self, node):
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for child in node.children:
            eval = self.alpha_beta(child, 4, alpha, beta, False)
            if eval > best_eval:
                best_eval = eval
                best_move = child
        return best_move

    def minimax(self, node, maximizing_playerTurn):
        self.nodes_visited += 1
        if node.children == []:
            return node.ai_hum_scores[False] - node.ai_hum_scores[True]

        if maximizing_playerTurn:
            best_value = float('-inf')
            for child in node.children:
                value = self.minimax(child, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for child in node.children:
                value = self.minimax(child, True)
                best_value = min(best_value, value)
            return best_value

    def find_best_move_minimax(self, node):
        best_value = float('-inf')
        best_move = None
        for child in node.children:
            value = self.minimax(child, False)
            if value > best_value:
                best_value = value
                best_move = child
        return best_move


class Player:
    def __init__(self):
        self.score = 0

    def add_score(self, score):
        self.score += score

# Game objects
player_score = 0
ai_score = 0
bank = 0


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Divide and Conquer")

# Dialog parameters
DIALOG_WIDTH = 400
DIALOG_HEIGHT = 300
DIALOG_X = (SCREEN_WIDTH - DIALOG_WIDTH) // 2
DIALOG_Y = (SCREEN_HEIGHT - DIALOG_HEIGHT) // 2
DIALOG_PADDING = 20

SAVE_BUTTON_WIDTH = 75
SAVE_BUTTON_HEIGHT = 30
SAVE_BUTTON_X = DIALOG_X + DIALOG_WIDTH // 2 - SAVE_BUTTON_WIDTH // 2
SAVE_BUTTON_Y = DIALOG_Y + DIALOG_HEIGHT - 80
save_button_rect = pygame.Rect(SAVE_BUTTON_X, SAVE_BUTTON_Y, SAVE_BUTTON_WIDTH, SAVE_BUTTON_HEIGHT)


NUMBER_BUTTON_WIDTH = 300
NUMBER_BUTTON_HEIGHT = 30
NUMBER_BUTTON_X = SAVE_BUTTON_X/4*3
NUMBER_BUTTON_Y = SAVE_BUTTON_Y - 50
number_button_rect = pygame.Rect(NUMBER_BUTTON_X, NUMBER_BUTTON_Y - 20, NUMBER_BUTTON_WIDTH, NUMBER_BUTTON_HEIGHT)

# Fonts
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 26)
checkbox_font = pygame.font.Font(None, 24)


whosfirst = True
algo = "Alpha-Beta"
game_started = False
evaluation_time = 0
numbers = get_5_random_numbers()
n= 0
chosen_number = 12344

game_tree = Game_tree(chosen_number, whosfirst)
game_logic = Game_logic(chosen_number, whosfirst)
player1 = Player()
player2 = Player()
current_player = player1 if whosfirst else player2
opponent_player = player2 if whosfirst else player1


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_checkbox(checkbox_text, font, color, surface, x, y, checkbox_width=20, checkbox_height=20, checkbox_padding=5,
                  checked=False, circular=False):
    if circular:
        pygame.draw.circle(surface, BLACK, (x + checkbox_width // 2, y + checkbox_height // 2), checkbox_width // 2, 2)
    else:
        pygame.draw.rect(surface, BLACK, (x, y, checkbox_width, checkbox_height), 2)
        
    text_surface = font.render(checkbox_text, True, color)
    text_rect = text_surface.get_rect(topleft=(x + checkbox_width + checkbox_padding, y))
    surface.blit(text_surface, text_rect)
    if checked:
        pygame.draw.line(surface, BLACK, (x + 2, y + 2), (x + checkbox_width - 2, y + checkbox_height - 2), 2)
        pygame.draw.line(surface, BLACK, (x + checkbox_width - 2, y + 2), (x + 2, y + checkbox_height - 2), 2)
    return pygame.Rect(x, y, checkbox_width + text_rect.width + checkbox_padding, checkbox_height)


# Function to draw the dialog window
def draw_dialog():
    pygame.draw.rect(SCREEN, WHITE, (DIALOG_X, DIALOG_Y, DIALOG_WIDTH, DIALOG_HEIGHT))
    draw_text("Game Settings", font, BLACK, SCREEN, DIALOG_X + DIALOG_PADDING, DIALOG_Y + DIALOG_PADDING)
    human_turn_checkbox = draw_checkbox("Human's Turn", checkbox_font, BLACK, SCREEN, DIALOG_X + DIALOG_PADDING,
                                        DIALOG_Y + DIALOG_PADDING * 3, checked=whosfirst)
    ai_turn_checkbox = draw_checkbox("AI's Turn", checkbox_font, BLACK, SCREEN, DIALOG_X + DIALOG_PADDING,
                                     DIALOG_Y + DIALOG_PADDING * 4, checked=not whosfirst)
    algo_checkbox = draw_checkbox(f"Algorithm: {algo}", checkbox_font, BLACK, SCREEN, DIALOG_X + DIALOG_PADDING,
                                  DIALOG_Y + 15 + DIALOG_PADDING * 5, circular=True)
    
    number_checkbox = draw_checkbox(f"Choose number: {numbers[n]}", checkbox_font, BLACK, SCREEN, DIALOG_X + DIALOG_PADDING,
                                  DIALOG_Y+ 35 + DIALOG_PADDING * 5, circular=True)
    pygame.draw.rect(SCREEN, BLACK, save_button_rect)
    draw_text("Save", font, WHITE, SCREEN, SAVE_BUTTON_X + 10, SAVE_BUTTON_Y + 5)
    
    return human_turn_checkbox, ai_turn_checkbox, algo_checkbox, number_checkbox


def start_game():
    global game_tree, game_logic, current_player
    game_tree = Game_tree(chosen_number, whosfirst)
    game_logic = Game_logic(chosen_number, whosfirst)
    current_player = player1 if whosfirst else player2

def display_winner(winner, nodes_explored):
    pygame.display.set_caption("Game Over")
    dialog_font = pygame.font.Font(None, 48)
    if winner == "AI":
        message = "AI wins!"
    elif winner == "Human":
        message = "Human player wins!"
    else:
        message = "It's a draw!"
    text = dialog_font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    nodes_text = f"Nodes Explored by AI: {nodes_explored}"
    nodes_text_rendered = dialog_font.render(nodes_text, True, BLACK)
    nodes_text_rect = nodes_text_rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    SCREEN.blit(text, text_rect)
    SCREEN.blit(nodes_text_rendered, nodes_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()


# Main game loop
running = True
human_turn_checkbox, ai_turn_checkbox, algo_checkbox,number_checkbox = draw_dialog()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if human_turn_checkbox.collidepoint(mouse_pos):
                    whosfirst = True
                elif ai_turn_checkbox.collidepoint(mouse_pos):
                    whosfirst = False
                elif algo_checkbox.collidepoint(mouse_pos):
                    algo = "Alpha-Beta" if algo == "Minimax" else "Minimax"
                elif number_checkbox.collidepoint(mouse_pos):
                    if n<4:
                        n +=1
                    else:
                        n = 0
               
                elif save_button_rect.collidepoint(mouse_pos):
                    chosen_number = numbers[n]
                    start_game()
                    game_started = True
                    current_player = player1 if whosfirst else player2
                human_turn_checkbox, ai_turn_checkbox, algo_checkbox, number_checkbox = draw_dialog()

    if game_started:
        SCREEN.fill(WHITE)
        if current_player == player1:
            # Human player's turn
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 250 < mouse_pos[0] < 450 and 400 < mouse_pos[1] < 500:
                    divisor = 2
                elif 450 < mouse_pos[0] < 650 and 400 < mouse_pos[1] < 500:
                    divisor = 3
                else:
                    continue
                    
                
                if game_tree.make_move(divisor):
                    player_score += -1 if game_tree.current_node.number % 2 != 0 else 1
                    if game_tree.current_node.number % 5 == 0  or game_tree.current_node.number % 10  == 0:
                        game_tree.current_node.bank += 1  
                    current_player = player2   # Switch to AI player after human's turn
        else:
            # AI's turn
            start_time = time.time()
            if algo == "Alpha-Beta":
                best_move = game_logic.find_best_move_alpha_beta(game_tree.current_node)
            else:
                best_move = game_logic.find_best_move_minimax(game_tree.current_node)
           
            if game_tree.current_node.number % 2 == 0 and game_tree.current_node.number % 3 == 0:
                divisor = best_move.divisor
            else:
                divisor = 2 if game_tree.current_node.number % 2 == 0 else 3
            game_tree.make_move(divisor)
            ai_score += -1 if game_tree.current_node.number % 2 != 0 else 1
            if game_tree.current_node.number % 5 == 0 or game_tree.current_node.number % 10 == 0:
                game_tree.current_node.bank += 1
            end_time = time.time()
            evaluation_time = end_time - start_time
            current_player = player1  # Switch to human player after AI's turn
            time.sleep(1)

            
        # Check if the game is over
        if game_tree.current_node.number in [2, 3]:
            if player_score > ai_score:
                display_winner("Human", game_logic.nodes_visited)
                break
                
            elif ai_score > player_score:
                display_winner("AI", game_logic.nodes_visited)
                break
            else:
                display_winner("Draw", game_logic.nodes_visited) 
                break

        # Draw buttons
        pygame.draw.rect(SCREEN, GREEN, (250, 400, 200, 100))
        pygame.draw.rect(SCREEN, RED, (450, 400, 200, 100))
        
        draw_text("Divide by 2", font, BLACK, SCREEN, 280, 435)
        draw_text("Divide by 3", font, BLACK, SCREEN, 480, 435)

        # Draw game state
        draw_text(f"Number: {game_tree.current_node.number}", font, BLACK, SCREEN, 50, 50)
        draw_text(f"AI Score: {ai_score}", font, BLACK, SCREEN, 50, 100)
        draw_text(f"Player Score: {player_score}", font, BLACK, SCREEN, 50, 150)
        draw_text(f"Bank: {game_tree.current_node.bank}", font, BLACK, SCREEN, 50, 200)
        draw_text(f"Algorithm: {algo}", font, BLACK, SCREEN, 500, 50)
        draw_text(f"Player's Turn: {'Human' if current_player == player1 else 'AI'}", font, BLACK, SCREEN, 500, 100)
        draw_text(f"Evaluation Time: {evaluation_time:.7f} seconds", font, BLACK, SCREEN, 500, 150)
        
    pygame.display.flip()
pygame.quit()


import random
import pygame
import words
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (142, 255, 139)
yellow = (255, 255, 139)
grey = (128, 128, 128)
bgpink = (255, 213, 219)
boxpink = (255, 138, 221)
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Wordle!')
turn = 0
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('times new roman.ttf', 56)
small_font = pygame.font.Font('times new roman.ttf', 28)
secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
game_over = False
letters = 0
turn_active = True

def draw_board():
    global turn
    global board
    for col in range (0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, boxpink, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
            piece_text = huge_font.render(board[row][col], True, black)
            screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
    pygame.draw.rect(screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)



def check_words():
    global turn
    global board
    global secret_word
    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)


running = True
while running:
    timer.tick(fps)
    screen.fill(bgpink)
    check_words()
    draw_board()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            board[turn][letters] = entry
            letters += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters] = ' '
                letters -= 1
            if event.key == pygame.K_SPACE and not game_over:
                turn += 1
                letters = 0
            if event.key == pygame.K_SPACE and game_over:
                turn = 0
                letters = 0
                game_over = False
                secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]



    for row in range (0, 6):
        guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
        if guess == secret_word and row < turn:
            game_over = True


    if letters == 5:
        turn_active = False
    if letters < 5:
        turn_active = True

    if turn == 6:
        game_over = True
        loser_text = small_font.render('You lost, to try again press space!', True, black)
        screen.blit(loser_text, (15, 610))

    if game_over and turn < 6:
        winner_text = huge_font.render('YOU WON!', True, black)
        screen.blit(winner_text, (150, 610))

    pygame.display.flip()
pygame.quit()

import pygame
from network import Network
import pickle

pygame.font.init()

width = 1200
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blackjack Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 75

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 36)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1, y1 = pos
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        return False


def redraw_window(win, game, player_id):
    win.fill((0, 0, 0))

    if not game:
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        if game['phase'] == 'betting':
            text = font.render("Place your bet", 1, (0, 255, 255))
            win.blit(text, (width/2 - text.get_width()/2, 50))
            btns[0].draw(win)  # BET button
        elif game['phase'] == 'playing':
            player = game['players'][player_id]
            dealer = game['dealer']

            text = font.render("Your Hand", 1, (0, 255, 255))
            win.blit(text, (50, 50))
            show_hand(win, player['hand'], 50, 100)

            text = font.render("Dealer's Hand", 1, (0, 255, 255))
            win.blit(text, (width - 300, 50))
            show_hand(win, dealer['hand'], width - 300, 100)

            btns[1].draw(win)  # HIT button
            btns[2].draw(win)  # STAND button

        elif game['phase'] == 'result':
            result_text = "Tie Game!"
            if player['win'] == 1:
                result_text = "You Won!"
            elif player['win'] == 0:
                result_text = "You Lost..."
            text = font.render(result_text, 1, (255, 0, 0))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        
        pygame.display.update()


def show_hand(win, hand, x, y):
    font = pygame.font.SysFont("comicsans", 30)
    for card in hand:
        text = font.render(f"{card['value']} of {card['suit']}", 1, (255, 255, 255))
        win.blit(text, (x, y))
        y += 40


btns = [
    Button("BET", 525, 500, (255, 0, 0)),
    Button("HIT", 440, 500, (255, 0, 0)),
    Button("STAND", 610, 500, (0, 255, 0))
]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player_id = int(n.get_p())
    print("You are player", player_id)

    while run:
        clock.tick(60)
        try:
            game = pickle.loads(n.send("get"))
        except Exception as e:
            run = False
            print("Couldn't get game:", e)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game['phase'] == 'betting' and btns[0].click(pos):
                    n.send(pickle.dumps("bet"))
                elif game['phase'] == 'playing':
                    if btns[1].click(pos):
                        n.send(pickle.dumps("hit"))
                    elif btns[2].click(pos):
                        n.send(pickle.dumps("stand"))

        redraw_window(win, game, player_id)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
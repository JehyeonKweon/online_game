# import queue
# from player import Player

# class Game:
#     def __init__(self, game_id, dealer):
#         self.game_id = game_id
#         self.dealer = dealer
#         self.players = {}
#         self.turn = queue.Queue()

#     def add_player(self, id):
#         if len(self.players) < 3:
#             self.players[id] = Player()


#     def player_betting(self, id, betting):
#         if betting == 'bet':
#             self.players[id].bet = True
            

#     def create_round(self):
#         for id, player in self.players:
#             if player.get_bet:
#                 self.turn.put((id, player))

#         self.turn.put(self.dealer)
#         self.turn.put(None)


#     def deal_cards(self):
#         for _ in range(2):
#             self.create_round()
#             while True:
#                 receiver = self.turn.get()
#                 if receiver != None:
#                     card = self.dealer.get_card()
#                     receiver.hand.append(card)
                
#                 elif receiver == None:
#                     break


#     def player_turn(self, id, decision):

#         if decision == 'hit':
#             card = self.dealer.get_card()
#             self.players[id].hand.append(card)
#             self.players[id].update_score()
#             return True
#         else:
#             return False

        


#     def pay_out(self):
#         if self.dealer.get_score() <= 21:
#             # if dealer is not busted, compare scores to the players
#             dealer_score = 21 - self.dealer.get_score()
#             for id, player in self.players:
#                 if player.get_score() <= 21:
#                     # player not busted
#                     player_score = 21 - player.get_score()
#                     if dealer_score < player_score:
#                         player.win = 0
#                     elif dealer_score > player_score:
#                         player.win = 1
#                 else:
#                     # player busted
#                     player.win = 0

#         else:
#             # dealer busted
#             for id, player in self.players:
#                 if player.get_score() <= 21:
#                     # if players are not busted win
#                     player.win = 1

import queue
from player import Player

class Game:
    def __init__(self, game_id, dealer):
        self.game_id = game_id
        self.dealer = dealer
        self.players = {}
        self.turn = queue.Queue()
        self.phase = 'betting'

    def add_player(self, id):
        if len(self.players) < 3:
            self.players[id] = Player()

    def player_betting(self, id, betting):
        if betting == 'bet':
            self.players[id].place_bet()

    def create_round(self):
        for id, player in self.players.items():
            if player.get_bet():
                self.turn.put(id)

        self.turn.put('dealer')
        self.turn.put(None)

    def deal_cards(self):
        for _ in range(2):
            self.create_round()
            while True:
                receiver = self.turn.get()
                if receiver is not None:
                    if receiver == 'dealer':
                        card = self.dealer.get_card()
                        self.dealer.hand.append(card)
                        self.dealer.update_score()
                    else:
                        card = self.dealer.get_card()
                        self.players[receiver].hand.append(card)
                        self.players[receiver].update_score()
                else:
                    break

    def player_turn(self, id, decision):
        if decision == 'hit':
            card = self.dealer.get_card()
            self.players[id].hand.append(card)
            self.players[id].update_score()
            return True
        else:
            return False

    def pay_out(self):
        if self.dealer.get_score() <= 21:
            dealer_score = 21 - self.dealer.get_score()
            for id, player in self.players.items():
                if player.get_score() <= 21:
                    player_score = 21 - player.get_score()
                    if dealer_score < player_score:
                        player.win = 1
                    elif dealer_score > player_score:
                        player.win = 0
                else:
                    player.win = 0
        else:
            for id, player in self.players.items():
                if player.get_score() <= 21:
                    player.win = 1

    def reset_game(self):
        self.dealer.hand = []
        self.dealer.score = 0
        self.phase = 'betting'
        for player in self.players.values():
            player.reset()

    def game_state(self):
        return {
            'players': {id: {
                'hand': player.hand,
                'score': player.get_score(),
                'win': player.get_win(),
                'bet': player.get_bet()
            } for id, player in self.players.items()},
            'dealer': {
                'hand': self.dealer.hand,
                'score': self.dealer.get_score()
            },
            'turn': self.turn.queue,
            'phase': self.phase
        }

    def reset_turns(self):
        self.turn = queue.Queue()
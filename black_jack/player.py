# class Player:

#     def __init__(self):
#         self.hand = []
#         self.score = 0
#         self.win = -1
#         self.bet = False


#     def get_score(self):
#         return self.score
    

#     def get_win(self):
#         return self.win
    

#     def get_bet(self):
#         return self.bet


#     def update_score(self):
#         self.score = 0
#         for card in self.hand:
#             if card['cards'][0]['value'] == 'KING' or card['cards'][0]['value'] == 'QUEEN' or card['cards'][0]['value'] == 'JACK':
#                 self.score += 10
#             elif card['cards'][0]['value'] == 'ACE':
#                 if self.score + 11 <= 21:
#                     self.score += 11
#                 else:
#                     self.score += 1
#             else:
#                 self.score += int(card['cards'][0]['value'])

class Player:
    def __init__(self):
        self.hand = []
        self.score = 0
        self.win = -1  # -1 means undecided, 0 means loss, 1 means win
        self.bet = False

    def get_score(self):
        return self.score

    def get_win(self):
        return self.win

    def get_bet(self):
        return self.bet

    def update_score(self):
        self.score = 0
        aces = 0
        for card in self.hand:
            value = card['value']
            if value in ['KING', 'QUEEN', 'JACK']:
                self.score += 10
            elif value == 'ACE':
                aces += 1
                self.score += 11
            else:
                self.score += int(value)
        
        while self.score > 21 and aces:
            self.score -= 10
            aces -= 1

    def place_bet(self):
        self.bet = True

    def reset(self):
        self.hand = []
        self.score = 0
        self.win = -1
        self.bet = False
# import requests

# class Dealer:
#     def __init__(self):
#         self.hand = []
#         self.score = 0
#         self.deck_id = ''
#         self.remaining = 0
#         self.get_deck()

#     def get_score(self):
#         return self.score


#     def get_deck(self):
#         request = requests.get('https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6')
#         if request.status_code == 200:
#             data = request.json()
#             self.deck_id = data['deck_id']
#             self.remaining = data['remaining']


#     def get_card(self):
#         request = requests.get(f'https://www.deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1')
#         if request.status_code == 200:
#             data = request.json()
#             self.check_remaining()
#             return data
        
    
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


#     def hit(self):
#         card = self.get_card()
#         self.hand.append(card)

    
#     def play(self):
#         if self.score <= 16:
#             self.hit()
#             self.update_score()

    
#     def check_remaining(self):
#         if self.remaining == 0:
#             self.get_deck()


import requests

class Dealer:
    def __init__(self):
        self.hand = []
        self.score = 0
        self.deck_id = ''
        self.remaining = 0
        self.get_deck()

    def get_score(self):
        return self.score

    def get_deck(self):
        request = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6')
        if request.status_code == 200:
            data = request.json()
            self.deck_id = data['deck_id']
            self.remaining = data['remaining']

    def get_card(self):
        request = requests.get(f'https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1')
        if request.status_code == 200:
            data = request.json()
            self.remaining -= 1
            self.check_remaining()
            return data['cards'][0]

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

    def hit(self):
        card = self.get_card()
        self.hand.append(card)
        self.update_score()

    def play(self):
        while self.score <= 16:
            self.hit()

    def check_remaining(self):
        if self.remaining == 0:
            self.get_deck()
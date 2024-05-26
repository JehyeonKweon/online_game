# import socket
# from _thread import *
# import pickle
# from game import Game
# from dealer import Dealer

# server = "10.200.118.108"
# port = 5555

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)

# s.listen(2)
# print("Waiting Connection")

# def threaded_client(conn, game, player_id):
#     conn.send(str.encode(str(player_id)))
#     while True:
#         ready = pickle.loads(conn.recv(4096))
#         if not ready:
#             break
#         else:
#             if ready == 'ready':
#                 while True:
#                     betting = pickle.loads(conn.recv(4096))
#                     if not betting:
#                         break
#                     else:
#                         game.player_betting(player_id, betting)
#                         game.deal_cards()
#                         conn.sendall(pickle.dumps(game))
#                         game.create_round()

#                         while True:
#                             turn = game.turn.get()
#                             if turn != None or turn == game.dealer:
#                                 if turn[0] == player_id:
#                                     keep_going = True
#                                     while keep_going:
#                                         if turn[1].get_score() <= 21:
#                                             hit = pickle.loads(conn.recv(4096))
#                                             if not hit:
#                                                 break
#                                             else:
#                                                 keep_going = game.player_turn(player_id, hit)
#                                                 conn.sendall(pickle.dumps(game))

#                             elif turn == game.dealer:
#                                 # revel one hidden card
#                                 game.dealer.play()
#                                 conn.sendall(pickle.dumps(game))

#                             elif turn == None:
#                                 game.pay_out()
#                                 conn.sendall(pickle.dumps(game))
#                                 break
            


#     conn.close()

# games = []
# player_id = 0
# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)
    
#     game_id = player_id // 3
#     if game_id < len(games):
#         games[game_id].add_player(player_id % 3)
#     else:
#         games.append(Game(game_id, Dealer()))
#         games[game_id].add_player(player_id % 3)

#     start_new_thread(threaded_client, (conn, games[game_id], player_id % 3))
#     player_id += 1

import socket
from _thread import start_new_thread
import pickle
from game import Game
from dealer import Dealer

server = "10.200.118.108"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(3)  # Allows up to 3 players to connect
print("Waiting Connection")

def threaded_client(conn, game, player_id):
    conn.send(str(player_id).encode())
    
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            
            if not data:
                break
            
            if data == 'ready':
                game.reset_turns()
                conn.sendall(pickle.dumps(game.game_state()))

                while game.phase == 'betting':
                    bet_data = pickle.loads(conn.recv(4096))
                    if 'bet' in bet_data:
                        game.player_betting(player_id, bet_data['bet'])
                        conn.sendall(pickle.dumps(game.game_state()))

                while game.phase == 'playing':
                    if game.turn.queue[0] == player_id and game.players[player_id]['status'] == 'playing':
                        player_action = pickle.loads(conn.recv(4096))
                        if 'action' in player_action:
                            if player_action['action'] == 'hit':
                                game.hit(player_id)
                            elif player_action['action'] == 'stand':
                                game.stand(player_id)
                            conn.sendall(pickle.dumps(game.game_state()))
                    
                    if game.turn.queue[0] == player_id:
                        break

                while game.phase == 'dealer':
                    game.dealer_play()
                    conn.sendall(pickle.dumps(game.game_state()))
                    break
                
                while game.phase == 'result':
                    game.determine_winner()
                    conn.sendall(pickle.dumps(game.game_state()))
                    game.reset_game()
                    break
        except:
            break

    conn.close()

games = []
player_id = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    game_id = player_id // 3
    if game_id < len(games):
        games[game_id].add_player(player_id % 3)
    else:
        games.append(Game(game_id, Dealer()))
        games[game_id].add_player(player_id % 3)

    start_new_thread(threaded_client, (conn, games[game_id], player_id % 3))
    player_id += 1
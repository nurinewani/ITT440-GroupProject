import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
players = []
choices = [None, None]
rounds = 4
current_round = 0
scores = [0, 0]
player_turn = 0

def handle_client(conn, addr):
    global player_turn, current_round

    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        
        if not msg:
            continue
        
        if msg.startswith("NAME:"):
            player_name = msg.split(":")[1]
            players.append(player_name)
            if len(players) == 2:
                broadcast(f"Game is starting!\nPlayer 1: {players[0]}, Player 2: {players[1]}")
                send_turn_message()
        else:
            if players[player_turn] in msg:
                choices[player_turn] = msg.split(":")[1]
                player_turn = (player_turn + 1) % 2
                if None not in choices:
                    determine_winner()
                    current_round += 1
                    if current_round == rounds:
                        broadcast(f"\nFinal scores:\n{players[0]}: {scores[0]}, {players[1]}: {scores[1]}")
                        broadcast(determine_final_winner())
                        connected = False
                    else:
                        broadcast(f"\nScores:\n{players[0]}: {scores[0]}, {players[1]}: {scores[1]}")
                        choices[0] = choices[1] = None
                        send_turn_message()
                else:
                    send_turn_message()
    
    conn.close()

def send_turn_message():
    turn_message = f"\nTurn: {players[player_turn]}"
    broadcast(turn_message)

def determine_winner():
    global scores
    if choices[0] == choices[1]:
        broadcast("It's a tie!")
    elif (choices[0] == "batu" and choices[1] == "burung") or (choices[0] == "burung" and choices[1] == "air") or (choices[0] == "air" and choices[1] == "batu"):
        broadcast(f"\n{players[0]} wins the round!")
        scores[0] += 1
    else:
        broadcast(f"\n{players[1]} wins the round!")
        scores[1] += 1

def determine_final_winner():
    if scores[0] > scores[1]:
        return f"\n{players[0]} wins the game!"
    elif scores[1] > scores[0]:
        return f"\n{players[1]} wins the game!"
    else:
        return "\nThe game is a tie!"

def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
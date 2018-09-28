# solutions.py
"""Web Technologies."""

import re
import json
import socket
import requests
import collections
import numpy as np
from scipy.spatial import KDTree
from matplotlib import pyplot as plt

def json_example(filename="nyc_traffic.json"):
    """Load the data from the specified JSON file. Look at the first few
    entries of the dataset and decide how to gather information about the
    cause(s) of each accident. Make a readable, sorted bar chart showing the
    total number of times that each of the 7 most common reasons for accidents
    are listed in the data set.
    """
    causes = []
    with open(filename,'r') as f:
        info = json.load(f)
    for i in range(len(info)):
        if 'contributing_factor_vehicle_1' in info[i].keys():
            causes.append(str(info[i]['contributing_factor_vehicle_1']))
        if 'contributing_factor_vehicle_2' in info[i].keys():
            causes.append(str(info[i]['contributing_factor_vehicle_2']))
        if 'contributing_factor_vehicle_3' in info[i].keys():
            causes.append(str(info[i]['contributing_factor_vehicle_3']))
        if 'contributing_factor_vehicle_4' in info[i].keys():
            causes.append(str(info[i]['contributing_factor_vehicle_4']))

    # print(causes)
    c = collections.Counter(causes).most_common(7)
    print(c)
    d = dict(c)
    reasons = d.keys()
    values = d.values()
    y_pos = np.arange(7)
    plt.bar(y_pos,values,align='center',alpha=0.5)
    plt.xticks(y_pos, reasons, fontsize=6, rotation=15)
    plt.show()


class TicTacToe:
    def __init__(self):
        """Initialize an empty board. The O's go first."""
        self.board = [[' ']*3 for _ in range(3)]
        self.turn, self.winner = "O", None

    def move(self, i, j):
        """Mark an O or X in the (i,j)th box and check for a winner."""
        if self.winner is not None:
            raise ValueError("the game is over!")
        elif self.board[i][j] != ' ':
            raise ValueError("space ({},{}) already taken".format(i,j))
        self.board[i][j] = self.turn

        # Determine if the game is over.
        b = self.board
        if any(sum(s == self.turn for s in r)==3 for r in b):
            self.winner = self.turn     # 3 in a row.
        elif any(sum(r[i] == self.turn for r in b)==3 for i in range(3)):
            self.winner = self.turn     # 3 in a column.
        elif b[0][0] == b[1][1] == b[2][2] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        elif b[0][2] == b[1][1] == b[2][0] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def empty_spaces(self):
        """Return the list of coordinates for the empty boxes."""
        return [(i,j) for i in range(3) for j in range(3)
                                        if self.board[i][j] == ' ' ]
    def __str__(self):
        return "\n---------\n".join(" | ".join(r) for r in self.board)


class TicTacToeEncoder(json.JSONEncoder):
    """A custom JSON Encoder for TicTacToe objects."""
    def default(self, obj):
        if not isinstance(obj, TicTacToe):
            raise TypeError("expected a TicTacToe object for encoding")
        return {"dtype": "TicTacToe", "board": obj.board, "turn": obj.turn, "winner": obj.winner}


def tic_tac_toe_decoder(obj):
    """A custom JSON decoder for TicTacToe objects."""
    if "dtype" in obj:
        if obj["dtype"] != "TicTacToe" or "board" not in obj or "turn" not in obj or "winner" not in obj:
            raise ValueError("expected a JSON message from TicTacToeEncoder")
        newTTT = TicTacToe()
        newTTT.board = obj["board"]
        newTTT.turn = obj["turn"]
        newTTT.winner = obj["winner"]
        return newTTT
    raise ValueError("expected a JSON message from TicTacToeEncoder")


def mirror_server(server_address=("0.0.0.0", 33333)):
    """A server for reflecting strings back to clients in reverse order."""
    print("Starting mirror server on {}".format(server_address))

    # Specify the socket type, which determines how clients will connect.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)    # Assign this socket to an address.
    server_sock.listen(1)               # Start listening for clients.

    while True:
        # Wait for a client to connect to the server.
        print("\nWaiting for a connection...")
        connection, client_address = server_sock.accept()

        try:
            # Receive data from the client.
            print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()    # Receive data.
            print("Received '{}' from client".format(in_data))

            # Process the received data and send something back to the client.
            out_data = in_data[::-1]
            print("Sending '{}' back to the client".format(out_data))
            connection.sendall(out_data.encode())       # Send data.

        # Make sure the connection is closed securely.
        finally:
            connection.close()
            print("Closing connection from {}".format(client_address))

def mirror_client(server_address=("0.0.0.0", 33333)):
    """A client program for mirror_server()."""
    print("Attempting to connect to server at {}...".format(server_address))

    # Set up the socket to be the same type as the server.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server.
    print("Connected!")

    # Send some data from the client user to the server.
    out_data = input("Type a message to send: ")
    client_sock.sendall(out_data.encode())              # Send data.

    # Wait to receive a response back from the server.
    in_data = client_sock.recv(1024).decode()           # Receive data.
    print("Received '{}' from the server".format(in_data))

    # Close the client socket.
    client_sock.close()

# Address created to match source
address = 44471

def tic_tac_toe_server(server_address=("0.0.0.0", address)):
    """A server for playing tic-tac-toe with random moves."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)                    # Assign this socket to an address.
    server_sock.listen(1)                               # Start listening for clients.
    out_data = ""
    print("\nWaiting for a connection...")
    connection, client_address = server_sock.accept()
    while (out_data != "WIN" and out_data != "DRAW" and out_data != "LOSE"):
        try:
            print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()    # Receive data.
            # print("Received '{}' from client".format(in_data))

            TTT = json.loads(in_data, object_hook=tic_tac_toe_decoder)
            options = TTT.empty_spaces()
            if TTT.winner is not None:
                out_data = "WIN"
            elif len(options) == 0:
                out_data = "DRAW"
            else:
                rand = np.random.randint(len(options))
                TTT.move(options[rand][0],options[rand][1])
                if TTT.winner == "X":
                    out_data = "LOSE"
                    out_data2 = json.dumps(TTT, cls=TicTacToeEncoder)
                else:
                    out_data = json.dumps(TTT, cls=TicTacToeEncoder)

            # print("Sending '{}' back to the client".format(out_data))
            connection.sendall(out_data.encode())       # Send data.
            if TTT.winner == "X":
                # print("Sending '{}' back to the client".format(out_data2))
                connection.sendall(out_data2.encode())

        finally:
            pass
            # if out_data == "WIN" or out_data == "DRAW" or out_data == "LOSE":
    connection.close()

def tic_tac_toe_client(server_address=("0.0.0.0", address)):
    """A client program for tic_tac_toe_server()."""
    print("Attempting to connect to server at {}...".format(server_address))

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server.


    TTT = TicTacToe()
    pattern = re.compile(r"^[0-2] [0-2]$")
    while TTT.winner is None:
        print(TTT)
        if len(TTT.empty_spaces()) == 0:
            break
        valid = False
        while not valid:
            ij = input("Make a move (enter row and column, 2 numbers seperated by a space): ")
            if bool(pattern.search(ij)):
                try:
                    TTT.move(int(ij[0]),int(ij[2]))
                    valid = True
                except ValueError as e:
                    print(e)
            else:
                print("Invalid input")

        out_data = json.dumps(TTT, cls=TicTacToeEncoder)
        print("Sending '{}' back to the server".format(out_data))
        client_sock.sendall(out_data.encode())              # Send data.

        in_data = client_sock.recv(1024).decode()           # Receive data.
        print("Received '{}' from the server".format(in_data))

        if in_data == "WIN":
            print("Congrats, you won!")
            print(TTT)
        elif in_data == "LOSE":
            print("Sorry, you lose.")
            in_data2 = client_sock.recv(1024).decode()
            TTT = json.loads(in_data2, object_hook=tic_tac_toe_decoder)
            print(TTT)
        elif in_data == "DRAW":
            print("Tie.")
        else:#TTT
            TTT = json.loads(in_data, object_hook=tic_tac_toe_decoder)

    #WHAT TO DO WHEN GAME IS OVER
    client_sock.close()



def download_nyc_data():
    """Make requests to download data from the following API endpoints.

    Recycling bin locations: https://data.cityofnewyork.us/api/views/sxx4-xhzg/rows.json?accessType=DOWNLOAD

    Residential addresses: https://data.cityofnewyork.us/api/views/7823-25a9/rows.json?accessType=DOWNLOAD

    Save the recycling bin data as nyc_recycling.json and the residential
    address data as nyc_addresses.json.
    """
    filename_recycle = "nyc_recycling.json"
    filename_address = "nyc_addresses.json"
    # recycle = requests.get("https://data.cityofnewyork.us/api/views/sxx4-xhzg/rows.json?accessType=DOWNLOAD").json()
    # with open(filename_recycle, "w") as f:
    #     json.dump(recycle, f)
    addresses = requests.get("https://data.cityofnewyork.us/api/views/7823-25a9/rows.json?accessType=DOWNLOAD").json()
    with open(filename_address, "w") as f2:
        json.dump(addresses, f2)


def kd_tree_json(recycling="nyc_recycling.json", addresses="nyc_addresses.json"):
    """Load the specifiec data files. Use a k-d tree to determine the distances
    from each address to the nearest recycling bin, and plot a histogram of
    the results.

    DO NOT call download_nyc_data() in this function.
    """
    with open(recycling,'r') as f:
        recycle = json.load(f)
    with open(addresses,'r') as f2:
        address = json.load(f2)
    distances = []
    lat_lon = []
    recycleData = recycle['data']
    addressData = address['data']

    for r_bin in recycleData:
        if r_bin[-2] is not None:
            lat_lon.append(np.array([float(r_bin[-2]), float(r_bin[-1])]))

    pattern = re.compile(r"-?[0-9]{2}\.[0-9]+")
    tree = KDTree(lat_lon)

    for address in addressData:
        findPattern = pattern.findall(address[8])
        new_lat_lon = np.array([float(findPattern[1]), float(findPattern[0])])
        min_distance, index = tree.query(np.array([new_lat_lon]))
        distances.append(min_distance)

    plt.hist(distances, bins=10)
    plt.show()

def test2():
    TTT = TicTacToe()
    TTT.move(0,0)
    TTT.move(1,1)
    TTT.move(2,0)
    TTT.move(0,2)
    TTT.move(1,0)
    out_data = json.dumps(TTT, cls=TicTacToeEncoder)
    newTTT = json.loads(out_data, object_hook=tic_tac_toe_decoder)
    print(newTTT)

if __name__ == '__main__':
    print(json_example())
    print(test2())
    print(kd_tree_json())


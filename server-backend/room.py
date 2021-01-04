import random
from game import RoomGame

used_ids = set([''])
CHARS = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'

def make_room(width, height, mines):
    room_id = ''
    while room_id in used_ids:
        room_id = ''
        for i in range(3):
            room_id += random.choice(CHARS)

    return (room_id, ServerRoom(width, height, mines))

class ServerRoom:
    def __init__(self, width, height, mines):
        assert height * width - mines > 10
        
        self.width = width
        self.height = height
        self.mines = mines  

        self.finished = False


        self.board = [[False] * width for _ in range(height)]
        rem = mines
        while rem:
            x = random.randrange(height)
            y = random.randrange(width)
            if not self.board[x][y] and (abs(x - self.height//2) > 1 or abs(y - self.width//2) > 1):
                self.board[x][y] = True
                rem -= 1

        self.player_games = dict()

    def join_room(self, player):
        if player not in self.player_games:
            self.player_games[player] = RoomGame(self, player)
        return self.player_games[player]

    def rep(self):
        outL = [len(self.player_games)]
        rest = []
        for player in self.player_games:
            game = self.player_games[player]
            rest.append((player, game.rev_count, (2 if game.won else 0) if game.finished else 1, game.value()))
        rest.sort(key = lambda x: (x[1], x[2]), reverse = True)

        for a,b,c,d in rest:
            outL.append(a)
            outL.append(b)
            outL.append(c)
            outL.append(f"{d:0.3f}")

        print(outL)
        return ' '.join(map(str,outL))
        

        

    

import random
import time
from database import db_add
from perf_calc import pp

class Game:
    dX = [1,1,1,0,0,-1,-1,-1]
    dY = [1,-1,0,-1,1,1,-1,0]
    
    def adj(self, x, y):
        out = 0
        for d in range(8):
            xx = x + Game.dX[d]
            yy = y + Game.dY[d]
            if 0 <= xx < self.height and 0 <= yy < self.width and self.board[xx][yy]:
                out += 1
        return out

    def chord(self, x, y):
        want = self.rev[x][y]
        seen = 0
        for d in range(8):
            xx = x + Game.dX[d]
            yy = y + Game.dY[d]
            if 0 <= xx < self.height and 0 <= yy < self.width and self.flags[xx][yy]:
                seen += 1

        print('CHORD',x,y,want,seen)
        
        if want == seen:
            for d in range(8):
                xx = x + Game.dX[d]
                yy = y + Game.dY[d]
                if 0 <= xx < self.height and 0 <= yy < self.width and not self.flags[xx][yy]:
                    self.reveal(xx,yy)
                    
    def flag_chord(self, x, y):
        want = self.rev[x][y]
        seen = 0
        for d in range(8):
            xx = x + Game.dX[d]
            yy = y + Game.dY[d]
            if 0 <= xx < self.height and 0 <= yy < self.width:
                if self.rev[xx][yy] == -1:
                    seen += 1

        print('FLAG_CHORD',x,y,want,seen)
        
        if want == seen:
            for d in range(8):
                xx = x + Game.dX[d]
                yy = y + Game.dY[d]
                if 0 <= xx < self.height and 0 <= yy < self.width and not self.flags[xx][yy]:
                    self.flag(xx,yy)
                    
    def click(self, x, y):
        if self.finished:
            return []
        
        if self.flags[x][y]:
            return []
        elif self.rev[x][y] == -1:
            self.reveal(x,y)
        else:
            self.chord(x,y)

    def reveal(self, x, y, depth = 0):
        assert 0 <= x < self.height
        assert 0 <= y < self.width

        MAX_DEPTH = 200
        if depth > MAX_DEPTH:
            return []

        if self.flags[x][y]:
            return []

        if self.finished:
            return []

        if self.rev[x][y] != -1: return []

        if self.board[x][y]:
            self.finished = True
            self.won = False
            self.end_time = time.time()

            self.finish()

            return []

        
        calc = self.adj(x, y)
        out = [(x,y,calc)]
        self.rev[x][y] = calc

        if calc == 0:
            for d in range(8):
                xx = x + Game.dX[d]
                yy = y + Game.dY[d]
                if 0 <= xx < self.height and 0 <= yy < self.width:
                    out += self.reveal(xx,yy,depth + 1)

        self.rev_count += 1
        if self.rev_count + self.mines == self.width * self.height:
            self.finished = True
            self.won = True
            self.end_time = time.time()

            self.finish()
            

        return out

    def flag(self, x, y):
        if self.finished:
            return
        
        if self.rev[x][y] == -1:
            if self.flags[x][y]:
                self.f_count -= 1
            self.flags[x][y] ^= True
            if self.flags[x][y]:
                self.f_count += 1
        else:
            self.flag_chord(x,y)

    def rep(self):
        w = self.width
        h = self.height
        m = self.mines - self.f_count
        score = self.rev_count
        
        state = 1 if not self.finished else (2 if self.won else 0)
        if w == 0: state = 3
        
        if self.room == None:
            players = '0'
        else:
            players = self.room.rep()

        repr_board = [list(map(str,line)) for line in self.rev]
        for x in range(self.height):
            for y in range(self.width):
                if self.flags[x][y]:
                    repr_board[x][y] = 'F'
                
        if self.finished:
            for x in range(self.height):
                for y in range(self.width):
                    if self.board[x][y]:
                        if repr_board[x][y] == 'F':
                            repr_board[x][y] = 'F'
                        else:
                            repr_board[x][y] = 'M'
                    else:
                        if repr_board[x][y] == 'F':
                            repr_board[x][y] = 'G'
                        
            
                      
        board = ' '.join(' '.join(line) for line in repr_board)

        print(w, h, m, score, state, players, board)

        game_string = f'{w} {h} {m} {score} {state} {players} {board}'
        return game_string

    def value(self):
        return pp(self.mines, self.width, self.height, self.rev_count)

class ServerGame(Game):  
    def __init__(self, height, width, mines, player):
        assert 3 * mines < 2 * height * width
        assert height * width - mines > 10
        
        self.width = width
        self.height = height
        self.mines = mines
        self.player = player    

        self.finished = False


        self.board = [[False] * width for _ in range(height)]
        self.flags = [[False] * width for _ in range(height)]
        self.f_count = 0
        
        rem = mines
        while rem:
            x = random.randrange(height)
            y = random.randrange(width)
            if not self.board[x][y]:
                self.board[x][y] = True
                rem -= 1

        self.rev = [[-1] * width for _ in range(height)]
        self.rev_count = 0

        self.room = None
        
        self.start_time = time.time()

    def finish(self):
        assert self.finished
        
        db_add(self)

class RoomGame(Game):
    def __init__(self, room, player):
        self.width = room.width
        self.height = room.height
        self.mines = room.mines
        self.player = player

        self.finished = False

        self.board = [row[:] for row in room.board]
        self.flags = [[False] * self.width for _ in range(self.height)]
        self.f_count = 0

        self.rev = [[-1] * self.width for _ in range(self.height)]
        self.rev_count = 0

        self.room = room
        
        self.start_time = time.time()

    def finish(self):
        assert self.finished
        
        if self.room.verify():
            db_add(self)
            

class Empty(Game):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mines = 0

        self.finished = True
        self.won = False

        self.board = []
        self.flags = []
        self.f_count = 0

        self.rev = []
        self.rev_count = 0

        self.room = None

import sqlite3 as sl
from time import sleep
from perf_calc import perf_calc, pp

games = []
database = 'minesweeper.db'

def db_add(game):
    games.append(game)

def db_store():
    global games

    while True:
        sleep(10)
        print('Storing Data')

        data = []
        user_upd = set()
        count = 0
        while games:
            game = games.pop()
            assert game.finished

            user_upd.add(game.player)

            score = pp(game.mines, game.width, game.height, game.rev_count)
            
            data.append((game.player, game.width, game.height, game.mines, score, game.rev_count, game.end_time - game.start_time))
            count += 1

        sql = 'INSERT INTO GAMES (name, width, height, mines, score, remain, time) values (?, ?, ?, ?, ?, ?, ?)'
        con = sl.connect(database)
        with con:
            con.executemany(sql, data)

        for user in user_upd:
            perf_calc(user)

        con.commit()
        con.close()
        print('Count =',count)
        print('Done Storing')

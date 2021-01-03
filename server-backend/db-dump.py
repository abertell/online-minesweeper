<<<<<<< HEAD
import sqlite3 as sl

database = 'minesweeper.db'
con = sl.connect(database)

for table in ('GAMES','PERFORMANCE_TOP','PERFORMANCE_TOP_10','PERFORMANCE_PP','PERFORMANCE_ALL','USER'):
    print(table)
    with con:
        data = con.execute(f"SELECT * FROM {table}")    
        for row in data:
            print(row)
    print()
=======
import sqlite3 as sl

database = 'minesweeper.db'
con = sl.connect(database)

for table in ('GAMES','PERFORMANCE_TOP','PERFORMANCE_TOP_10','PERFORMANCE_PP','PERFORMANCE_ALL','USER'):
    print(table)
    with con:
        data = con.execute(f"SELECT * FROM {table}")    
        for row in data:
            print(row)
    print()
>>>>>>> 74e0fe7228c019e463541cc7da630021078b3d38

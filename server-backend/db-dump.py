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

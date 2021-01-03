import sqlite3 as sl
from math import log

def pp(m,w,h,x):
    a = w * h
    return ((4.22*log(106+a)-16.8)**(m/a)-1)*100*(0.5)**((a-m-8)/(x-8)-1)

database = 'minesweeper.db'

sizes = [(8,8),(9,9),(16,16),(16,30),(24,30)]

def perf_add(user):
    con = sl.connect(database)
    
    for table in ('PERFORMANCE_TOP', 'PERFORMANCE_TOP_10', 'PERFORMANCE_PP', 'PERFORMANCE_ALL'):
        request = f"INSERT INTO {table} (name) VALUES ('{user}')"
        con.execute(request)

    con.commit()
    con.close()
        

def perf_calc(user):
    con = sl.connect(database)

    top = []
    top_10 = []
    pp = []
    
    for width, height in sizes:
        with con:
            request = f"SELECT score FROM GAMES WHERE NAME = ? AND (WIDTH = {width} AND HEIGHT = {height} OR WIDTH = {height} AND HEIGHT = {width})"
            data = list(map(lambda x: int(x[0]),con.execute(request,[user])))
            data.sort()

            top.append(data[-1] if data else 0)
            top_10.append(sum(data[-10:]))

            pp_val = 0
            for v in data:
                pp_val *= .9
                pp_val += v

            pp.append(pp_val)

    print(user,top,top_10,pp)

    size_names = [f'`{width}_BY_{height}`' for width,height in sizes] + ["TOTAL"]

    for table, values in (('PERFORMANCE_TOP',top), ('PERFORMANCE_TOP_10',top_10), ('PERFORMANCE_PP',pp)):
        v_ins = tuple(values + [sum(values)])

        t_string = ','.join(f"{name} = {val}" for name, val in zip(size_names, v_ins))
        
        request = f'''UPDATE {table}
                    SET
                    {t_string}
                    WHERE NAME = ?'''
        with con:
            con.execute(request,[user])

    with con:
        request = f"SELECT score FROM GAMES WHERE NAME = ? AND (WIDTH >= 8 AND HEIGHT >= 8)"
        data = list(map(lambda x: int(x[0]),con.execute(request,[user])))
        data.sort()

    pp_all = 0
    for v in data:
        pp_all *= .95
        pp_all += v

    request = 'UPDATE PERFORMANCE_ALL SET pp = ? WHERE name = ?'
    with con:
        con.execute(request, (pp_all, user))
            
    con.commit()
    con.close()

def pp_recalc():
    con = sl.connect(database)

    users = set()

    data = con.execute(f"SELECT * FROM GAMES")
    upd = []

    
    for row in GAMES:
        print(row)

    

    con.commit()
    con.close()
    

    
    

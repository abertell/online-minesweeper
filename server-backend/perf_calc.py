import sqlite3 as sl
from math import log

def pp(m,w,h,x):
    if 2 * m > w * h:
        return 0.0

    a,b,c=5.132659273699201,59.96477197931381,-20.352104580796095
    norm=90
    line=lambda x:a*log(x+b)+c
    exp=lambda a:log(2,line(a))
    speed=lambda a:2*log(1+(log(log(log(a)))-log(log(log(256)))))
    ramp=lambda m,a:exp(a)*((m/a)/exp(a))**(1+speed(a))
    base=lambda m,a:line(a)**ramp(m,a)-1
    ecc=lambda w,h:max(w/h,h/w)**.05
    cutoff=lambda m,a,x:(1-.1/(1+log(a/64)))**(x<a-m)
    balance=lambda r:max(1-100*(1-r)**2,r*r)
    dropoff=lambda m,a,x:.35**(log(a)*(1/balance((x-8)/(a-m-8))-1))
    large=lambda a:(100-(log(1+log(max(a,1000))/log(1000),2)-1)*75)/100
    
    return norm*base(m,w*h)*ecc(w,h)*cutoff(m,w*h,x)*dropoff(m,w*h,x)*large(w*h)

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
            request = f"SELECT score FROM GAMES WHERE NAME = ? AND ((WIDTH = {width} AND HEIGHT = {height}) OR (WIDTH = {height} AND HEIGHT = {width}))"
            data = list(map(lambda x: float(x[0]),con.execute(request,[user])))
            data.sort()

            top.append(data[-1] if data else 0)
            top_10.append(sum(data[-10:]))

            pp_val = 0
            for v in data:
                pp_val *= .9
                pp_val += v

            pp.append(pp_val)

    print(user,top,top_10,pp)

    size_names = [f'`{width}_BY_{height}`' for width,height in sizes] + ["pp"]

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
        request = f"SELECT score FROM GAMES WHERE NAME = ? AND ((WIDTH <= 1000 AND HEIGHT <= 1000) AND (WIDTH >= 8 AND HEIGHT >= 8))"
        data = list(map(lambda x: float(x[0]),con.execute(request,[user])))
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

    
    for row in data:
        print(row)
        pp_value = pp(row[4], row[2], row[3], row[6])
        assert(isinstance(pp_value, float))
        upd.append((pp_value, row[0]))
        users.add(row[1])

    request = 'UPDATE GAMES SET score = ? where id = ?'

    con.executemany(request, upd)

    con.commit()
    con.close()
    
    for user in users:
        perf_calc(user)

def r_float(num):
    if num == None:
        return "0.000"
    
    fl = float(num)
    return f"{fl:.3f}"
    
def get_data(user):
    con = sl.connect(database)
    
    pps = []
    scores = []

    for table in ('PERFORMANCE_TOP', 'PERFORMANCE_TOP_10', 'PERFORMANCE_PP', 'PERFORMANCE_ALL'):
        with con:
            request = f"SELECT pp FROM {table} WHERE NAME = ?"
            data = list(con.execute(request, [user]))

            pps.append(r_float(data[0][0] if len(data) > 0 else None))

    with con:
        request = "SELECT width, height, mines, score, remain FROM GAMES WHERE NAME = ? AND ((WIDTH <= 1000 AND HEIGHT <= 1000) AND (WIDTH >= 8 AND HEIGHT >= 8))"
        data = list(con.execute(request,[user]))
        data.sort(key = lambda x: -x[3])
    data_parse = [list(map(r_float, row)) for row in data]
    data_parse = data_parse[:20]

    print(pps, data_parse)
    
    return ' '.join(map(str,pps)) + ' ' + str(len(data_parse)) + ' ' + ' '.join(' '.join(map(str, line)) for line in data_parse)

def get_ppv2_leader():
    con = sl.connect(database)

    table = 'PERFORMANCE_ALL'
    request = f"SELECT name, pp FROM {table} ORDER BY pp DESC LIMIT 20"
    data = con.execute(request)

    data_parse = [name + ' ' + r_float(pp) for name, pp in data]

    return str(len(data_parse))+' '+' '.join(data_parse)

def get_top_plays():
    con = sl.connect(database)
    
    with con:
        request = "SELECT name, width, height, mines, score, remain FROM GAMES WHERE ((WIDTH <= 1000 AND HEIGHT <= 1000) AND (WIDTH >= 8 AND HEIGHT >= 8)) ORDER BY score DESC LIMIT 20"
        data = list(con.execute(request))
    data_parse = [[row[0], int(row[1]), int(row[2]), int(row[3]), r_float(row[4]), int(row[5])] for row in data]
    
    return str(len(data_parse)) + ' ' + ' '.join(' '.join(map(str, line)) for line in data_parse) 

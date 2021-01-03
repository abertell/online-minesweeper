<<<<<<< HEAD
import sqlite3 as sl
import hashlib
from perf_calc import perf_add

database = 'minesweeper.db'

def login(user,pwd):
    con = sl.connect(database)

    pwd_enc = pwd.encode()
    hash1 = hashlib.md5(pwd_enc).hexdigest().encode()
    hash2 = hashlib.md5(hash1)

    hash_s = hash2.hexdigest()

    data = list(con.execute(f"SELECT password from USER where name = '{user}'"))

    if len(data) == 0:
        print(f'NEW USER: {user}')

        con.execute(f"INSERT INTO USER (name, password) VALUES ('{user}','{hash_s}')")
        con.commit()
        con.close()
        
        perf_add(user)
        return user
    else:
        print(data[0][0], hash_s)
        if (data)[0][0] == hash_s:
            return user
        return None

                       
=======
import sqlite3 as sl
import hashlib
from perf_calc import perf_add

database = 'minesweeper.db'

def login(user,pwd):
    con = sl.connect(database)

    pwd_enc = pwd.encode()
    hash1 = hashlib.md5(pwd_enc).hexdigest().encode()
    hash2 = hashlib.md5(hash1)

    hash_s = hash2.hexdigest()

    data = list(con.execute(f"SELECT password from USER where name = '{user}'"))

    if len(data) == 0:
        print(f'NEW USER: {user}')

        con.execute(f"INSERT INTO USER (name, password) VALUES ('{user}','{hash_s}')")
        con.commit()
        con.close()
        
        perf_add(user)
        return user
    else:
        print(data[0][0], hash_s)
        if (data)[0][0] == hash_s:
            return user
        return None

                       
>>>>>>> 74e0fe7228c019e463541cc7da630021078b3d38

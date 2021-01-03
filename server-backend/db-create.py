import sqlite3 as sl

database = 'minesweeper.db'
con = sl.connect(database)

with con:
    con.execute("""
        CREATE TABLE USER (
            name TEXT NOT NULL PRIMARY KEY,
            password TEXT
        );
    """)
    
    con.execute("""
        CREATE TABLE GAMES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            width INTEGER,
            height INTEGER,
            mines INTEGER,
            score INTEGER,
            remain INTEGER,
            time REAL
        );
    """)


    con.execute("""
        CREATE TABLE PERFORMANCE_TOP (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` INTEGER,
            `9_BY_9` INTEGER,
            `16_BY_16` INTEGER,
            `16_BY_30` INTEGER,
            `24_BY_30` INTEGER,
            TOTAL INTEGER
        );
    """)

    con.execute("""
        CREATE TABLE PERFORMANCE_TOP_10 (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` INTEGER,
            `9_BY_9` INTEGER,
            `16_BY_16` INTEGER,
            `16_BY_30` INTEGER,
            `24_BY_30` INTEGER,
            TOTAL INTEGER
        );
    """)

    con.execute("""
        CREATE TABLE PERFORMANCE_PP (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` REAL,
            `9_BY_9` REAL,
            `16_BY_16` REAL,
            `16_BY_30` REAL,
            `24_BY_30` REAL,
            TOTAL REAL
        );
    """)
        

<<<<<<< HEAD
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
            width REAL,
            height REAL,
            mines REAL,
            score REAL,
            remain REAL,
            time REAL
        );
    """)


    con.execute("""
        CREATE TABLE PERFORMANCE_TOP (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` REAL,
            `9_BY_9` REAL,
            `16_BY_16` REAL,
            `16_BY_30` REAL,
            `24_BY_30` REAL,
            TOTAL REAL
        );
    """)

    con.execute("""
        CREATE TABLE PERFORMANCE_TOP_10 (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` REAL,
            `9_BY_9` REAL,
            `16_BY_16` REAL,
            `16_BY_30` REAL,
            `24_BY_30` REAL,
            TOTAL REAL
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

    con.execute("""
        CREATE TABLE PERFORMANCE_ALL (
            name TEXT NOT NULL PRIMARY KEY,
            pp REAL
        );
    """)
        
=======
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
            width REAL,
            height REAL,
            mines REAL,
            score REAL,
            remain REAL,
            time REAL
        );
    """)


    con.execute("""
        CREATE TABLE PERFORMANCE_TOP (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` REAL,
            `9_BY_9` REAL,
            `16_BY_16` REAL,
            `16_BY_30` REAL,
            `24_BY_30` REAL,
            TOTAL REAL
        );
    """)

    con.execute("""
        CREATE TABLE PERFORMANCE_TOP_10 (
            name TEXT NOT NULL PRIMARY KEY,
            `8_BY_8` REAL,
            `9_BY_9` REAL,
            `16_BY_16` REAL,
            `16_BY_30` REAL,
            `24_BY_30` REAL,
            TOTAL REAL
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

    con.execute("""
        CREATE TABLE PERFORMANCE_ALL (
            name TEXT NOT NULL PRIMARY KEY,
            pp REAL
        );
    """)
        
>>>>>>> 74e0fe7228c019e463541cc7da630021078b3d38

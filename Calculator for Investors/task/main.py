import sqlite3
from sqlite3 import Error

MAIN_MENU = '''
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria
'''
CRUD_MENU = '''
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies
'''
TOP_TEN_MENU = '''
TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA
'''

def do_top10_menu():
    while True:
        print(TOP_TEN_MENU)
        cmd = input('Enter an option:\n')
        if cmd == '0':
            break
        elif cmd in '123':
            print('Not implemented!')
            break
        else:
            print('Invalid option!')

def do_crud_menu():
    while True:
        print(CRUD_MENU)
        cmd = input('Enter an option:\n')
        if cmd == '0':
            break
        elif cmd in '12345':
            print('Not implemented!')
            break
        else:
            print('Invalid option!')

def do_main_menu():
    while True:
        print(MAIN_MENU)
        cmd = input('Enter an option:\n')
        if cmd == '0':
            break
        elif cmd == '1':
            do_crud_menu()
        elif cmd == '2':
            do_top10_menu()
        else:
            print('Invalid option!')
    print('Have a nice day!')

def create_tables(conn):
    sql1 = """CREATE TABLE IF NOT EXISTS companies (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT
            ); """
    sql2 = """CREATE TABLE IF NOT EXISTS financial (
                ticker TEXT PRIMARY KEY,
                ebitda REAL,
                sales REAL,
                net_profit REAL,
                market_price REAL,
                net_debt REAL,
                assets REAL,
                equity REAL,
                cash_equivalents REAL,
                liabilities REAL DEFAULT None
            ); """
    try:
        c = conn.cursor()
        c.execute(sql1)
        c.execute(sql2)
    except Error as e:
        print(e)

def add_comp(conn, data):
    sql = ''' INSERT INTO companies(ticker,name,sector)
                VALUES(?,?,?) '''
    cur = conn.cursor()
    for row in data:
        row = row.replace(', Inc.', ' Inc.')
        cur.execute(sql, row.split(','))
    conn.commit()

def add_fin(conn, data):
    sql = ''' INSERT INTO financial
                VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    for row in data:
        row = [x if x else None for x in row.split(',')]
        cur.execute(sql, row)
    conn.commit()

def read_data(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(line.rstrip())
    return data[1:]

con = sqlite3.connect('investor.db')
create_tables(con)
data = read_data('test/companies.csv')
add_comp(con, data)
data = read_data('test/financial.csv')
add_fin(con, data)
print('Database created successfully!')
con.close()


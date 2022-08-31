import os
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
COMP_STR = '''Enter ticker (in the format 'MOON'):
Enter company (in the format 'Moon Corp'):
Enter industries (in the format 'Technology'):'''
FIN_STR = '''Enter ebitda (in the format '987654321'):
Enter sales (in the format '987654321'):
Enter net profit (in the format '987654321'):
Enter market price (in the format '987654321'):
Enter net dept (in the format '987654321'):
Enter assets (in the format '987654321'):
Enter equity (in the format '987654321'):
Enter cash equivalents (in the format '987654321'):
Enter liabilities (in the format '987654321'):'''

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
            pass
        elif cmd == '1':
            new_company()
        elif cmd == '2':
            read_comp()
        elif cmd == '3':
            upd_comp()
        elif cmd == '4':
            del_comp()
        elif cmd == '5':
            list_all()
        else:
            print('Invalid option!')
            continue
        break

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
        sql = 'SELECT COUNT(ticker) FROM companies'
        cnt = c.execute(sql).fetchone()
        return cnt[0]
    except Error as e:
        print(e)

def new_company():
    vals = []
    for s in COMP_STR.split('\n'):
        vals.append(input(s + '\n'))
    v1 = ','.join(vals)
    add_comp(conn, [v1])
    for s in FIN_STR.split('\n'):
        vals.append(input(s + '\n'))
    v2 = ','.join([vals[0]] + vals[3:])
    add_fin(conn, [v2])
    print('Company created successfully!')

def upd_fin(data):
    sql = ''' UPDATE financial
                SET ebitda = ?,
                    sales = ?,
                    net_profit = ?,
                    market_price = ?,
                    net_debt = ?,
                    assets = ?,
                    equity = ?,
                    cash_equivalents = ?,
                    liabilities = ?    
                WHERE ticker = ? '''
    cur = conn.cursor()
    cur.execute(sql, data.split(','))
    conn.commit()

def add_comp(conn, data):
    sql = ''' INSERT INTO companies(ticker,name,sector)
                VALUES(?,?,?) '''
    cur = conn.cursor()
    for row in data:
        if '"' in row:
            row = row.replace(', Inc.', '_ Inc.')
            row = row.replace('"', '')
            row = row.split(',')
            for i in range(len(row)):
                row[i] = row[i].replace('_', ',')
        else:
            row = row.split(',')
        cur.execute(sql, row)
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

def find_comp():
    mask = input('Enter company name:\n')
    mask = f"%{mask}%"
    sql = '''SELECT ticker, name FROM companies
                WHERE name LIKE ?'''
    cur = conn.cursor()
    res = cur.execute(sql, (mask,)).fetchall()
    comp = ''
    if res:
        for i in range(len(res)):
            print(i, res[i][1])
        num = input('Enter company number:\n')
        comp = res[int(num)]
    else:
        print('Company not found!')
    return comp

def upd_comp():
    comp = find_comp()
    if comp:
        vals = []
        for s in FIN_STR.split('\n'):
            vals.append(input(s + '\n'))
        v = ','.join(vals + [comp[0]])
        upd_fin(v)
        print('Company updated successfully!')

def read_comp():
    comp = find_comp()
    # print(comp)
    if not comp:
        return
    sql = 'SELECT * FROM financial WHERE ticker=?'
    cur = conn.cursor()
    res = cur.execute(sql, (comp[0],)).fetchall()[0]
    print(comp[0], comp[1])
    print(f'P/E = {div(res[4], res[3])}')
    print(f'P/S = {div(res[4], res[2])}')
    print(f'P/B = {div(res[4], res[6])}')
    print(f'ND/EBITDA = {div(res[5], res[1])}')
    print(f'ROE = {div(res[3], res[7])}')
    print(f'ROA = {div(res[3], res[6])}')
    print(f'L/A = {div(res[9], res[6])}')

def div(a, b):
    return None if a is None or b is None else round(a / b, 2)

def del_comp():
    comp = find_comp()
    if comp:
        cur = conn.cursor()
        sql = 'DELETE FROM financial WHERE ticker=?'
        cur.execute(sql, (comp[0],))
        sql = 'DELETE FROM companies WHERE ticker=?'
        cur.execute(sql, (comp[0],))
        conn.commit()
        print('Company deleted successfully!')

def list_all():
    print('COMPANY LIST')
    sql = 'SELECT * FROM companies ORDER BY ticker'
    cur = conn.cursor()
    cur.execute(sql)
    for c in cur.fetchall():
        s = ''
        for w in c:
            s += w + ' '
        print(s.strip())

def create_db():
    # if os.path.exists('investor.db'):
    #     os.remove('investor.db')
    conn = sqlite3.connect('investor.db')
    cnt = create_tables(conn)
    if cnt < 10:
        data = read_data('test/companies.csv')
        add_comp(conn, data)
        data = read_data('test/financial.csv')
        add_fin(conn, data)
    return conn

conn = create_db()
print('Welcome to the Investor Program!')
do_main_menu()
conn.close()

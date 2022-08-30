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

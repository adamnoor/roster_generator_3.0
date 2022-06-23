from operator import truediv
import os.path
from logic_read_db import run_read
from logic_create_db import run_create


x = True
while x:
    
    path = os.path.exists('football.sqlite')

    if path:
        print("Currently you have a table in football.sqlite")
        print("")
        print("Select 1 to rewrite the table")
        print("Select 2 to use the existing table to start building stacks")
        print("Select 3 to quit the script")
        print("")
        user_input = int(input("Make a selection: "))

        if user_input == 1:
            x = run_create()
        elif user_input == 2:
            run_read()
            x = False
        else:
            x = False
    
    else:
        x = run_create()
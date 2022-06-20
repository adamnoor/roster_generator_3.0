from operator import truediv
import os.path
from read_table import run_script
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
            x = run_script()
        else:
            x = False
    
    else:
        x = run_create()
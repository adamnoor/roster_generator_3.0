from operator import truediv
import os.path
from logic_read_db import run_read
from logic_create_db import run_create
from guided_logic import run_guided


keep_running = True
while keep_running:
    
    path = os.path.exists('football.sqlite')

    if path:
        print("Currently you have a table in football.sqlite")
        print("")
        print("Select 1 to rewrite the table")
        print("Select 2 to use the existing table to build a stack")
        print("Select 3 to use this exising table to build a guided stack")
        print("Select 4 to quit the script")
        print("")
        user_input = int(input("Make a selection: "))

        if user_input == 1:
            keep_running = run_create()
        elif user_input == 2:
            run_read()
            keep_running = False
        elif user_input == 3:
            run_guided()
            keep_running = False
        else:
            keep_running = False
    
    else:
        keep_running = run_create()
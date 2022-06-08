import os.path
from read_table import run_script
from create_table import run_create

path = os.path.exists('football.sqlite')

if path:
    print("Currently you have files in the generated_files folder")
    print("")
    print("Select 1 to rewrite the files")
    print("Select 2 to use these files to start building stacks")
    print("")
    user_input = int(input("Make a selection: "))

    if user_input == 1:
        run_create()
    
else:
    run_create()

path = os.path.exists('football.sqlite')

if path:
    print("")
    print("We will now build a stack")
    run_script()
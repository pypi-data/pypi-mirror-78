import os

def exit_func(n):
    print("\n")
    input("Press return to go back ...")
    os.system('cls' if os.name=='nt' else 'clear')
    print("\n")
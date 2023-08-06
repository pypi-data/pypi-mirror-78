from .connect import connect_node
from pyfiglet import Figlet
from .menu import menu
import os

fig = Figlet(font='slant')

def cli():
    os.system('cls' if os.name=='nt' else 'clear')
    print("\n")
    print(fig.renderText('jutsu'))
    print("\n")
    n = connect_node()
    print("\n")
    menu(n)
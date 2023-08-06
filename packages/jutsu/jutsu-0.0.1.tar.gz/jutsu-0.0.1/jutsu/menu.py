from PyInquirer import prompt
from .supply import supply
from .block_height import block_height
from .halving import next_halving
from .chain_size import chain_size

menu_items = [
    {
        'type': 'list',
        'name': 'menu',
        'message': 'What do you want to verify?',
        'choices': [
            'Circulating and maximum supply',
            'Block height',
            'Next halving',
            'Blockchain size',
            'Exit'
        ]
    }
]

confirm = [
    {
        'type': 'confirm',
        'message': 'This operation will take a few minutes. Continue?',
        'name': 'continue',
        'default': True,
    }
]

def menu(n):
    answers = prompt(menu_items)
    if answers['menu'] == "Circulating and total supply":
        confirmation = prompt(confirm)
        if confirmation['continue'] == True:
            supply(n)
            menu(n)
        else:
            menu(n)

    elif answers['menu'] == "Block height":
        block_height(n)
        menu(n)
    
    elif answers['menu'] == "Next halving":
        next_halving(n)
        menu(n)
    
    elif answers['menu'] == "Blockchain size":
        chain_size(n)
        menu(n)
    
    elif answers['menu'] == "Exit":
        exit()
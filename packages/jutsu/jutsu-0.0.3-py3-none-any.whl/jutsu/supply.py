import colorama
from yaspin import yaspin
import time
from .exit_func import exit_func

colorama.init()

@yaspin(text="Verifying...", color="green")
def calculate_circulating(n):
    """returns total amount of Bitcoin in the UTXO set"""
    c = n.gettxoutsetinfo()
    return c['total_amount'], c['height']

def calculate_max():
    """calculates the maximum supply based on btcdirect.eu/en-gb/how-many-bitcoin"""
    summation = 0
    for i in range(0, 33):
        summation += 210000 * ((50*(10**8)) / 2**i)
    
    summation = summation / (10**8)
    return summation

def circ_is_valid(c, maximum):
    """returns true if circulating supply is valid and inferior to total supply"""
    if c < maximum:
        v = True
    else:
        v = False
    return v

def supply(n):
    start = time.time()
    c = calculate_circulating(n)
    maximum = calculate_max()
    valid = circ_is_valid(c[0], maximum)
    calc_sup = (209999*50)+(210000*25)+(210000*12.5)+((int(c[1])-630000)*6.25)
    end = time.time()
    print("\n")
    print(colorama.Fore.WHITE + "Circulating supply:   "+ colorama.Fore.GREEN + str(c[0]) + colorama.Fore.WHITE + " BTC")
    print(colorama.Fore.WHITE + "Calculated supply:   ~"+ colorama.Fore.GREEN + str(calc_sup) + colorama.Fore.WHITE + " BTC")
    print(colorama.Fore.WHITE + "Maximum supply:       "+ colorama.Fore.GREEN + str(maximum) + colorama.Fore.WHITE + " BTC")
    print(colorama.Fore.WHITE + "Valid supply:         "+ colorama.Fore.GREEN + str(valid) + colorama.Fore.WHITE + "")
    print("\n")
    t = (end - start)
    minutes = t // 60
    t %= 60
    seconds = t
    print("Time elapsed: %d minutes and %d seconds" % (minutes, seconds))
    print("\n")
    exit_func(n)

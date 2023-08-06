import colorama
from yaspin import yaspin
import time
from .exit_func import exit_func

colorama.init()

@yaspin(text="Verifying...", color="green")
def current_height(n):
    c = n.getblockchaininfo()
    return int(c['headers'])

def maximum_rewarded_height():
    m = (210000 * 33) - 1
    return m

def block_height(n):
    start = time.time()
    c = current_height(n)
    m = maximum_rewarded_height()
    p = int((c*100) / m)
    end = time.time()
    print("\n")
    print(colorama.Fore.WHITE + "Current block height:              "+ colorama.Fore.GREEN + str(c) + colorama.Fore.WHITE + " Blocks")
    print(colorama.Fore.WHITE + "Maximum rewardable block height:   "+ colorama.Fore.GREEN + str(m) + colorama.Fore.WHITE + " Blocks")
    print(colorama.Fore.WHITE + "Progress:                          "+ colorama.Fore.GREEN + str(p) + "%" + colorama.Fore.WHITE + " of rewardable blocks discovered")
    print("\n")
    t = (end - start)
    seconds = int(t)
    print("Time elapsed: %d seconds" % seconds)
    print("\n")
    exit_func(n)
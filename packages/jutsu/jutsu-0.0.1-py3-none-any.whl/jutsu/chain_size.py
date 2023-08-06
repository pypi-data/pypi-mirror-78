import colorama
from yaspin import yaspin
import time
from .exit_func import exit_func

colorama.init()

@yaspin(text="Calculating...", color="green")
def current_size(n):
    info = n.getblockchaininfo()
    return float(info['size_on_disk'])


def chain_size(n):
    start = time.time()

    cs = current_size(n)
    cs = cs / 1e9
    cs = "%.2f" % cs

    end = time.time()
    print("\n")
    print(colorama.Fore.WHITE + "Current blockchain size:              "+ colorama.Fore.GREEN + str(cs) + colorama.Fore.WHITE + " GB")
    print("\n")
    t = (end - start)
    seconds = int(t)
    print("Time elapsed: %d seconds" % seconds)
    print("\n")
    exit_func(n)
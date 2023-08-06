import colorama
from yaspin import yaspin
import time
import datetime
from .exit_func import exit_func

colorama.init()

@yaspin(text="Calculating...", color="green")
def current_height(n):
    info = n.getblockchaininfo()
    return int(info['headers'])


def next_halving(n):
    start = time.time()

    ch = current_height(n)
    next_halving_height = 210000 + 630000
    remaining_blocks = next_halving_height - ch

    remaining_time_sec = remaining_blocks * 10 * 60

    now = time.time()
    then = now + remaining_time_sec

    halving_date = datetime.datetime.fromtimestamp(then).strftime('%Y-%m-%d %H:%M')
    remaining_time_days = int(remaining_time_sec / 3600 / 24)

    end = time.time()
    print("\n")
    print(colorama.Fore.WHITE + "Next halving:              "+ colorama.Fore.GREEN + str(halving_date) + colorama.Fore.WHITE + "")
    print(colorama.Fore.WHITE + "Time remaining:            "+ colorama.Fore.GREEN + str(remaining_time_days) + colorama.Fore.WHITE + " days")
    print(colorama.Fore.WHITE + "Next block reward:         "+ colorama.Fore.GREEN + str(3.125) + colorama.Fore.WHITE + " BTC")
    print("\n")
    t = (end - start)
    seconds = int(t)
    print("Time elapsed: %d seconds" % seconds)
    print("\n")
    exit_func(n)
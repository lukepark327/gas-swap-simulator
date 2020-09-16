import os
import argparse
import random
import matplotlib.pyplot as plt

from uniswap import Uniswap


def get_PATH(path):
    PATH = (path or 'plots') + '/'
    os.makedirs(PATH, exist_ok=True)
    return PATH


def Gwei2GAS_Swap_Curve(args, pool, display=False):
    delta_Gweis = range(1, 1000000, 1000)
    amount_GASs = []
    for delta_Gwei in delta_Gweis:
        delta_GAS = pool.Gwei_to_GAS(delta_Gwei, bool_update=False)
        amount_GASs.append(delta_GAS / delta_Gwei)  # amount of GAS per 1 Gwei

    # Plot
    fig, ax1 = plt.subplots()

    ln1 = ax1.plot([1, 1000000], [200, 200], 'r-', label='original')  # straight line
    ax1.set_xlabel('Gwei')
    ax1.set_ylabel('GAS', color='r')
    ax1.set_ylim((95, 205))
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ln2 = ax2.plot(delta_Gweis, amount_GASs, 'b-', label='uniswap')
    ax2.set_ylabel('GAS', color='b')
    ax2.set_ylim((95, 205))
    ax2.tick_params('y', colors='b')

    lns = ln1 + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Gwei2GAS_Swap_Curve.png', format='png', dpi=300)


def GAS2Gwei_Swap_Curve(args, pool, display=False):
    delta_GASs = range(1, 200000000, 200000)
    amount_Gweis = []
    for delta_GAS in delta_GASs:
        delta_Gwei = us.GAS_to_Gwei(delta_GAS, bool_update=False)
        amount_Gweis.append(delta_Gwei / delta_GAS)  # amount of GAS per 1 Gwei

    n_err = amount_Gweis.count(0.)

    # Plot
    fig, ax1 = plt.subplots()

    ln1 = ax1.plot([1, 200000000], [0.005, 0.005], 'r-', label='original')  # straight line
    ax1.set_xlabel('GAS')
    ax1.set_ylabel('Gwei', color='r')
    ax1.set_ylim((0.0022, 0.0052))
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ln2 = ax2.plot(delta_GASs[n_err:], amount_Gweis[n_err:], 'b-', label='uniswap')
    ax2.set_ylabel('Gwei', color='b')
    ax2.set_ylim((0.0022, 0.0052))
    ax2.tick_params('y', colors='b')

    lns = ln1 + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'GAS2Gwei_Swap_Curve.png', format='png', dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=950327)
    parser.add_argument('--path')  # location of log files
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(args)

    random.seed(args.seed)

    """init"""
    us = Uniswap(address='-1',
                 amount_Gwei=1000000,
                 amount_GAS=200000000,  # Gwei:GAS = 1:200
                 init_LT=1000000,
                 fee=0.003)
    print(">>> init pool.")
    us.print_pool_state(bool_LT=True)

    """Simulation 1-1) Gwei -> GAS Swap curve"""
    Gwei2GAS_Swap_Curve(args, us, display=args.no_save)

    """Simulation 1-2) GAS -> Gwei Swap curve"""
    GAS2Gwei_Swap_Curve(args, us, display=args.no_save)

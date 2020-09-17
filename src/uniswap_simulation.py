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


def LP_k_GweiNGAS_Curve(args, pool, display=False):
    ks, Gweis, GASs = [], [], []
    ks.append(us.k)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            us.Gwei_to_GAS(105)
        else:
            us.GAS_to_Gwei_exact(105)

        ks.append(us.k)
        Gweis.append(us.Gwei)
        GASs.append(us.GAS)

    print(">>> after 1000 txs.")
    us.print_pool_state(bool_LT=True)

    """Providing Lquidity"""
    input_Gwei = 200000
    required_GAS = us.required_GAS_for_liquidity(input_Gwei)
    print(">>> input (Gwei, GAS) = ({}, {})".format(input_Gwei, required_GAS))
    get_LT = us.join('0', input_Gwei, required_GAS)
    ks.append(us.k)

    print(">>> after LP.")
    us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            us.Gwei_to_GAS(105)
        else:
            us.GAS_to_Gwei_exact(105)

        ks.append(us.k)
        Gweis.append(us.Gwei)
        GASs.append(us.GAS)

    print(">>> after 1000 txs.")
    us.print_pool_state(bool_LT=True)

    """Remove Lquidity"""
    withdraw_LT = get_LT
    get_Gwei, get_GAS = us.out('0', withdraw_LT)
    print(">>> output (Gwei, GAS) = ({}, {})".format(get_Gwei, get_GAS))
    ks.append(us.k)

    print(">>> after LP remove.")
    us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            us.Gwei_to_GAS(105)
        else:
            us.GAS_to_Gwei_exact(105)

        ks.append(us.k)
        Gweis.append(us.Gwei)
        GASs.append(us.GAS)

    print(">>> after 1000 txs.")
    us.print_pool_state(bool_LT=True)

    """Plot"""
    # k_Curve
    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(ks, 'c-', label='k')
    ax1.set_xlabel('transaction')
    ax1.set_ylabel('k')  # , color='c')
    # ax1.tick_params('y', colors='c')

    plt.legend()

    plt.axvline(x=1000, color='gray', linestyle=':', linewidth=2)
    plt.axvline(x=2000, color='gray', linestyle=':', linewidth=2)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'LP_k_Curve.png', format='png', dpi=300)

    # GweiNGAS_Curve
    fig, ax1 = plt.subplots()

    ln1 = ax1.plot(Gweis, 'b-', label='Gwei')
    ax1.set_xlabel('transaction')
    ax1.set_ylabel('Gwei', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ln2 = ax2.plot(GASs, 'r-', label='GAS')
    ax2.set_ylabel('GAS', color='r')
    ax2.tick_params('y', colors='r')

    lns = ln1 + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    plt.axvline(x=1000, color='gray', linestyle=':', linewidth=2)
    plt.axvline(x=2000, color='gray', linestyle=':', linewidth=2)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'LP_GweiNGAS_Curve.png', format='png', dpi=300)


def fee_Gain_Curve():
    pass


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
    # Gwei2GAS_Swap_Curve(args, us, display=args.no_save)

    """Simulation 1-2) GAS -> Gwei Swap curve"""
    # GAS2Gwei_Swap_Curve(args, us, display=args.no_save)

    """Simulation 2-1) Providing Liquidity & k"""
    # LP_k_GweiNGAS_Curve(args, us, display=args.no_save)

    """Simulation 2-2) Fee & LP's Gain"""
    fee_Gain_Curve(args, us, display=args.no_save)

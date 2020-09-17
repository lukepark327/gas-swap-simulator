import os
import argparse
import random
import matplotlib.pyplot as plt
from copy import deepcopy

from uniswap import Uniswap


def get_PATH(path):
    PATH = (path or 'plots/uniswap') + '/'
    os.makedirs(PATH, exist_ok=True)
    return PATH


def Swap_k_Curve(args, pool, display=False):
    tmp_pool = deepcopy(pool)

    ks, Gweis, GASs = [], [], []
    ks.append(tmp_pool.k)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105)
        else:
            tmp_pool.GAS_to_Gwei_exact(105)

        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

    print(">>> after 1000 txs.")
    tmp_pool.print_pool_state(bool_LT=True)

    """Plot"""
    # k_Curve
    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(ks, 'c-', label='k')
    ax1.set_xlabel('transaction')
    ax1.set_ylim((1998.9e11, 2001.6e11))
    ax1.set_ylabel('k')  # , color='c')
    # ax1.tick_params('y', colors='c')

    plt.legend()

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Swap_k_Curve.png', format='png', dpi=300)

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
    ax1.legend(lns, labs, loc='upper left')

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Swap_GweiNGAS_Curve.png', format='png', dpi=300)


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
        delta_Gwei = pool.GAS_to_Gwei(delta_GAS, bool_update=False)
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
    tmp_pool = deepcopy(pool)

    ks, Gweis, GASs = [], [], []
    ks.append(tmp_pool.k)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105)
        else:
            tmp_pool.GAS_to_Gwei_exact(105)

        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

    print(">>> after 1000 txs.")
    tmp_pool.print_pool_state(bool_LT=True)

    """Providing Lquidity"""
    input_Gwei = 200000
    required_GAS = tmp_pool.required_GAS_for_liquidity(input_Gwei)
    print(">>> input (Gwei, GAS) = ({}, {})".format(input_Gwei, required_GAS))
    get_LT = tmp_pool.join('0', input_Gwei, required_GAS)
    ks.append(tmp_pool.k)

    print(">>> after LP.")
    tmp_pool.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105)
        else:
            tmp_pool.GAS_to_Gwei_exact(105)

        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

    print(">>> after 1000 txs.")
    tmp_pool.print_pool_state(bool_LT=True)

    """Remove Lquidity"""
    withdraw_LT = get_LT
    get_Gwei, get_GAS = tmp_pool.out('0', withdraw_LT)
    print(">>> output (Gwei, GAS) = ({}, {})".format(get_Gwei, get_GAS))
    ks.append(tmp_pool.k)

    print(">>> after LP remove.")
    tmp_pool.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000):  # 1000 Rounds
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105)
        else:
            tmp_pool.GAS_to_Gwei_exact(105)

        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

    print(">>> after 1000 txs.")
    tmp_pool.print_pool_state(bool_LT=True)

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


def LP_LT_Curve(args, pool, display=False):
    input_Gweis = range(200000, 1000000, 10000)
    LTs = []
    for input_Gwei in input_Gweis:
        required_GAS = pool.required_GAS_for_liquidity(input_Gwei)
        # print(">>> input (Gwei, GAS) = ({}, {})".format(input_Gwei, required_GAS))
        get_LT = pool.join('0', input_Gwei, required_GAS, bool_update=False)
        LTs.append(get_LT)

    """Plot"""
    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(input_Gweis, LTs, 'b-', label='LT')
    ax1.set_xlabel('Gwei')
    ax1.set_ylabel('LT')

    plt.legend()

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'LP_LT_Curve.png', format='png', dpi=300)


def fee_Gain_Curve(args, pool, display=False):
    fees = range(1, 11)  # n * (1/1000) [%]
    Gains = []
    for fee in fees:
        tmp_pool = deepcopy(pool)  # copy
        fee /= 1000.
        tmp_pool.fee = fee

        """Providing Lquidity"""
        input_Gwei = 200000
        required_GAS = tmp_pool.required_GAS_for_liquidity(input_Gwei)
        get_LT = tmp_pool.join('0', input_Gwei, required_GAS, bool_update=True)

        """Txs"""
        for i in range(1000):  # 1000 Rounds
            if i % 2 == 0:
                tmp_pool.Gwei_to_GAS(105)
            else:
                tmp_pool.GAS_to_Gwei_exact(105)

        """Remove Lquidity"""
        withdraw_LT = get_LT
        get_Gwei, get_GAS = tmp_pool.out('0', withdraw_LT)
        # print(">>> output (Gwei, GAS) = ({}, {})".format(get_Gwei, get_GAS))
        Gain = get_Gwei * 200 + get_GAS
        Gains.append(Gain)

    """Plot"""
    fig, ax1 = plt.subplots()
    ln1 = ax1.plot([fee / 1000. for fee in fees], Gains, 'r-', label='GAS')
    ax1.set_xlabel('fee')
    ax1.set_ylabel('GAS')

    plt.legend()

    plt.axvline(x=0.003, color='gray', linestyle=':', linewidth=2)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Fee_Gain_Curve.png', format='png', dpi=300)


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

    """Simulation 1-1) Swap & k"""
    Swap_k_Curve(args, us, display=args.no_save)

    """Simulation 1-2) Gwei -> GAS Swap Curve"""
    Gwei2GAS_Swap_Curve(args, us, display=args.no_save)

    """Simulation 1-3) GAS -> Gwei Swap Curve"""
    GAS2Gwei_Swap_Curve(args, us, display=args.no_save)

    """Simulation 2-1) Providing Liquidity & k"""
    LP_k_GweiNGAS_Curve(args, us, display=args.no_save)

    """Simulation 2-3) LP & LT"""
    LP_LT_Curve(args, us, display=args.no_save)

    """Simulation 2-3) Fee & LP's Gain"""
    fee_Gain_Curve(args, us, display=args.no_save)

import os
import argparse
import random
import matplotlib.pyplot as plt
from copy import deepcopy

from uniswap import Uniswap
from arbitrager import Arbitrager
from circuitbreaker import Uniswap_with_CB


def get_PATH(path):
    PATH = (path or 'plots/circuitbreaker') + '/'
    os.makedirs(PATH, exist_ok=True)
    return PATH


def CB_Curve(args, pool, display=False):
    tmp_pool = deepcopy(pool)

    ks, Gweis, GASs, highs, lows = [], [], [], [], []
    ks.append(tmp_pool.k)
    Gweis.append(tmp_pool.Gwei)
    GASs.append(tmp_pool.GAS)

    """Txs"""
    for i in range(10000):  # 1000 Rounds
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105 * 5)
        else:
            tmp_pool.GAS_to_Gwei_exact(105 * 5)

        cb = tmp_pool.circuit_break(oracle_ratio=200.)
        if cb == 1:
            highs.append(i)
        elif cb == -1:
            lows.append(i)

        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

    print(">>> low: {} | high: {} | normal: {}".format(tmp_pool.low, tmp_pool.high, tmp_pool.normal))

    """Plot"""
    # k_Curve
    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(ks, 'c-', label='k')
    ax1.set_xlabel('transaction')
    # ax1.set_ylim((1998.9e11, 2001.6e11))
    ax1.set_ylabel('k')  # , color='c')
    # ax1.tick_params('y', colors='c')

    plt.legend(loc='lower right')

    for i in range(len(highs)):
        plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

    for i in range(len(lows)):
        plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'k_Curve.png', format='png', dpi=300)

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
    ax1.legend(lns, labs, loc='lower right')

    for i in range(len(highs)):
        plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

    for i in range(len(lows)):
        plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'GweiNGAS_Curve.png', format='png', dpi=300)


def Threshold_CB_Curve(args, pool, display=False):
    tmp_pool_3 = deepcopy(pool)     # 3%
    tmp_pool_5 = deepcopy(pool)     # 5%
    tmp_pool_10 = deepcopy(pool)    # 10%

    tmp_pool_3.update_threshold(0.03)
    # tmp_pool_5.update_threshold(0.05)
    tmp_pool_10.update_threshold(0.1)

    pseudo_randoms = [random.random() for _ in range(10000)]

    for t, tmp_pool in zip([3, 5, 10], [tmp_pool_3, tmp_pool_5, tmp_pool_10]):
        ks, Gweis, GASs, highs, lows = [], [], [], [], []
        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

        """Txs"""
        for i, pseudo_random in enumerate(pseudo_randoms):  # 1000 Rounds
            if pseudo_random < 0.5:
                tmp_pool.Gwei_to_GAS(105 * 5)
            else:
                tmp_pool.GAS_to_Gwei_exact(105 * 5)

            cb = tmp_pool.circuit_break(oracle_ratio=200.)
            if cb == 1:
                highs.append(i)
            elif cb == -1:
                lows.append(i)

            ks.append(tmp_pool.k)
            Gweis.append(tmp_pool.Gwei)
            GASs.append(tmp_pool.GAS)

        print(">>> {} | low: {} | high: {} | normal: {}".format(t, tmp_pool.low, tmp_pool.high, tmp_pool.normal))

        """Plot"""
        # k_Curve
        fig, ax1 = plt.subplots()
        ln1 = ax1.plot(ks, 'c-', label='k')
        ax1.set_xlabel('transaction')
        # ax1.set_ylim((1998.9e11, 2001.6e11))
        ax1.set_ylabel('k')  # , color='c')
        # ax1.tick_params('y', colors='c')

        plt.legend(loc='lower right')

        for i in range(len(highs)):
            plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

        for i in range(len(lows)):
            plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

        if display:
            plt.show()
        else:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(8, 6)
            plt.savefig(get_PATH(args.path) + str(t) + '_k_Curve.png', format='png', dpi=300)

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
        ax1.legend(lns, labs, loc='lower right')

        for i in range(len(highs)):
            plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

        for i in range(len(lows)):
            plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

        if display:
            plt.show()
        else:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(8, 6)
            plt.savefig(get_PATH(args.path) + str(t) + '_GweiNGAS_Curve.png', format='png', dpi=300)


def CB_vs_Curve(args, pool, actor, display=False):
    tmp_pool_swap = deepcopy(pool)
    tmp_pool_navie = deepcopy(pool)
    tmp_pool_arbitrage = deepcopy(pool)

    # tmp_pool_swap.update_mode("swap")
    tmp_pool_navie.update_mode("nothing")
    tmp_pool_arbitrage.update_mode("nothing")

    pseudo_randoms = [random.random() for _ in range(10000)]

    for t, tmp_pool in zip(["swap", "nothing", "arbitrage"], [tmp_pool_swap, tmp_pool_navie, tmp_pool_arbitrage]):
        ks, Gweis, GASs, highs, lows = [], [], [], [], []
        ks.append(tmp_pool.k)
        Gweis.append(tmp_pool.Gwei)
        GASs.append(tmp_pool.GAS)

        """Txs"""
        for i, pseudo_random in enumerate(pseudo_randoms):  # 1000 Rounds
            if pseudo_random < 0.5:
                tmp_pool.Gwei_to_GAS(105 * 5)
            else:
                tmp_pool.GAS_to_Gwei_exact(105 * 5)

            if t == "arbitrage":
                actor.arbitrage(tmp_pool)

            cb = tmp_pool.circuit_break(oracle_ratio=200.)
            if cb == 1:
                highs.append(i)
            elif cb == -1:
                lows.append(i)

            ks.append(tmp_pool.k)
            Gweis.append(tmp_pool.Gwei)
            GASs.append(tmp_pool.GAS)

        print(">>> {} | low: {} | high: {} | normal: {}".format(t, tmp_pool.low, tmp_pool.high, tmp_pool.normal))

        """Plot"""
        # k_Curve
        fig, ax1 = plt.subplots()
        ln1 = ax1.plot(ks, 'c-', label='k')
        ax1.set_xlabel('transaction')
        # ax1.set_ylim((1998.9e11, 2001.6e11))
        ax1.set_ylabel('k')  # , color='c')
        # ax1.tick_params('y', colors='c')

        plt.legend(loc='lower right')

        for i in range(len(highs)):
            if t == "nothing":
                plt.axvspan(min(highs[i], 9999), min(highs[i] + 1, 10000), facecolor='black', alpha=0.4)
            else:
                plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

        for i in range(len(lows)):
            plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

        if display:
            plt.show()
        else:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(8, 6)
            plt.savefig(get_PATH(args.path) + t + '_k_Curve.png', format='png', dpi=300)

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
        ax1.legend(lns, labs, loc='lower right')

        for i in range(len(highs)):
            if t == "nothing":
                plt.axvspan(min(highs[i], 9999), min(highs[i] + 1, 10000), facecolor='black', alpha=0.4)
            else:
                plt.axvline(x=highs[i], color='black', linestyle='-', alpha=0.4, linewidth=2)

        for i in range(len(lows)):
            plt.axvline(x=lows[i], color='gray', linestyle=':', linewidth=2)

        if display:
            plt.show()
        else:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(8, 6)
            plt.savefig(get_PATH(args.path) + t + '_GweiNGAS_Curve.png', format='png', dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=950327)
    parser.add_argument('--path')  # location of log files
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(args)

    random.seed(args.seed)

    """init"""
    us_CB = Uniswap_with_CB(address='-1',
                            amount_Gwei=1000000,
                            amount_GAS=200000000,
                            init_LT=1000000,
                            fee=0.003,
                            CB_mode="swap",    # "swap", "pause", "nothing"
                            threshold=0.05)    # 5%
    arbitrager = Arbitrager(1000000000, 200.)  # [GAS]

    # """Simulation 1)
    # # Gwei <-> GAS & CB Timing
    # # k & CB Timing
    # """
    # CB_Curve(args, us_CB, display=args.no_save)

    # Simulate one at a time.
    """Simulation 2)
    # Threshold & CB
    # Gwei <-> GAS & CB Timing
    # k & CB Timing
    """
    # Threshold_CB_Curve(args, us_CB, display=args.no_save)

    # Simulate one at a time.
    """Simulation 3)
    # Circuit Breaker vs. None
    # Circuit Breaker vs. Arbitrager
    """
    CB_vs_Curve(args, us_CB, arbitrager, display=args.no_save)

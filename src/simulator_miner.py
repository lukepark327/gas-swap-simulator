import os
import argparse
import random
import matplotlib.pyplot as plt
from copy import deepcopy

from uniswap import Uniswap
from miner import Miner


def get_PATH(path):
    PATH = (path or 'plots/miner') + '/'
    os.makedirs(PATH, exist_ok=True)
    return PATH


def Rewarded_by_Pool(args, pool, actor, display=False):
    tmp_pool = deepcopy(pool)
    tmp_actor = deepcopy(actor)

    balances_Gwei, balances_GAS = [], []
    balances_Gwei.append(tmp_actor.balance_Gwei)
    balances_GAS.append(tmp_actor.balance_GAS)

    for i in range(1000):
        if random.random() < 0.5:
            tmp_pool.Gwei_to_GAS(105)
        else:
            tmp_pool.GAS_to_Gwei_exact(105)

        tmp_actor.reward(pool=tmp_pool)
        balances_Gwei.append(tmp_actor.balance_Gwei)
        balances_GAS.append(tmp_actor.balance_GAS)

    """Plot"""
    fig, ax1 = plt.subplots()

    ln1 = ax1.plot(balances_Gwei, 'b-', label='Gwei')
    ax1.set_xlabel('block')
    ax1.set_ylabel('Gwei', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ln2 = ax2.plot(balances_GAS, 'r-', linewidth=8, alpha=0.2, label='GAS')
    ax2.set_ylabel('GAS', color='r')
    ax2.tick_params('y', colors='r')

    lns = ln1 + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Pool_Curve.png', format='png', dpi=300)


def Rewarded_by_Oracle(args, pool, actor, display=False):
    tmp_actor = deepcopy(actor)
    tmp_actor.reward_mode = "oracle"

    balances_Gwei, balances_GAS = [], []
    balances_Gwei.append(tmp_actor.balance_Gwei)
    balances_GAS.append(tmp_actor.balance_GAS)

    for i in range(1000):
        tmp_actor.reward(oracle_ratio=200.)
        balances_Gwei.append(tmp_actor.balance_Gwei)
        balances_GAS.append(tmp_actor.balance_GAS)

    """Plot"""
    fig, ax1 = plt.subplots()

    ln1 = ax1.plot(balances_Gwei, 'b-', label='Gwei')
    ax1.set_xlabel('block')
    ax1.set_ylabel('Gwei', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ln2 = ax2.plot(balances_GAS, 'r-', linewidth=8, alpha=0.2, label='GAS')
    ax2.set_ylabel('GAS', color='r')
    ax2.tick_params('y', colors='r')

    lns = ln1 + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Oracle_Curve.png', format='png', dpi=300)


def Pool_vs_Oracle(args, pool, actor, display=False):
    tmp_actor_pool = deepcopy(actor)
    tmp_actor_oracle = deepcopy(actor)
    tmp_actor_oracle.reward_mode = "oracle"

    init_oracle_ratio, end_oracle_ratio = 200., 2000.
    total_round = 1000

    balances_pool, balances_oracle = [], []
    balances_pool.append(tmp_actor_pool.balance_Gwei * init_oracle_ratio + tmp_actor_pool.balance_GAS)
    balances_oracle.append(tmp_actor_oracle.balance_Gwei * init_oracle_ratio + tmp_actor_oracle.balance_GAS)

    for t, tmp_actor in zip(["pool", "oracle"], [tmp_actor_pool, tmp_actor_oracle]):
        current_oracle_ratio = init_oracle_ratio

        balances_Gwei, balances_GAS = [], []
        balances_Gwei.append(tmp_actor.balance_Gwei)
        balances_GAS.append(tmp_actor.balance_GAS)

        if t == "pool":
            tmp_pool = deepcopy(pool)

            for i in range(total_round):
                if random.random() < 0.5:
                    tmp_pool.Gwei_to_GAS(105)
                else:
                    tmp_pool.GAS_to_Gwei_exact(105)

                current_oracle_ratio = init_oracle_ratio + (end_oracle_ratio - init_oracle_ratio) / (total_round - i)
                # print(current_oracle_ratio)

                tmp_actor.reward(pool=tmp_pool)
                balances_Gwei.append(tmp_actor.balance_Gwei)
                balances_GAS.append(tmp_actor.balance_GAS)
                balances_pool.append(tmp_actor.balance_Gwei * current_oracle_ratio + tmp_actor.balance_GAS)

        elif t == "oracle":
            for i in range(total_round):
                current_oracle_ratio = init_oracle_ratio + (end_oracle_ratio - init_oracle_ratio) / (total_round - i)
                # print(current_oracle_ratio)

                tmp_actor.reward(oracle_ratio=current_oracle_ratio)
                balances_Gwei.append(tmp_actor.balance_Gwei)
                balances_GAS.append(tmp_actor.balance_GAS)
                balances_oracle.append(tmp_actor.balance_Gwei * current_oracle_ratio + tmp_actor.balance_GAS)

        """Plot"""
        # GweiNGAS
        fig, ax1 = plt.subplots()

        ln1 = ax1.plot(balances_Gwei, 'b-', label='Gwei')
        ax1.set_xlabel('block')
        ax1.set_ylabel('Gwei', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ln2 = ax2.plot(balances_GAS, 'r-', linewidth=8, alpha=0.2, label='GAS')
        ax2.set_ylabel('GAS', color='r')
        ax2.tick_params('y', colors='r')

        lns = ln1 + ln2
        labs = [ln.get_label() for ln in lns]
        ax1.legend(lns, labs)

        if display:
            plt.show()
        else:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(8, 6)
            plt.savefig(get_PATH(args.path) + t + '_dynamic_Oracle_ratio_Curve.png', format='png', dpi=300)

    # total balance
    fig, ax1 = plt.subplots()

    # # smoothing
    # smoothen_diff = []
    # window = 3
    # for i in range(int(window/2), total_round-int(window/2)):
    #     avg_balances_pool = sum(balances_pool[i-int(window/2) : i+int(window/2)]) / window
    #     avg_balances_oracle = sum(balances_oracle[i-int(window/2) : i+int(window/2)]) / window
    #     smoothen_diff.append(avg_balances_oracle-avg_balances_pool)
    # ln1 = ax1.plot(smoothen_diff, 'r-', label='oracle - pool')    

    ln1 = ax1.plot([balances_oracle[r] - balances_pool[r] for r in range(total_round)], 'r-', label='oracle - pool')    
    # ln1 = ax1.plot(balances_pool, 'r-', label='pool')
    # ln2 = ax1.plot(balances_oracle, 'b-', label='oracle')
    ax1.set_xlabel('block')
    ax1.set_ylabel('GAS')

    lns = ln1  # + ln2
    labs = [ln.get_label() for ln in lns]
    ax1.legend(lns, labs)

    if display:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(get_PATH(args.path) + 'Total_dynamic_Oracle_ratio_Curve.png', format='png', dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=950327)
    parser.add_argument('--path')  # location of log files
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(args)

    random.seed(args.seed)

    current_block_number = 0
    current_block_gas_limit = 12000000

    """init"""
    us = Uniswap(address='-1',
                 amount_Gwei=1000000,
                 amount_GAS=200000000,  # Gwei:GAS = 1:200
                 init_LT=1000000,
                 fee=0.003)

    miner = Miner(current_block_number,
                  current_block_gas_limit)

    print(">>> init pool.")
    us.print_pool_state(bool_LT=True)

    """Simulation)
    # Test rewarding system
    # Simulate one at a time.
    """

    # """Simulation 1-1) pool"""
    # Rewarded_by_Pool(args, us, miner, display=args.no_save)

    # """Simulation 1-2) oracle"""
    # Rewarded_by_Oracle(args, us, miner, display=args.no_save)

    """Simulation 1-3) oracle (non-decreasing)
    # pool vs. oracle
    """
    Pool_vs_Oracle(args, us, miner, display=args.no_save)

import argparse
import numpy as np
import random
import matplotlib.pyplot as plt

# from uniswap import Uniswap
from circuitbreaker import Uniswap_with_CB
from arbitrager import Arbitrager
from miner import Miner


def argparsing():
    parser = argparse.ArgumentParser()

    """Participant"""
    parser.add_argument('--nUsers', type=int, default=100)
    # parser.add_argument('--nMiners', type=int, default=3)  # 1
    # parser.add_argument('--nProviders', type=int, default=10)  # 1
    # parser.add_argument('--nArbitrager', type=int, default=10)  # 1

    """Simulator"""
    parser.add_argument('--nRounds', type=int, default=10000)
    parser.add_argument('--gas', type=str, default='original',
                        choices=('original', 'uniswap'))
    parser.add_argument('--mining', type=str, default='fee',
                        choices=('fee', 'knapsack'))
    parser.add_argument('--reward', type=str, default='pool',
                        choices=('pool', 'oracle'))
    parser.add_argument('--CB', type=str, default='nothing',
                        choices=('swap', 'pause', 'nothing'))

    """Extra infos"""
    parser.add_argument('--seed', type=int, default=950327)
    parser.add_argument('--path')  # location of log files

    return parser.parse_args()


if __name__ == "__main__":
    args = argparsing()
    # print(args)

    random.seed(args.seed)

    """Hyperparams"""
    current_block_number = 0
    current_block_gas_limit = 12000000

    """Set Users & Transaction Pool"""
    users = []  # index: id
    for i in range(args.nUsers):
        users.append(0)  # initial nonce value

    tx_pool = []
    # tx = {'owner': owner, 'block': block, 'fee': fee}

    """Set Miner"""
    miner = Miner(current_block_number,
                  current_block_gas_limit,
                  mining_mode=args.mining,
                  reward_mode=args.reward)

    """Set Swap Pool"""
    us = Uniswap_with_CB(address='-1',
                         amount_Gwei=1000000,
                         amount_GAS=200000000,  # Gwei:GAS = 1:200
                         init_LT=1000000,
                         fee=0.003,
                         CB_mode=args.CB,       # if "nothing", it works like normal Uniswap protocol.
                         threshold=0.05)

    print(">>> initial pool state")
    us.print_pool_state(bool_LT=True)

    """Simulation
    # Time unit         : block
    # Transaction type  : payment (21000 gas)
    # Gas
    # TBA
    """
    for current_block in range(args.nRounds):
        pass

        if args.gas == "original":
            pass

        elif args.gas == "uniswap":
            pass

        # latest_block

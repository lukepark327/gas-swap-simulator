import argparse
import numpy as np
import random


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
    parser.add_argument('--miner', type=str, default='fee',
                        choices=('fee', 'knapsack'))
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

    """Set users"""
    users = []
    for i in range(args.nUsers):
        user = {
            'address': str(i),
            'nonce': 0}

    print(users)

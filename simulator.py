import argparse
import numpy as np


def argparsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nUsers', type=int, default=100)
    parser.add_argument('--nMiners', type=int, default=3)
    parser.add_argument('--nProviders', type=int, default=10)
    parser.add_argument('--nRounds', type=int, default=1000)
    parser.add_argument('--strategy', type=str, default='fee',
                        choices=('fee', 'knapsack'))
    parser.add_argument('--seed', type=int, default=950327)
    parser.add_argument('--path')  # location of log files

    return parser.parse_args()


if __name__ == "__main__":
    args = argparsing()
    # print(args)

    """Extrs data"""
    burn_address = '-1'
    
    # patience = {'high': 100, 'middle': 50, 'low': 10}  # blocks


    users = []
    for i in range(args.nUsers):
        user = {
            'address'   : str(i),
            'balance'   : ,
            'nonce'     : 0,
            'patience'  : 
        }
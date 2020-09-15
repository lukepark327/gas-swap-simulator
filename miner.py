"""TODO
# multiple miners
"""


import operator
from math import floor


class Miner():
    def __init__(self,
                 current_block_number,
                 current_block_gas_limit,
                 mining_mode="fee",     # "fee" of "knapsack"
                 reward_mode="pool",    # "pool" or "oracle"
                 ):

        self.block_number = current_block_number
        self.block_gas_limit = current_block_gas_limit

        self.mining_mode = mining_mode
        self.reward_mode = reward_mode

        # balance(s)
        self.balance_Gwei, self.balance_GAS = 0, 0

        # params
        self.gas_limit_bound = 1024  # params/protocol_params.go @ Geth
        self.block_reward_Gwei = int(2e+9)  # Gwei  # consensus/ethash/consensus.go @ Geth

    def update(self, gas_upside=True):
        self.block_number += 1
        self._update_gas_limit(upside=gas_upside)

    """gas"""

    def _update_gas_limit(self, upside=True):
        if upside:
            self.block_gas_limit *= (1. + (1. / self.gas_limit_bound))
        else:
            self.block_gas_limit *= (1. - (1. / self.gas_limit_bound))

        self.block_gas_limit = floor(self.block_gas_limit)
        return self.block_gas_limit

    """mining"""

    def _mine_kanpsack(self, txs):
        # 0-1 Knapsack Problem
        # TBA
        raise Exception("not yet implemented.")

    def _mine_fee(self, txs):
        # Greedy: sorting by fee

        sorted_txs = sorted(txs, key=operator.itemgetter(1), reverse=True)

        total_gas = 0
        i, j = -1, 0
        for j, tx in enumerate(sorted_txs):
            if tx[1] > self.block_gas_limit:
                i = j
                continue

            total_gas += tx[1]
            if total_gas > self.block_gas_limit:
                total_gas -= tx[1]
                break

        return total_gas, sorted_txs[i + 1:j]

    def mine(self, txs):
        # Empty block
        if len(txs) == 0:
            return []

        if self.mining_mode == "knapsack":
            return self._mine_kanpsack(txs)
        elif self.mining_mode == "fee":
            return self._mine_fee(txs)
        else:
            raise Exception("invalid mining mode")

    """Reward"""

    def _reward_via_pool(self, pool):
        return pool.required_GAS_for_liquidity(self.block_reward_Gwei)

    def _reward_via_oracle(self, oracle_ratio):
        return oracle_ratio * self.block_reward_Gwei  # ex) 200

    def reward(self, pool=None, oracle_ratio=None):
        if self.reward_mode == "pool":
            block_reward_GAS = self._reward_via_pool(pool)
        elif self.reward_mode == "oracle":
            block_reward_GAS = self._reward_via_oracle(oracle_ratio)
        else:
            raise Exception("invalid mining mode")

        self.balance_Gwei += self.block_reward_Gwei
        self.balance_GAS += block_reward_GAS

        return block_reward_GAS

    """Balance"""

    def deposit_Gwei(self, amount):
        self.balance_Gwei += amount

    def deposit_GAS(self, amount):
        self.balance_GAS += amount

    def withdraw_Gwei(self, amount):
        if self.balance_Gwei - amount < 0:
            raise Exception("invalid amount.")
        self.balance_Gwei -= amount

    def withdraw_GAS(self, amount):
        if self.balance_GAS - amount < 0:
            raise Exception("invalid amount.")
        self.balance_GAS -= amount

    """Logging"""

    def print_block_state(self):
        print("number\t\tgas_limit")
        print("{}\t\t{}".format(self.block_number, self.block_gas_limit))
        print('\n')

    def print_balance_state(self):
        print("Gwei\t\t\tGAS")
        print("{}\t\t{}".format(self.balance_Gwei, self.balance_GAS))
        print('\n')


if __name__ == "__main__":
    current_block_number = 0
    current_block_gas_limit = 12000000
    # block_interval = 15000  # milliseconds  # ignore now

    miner = Miner(current_block_number,
                  current_block_gas_limit)

    """test mining"""
    txs = [  # (tx_id, fee)
        (0, 21000),
        (1, 100000),
        (2, 52000),
        (3, 76000),
        (4, 21000),
        (5, 110000),
        (6, 58000),
        (7, 73000),
        (8, 23000),
        (9, 70000),
        (10, 72000),
        (11, 126000),
        (12, 21000),
        (13, 21000),
        (14, 52000),
        (15, 21000)]

    print(miner.mine(txs))

    """test block update"""
    miner.print_block_state()

    for _ in range(10):
        miner.update()
    miner.print_block_state()

    """test rewarding system"""
    miner.print_balance_state()

    # case 1: pool
    from uniswap import Uniswap
    us = Uniswap('-1', 100000, 20000000)  # 1:200
    print(miner.reward(pool=us))
    miner.print_balance_state()

    # case 2: oracle
    miner.reward_mode = "oracle"
    print(miner.reward(oracle_ratio=200.))
    miner.print_balance_state()

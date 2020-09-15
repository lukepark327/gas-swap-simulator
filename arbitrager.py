
class Arbitrager:
    def __init__(self,
                 oracle_ratio):
        self.oracle_ratio = oracle_ratio

    def update(self, oracle_ratio):
        self.oracle_ratio = oracle_ratio

    """Arbitraging"""

    def _Gwei_to_GAS(self, pool):
        pass

    def _GAS_to_Gwei(self, pool):
        pass

    def tx_fee(self, tx_type):
        # https://hackmd.io/@HaydenAdams/HJ9jLsfTz?type=view#Gas-Benchmarks
        if tx_type == "Gwei2GAS":
            return 46000
        elif tx_type == "GAS2Gwei":
            return 60000
        else:
            return 21000

    def arbitrage(self, pool):
        current_Gwei, current_GAS = pool.Gwei, pool.GAS
        pool_ratio = float(current_GAS / current_Gwei)

        if pool_ratio > self.oracle_ratio:
            self._Gwei_to_GAS(pool)
        elif pool_ratio < self.oracle_ratio:
            self._GAS_to_Gwei(pool)


if __name__ == "__main__":
    from uniswap import Uniswap

    import random

    """init"""
    us = Uniswap('-1', 100000, 20000000)  # 1:200
    us.print_pool_state(bool_LT=True)

    """Providing Liquidity"""
    print(us.join('0', 2000, 400001))
    us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(10000):
        # if random.random() < 0.5:
        #     us.Gwei_to_GAS(2)
        # else:
        #     us.GAS_to_Gwei_exact(2)
        us.Gwei_to_GAS(2)

    us.print_pool_state(bool_LT=False)

    """Removing Liquidity"""
    print(us.out('0', 20000))  # The LT holder takes extra fees
    us.print_pool_state(bool_LT=True)

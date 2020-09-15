from math import floor


class Arbitrager:
    def __init__(self,
                 balance_GAS,
                 oracle_ratio):

        self.balance_GAS = balance_GAS      # total value (Gwei + GAS)  # [GAS]
        self.oracle_ratio = oracle_ratio    # GAS / Gwei

        """Params"""
        self.tx_fee = {
            "Gwei2GAS": 46000,
            "GAS2Gwei": 60000,
            "default": 21000}

    def update(self, oracle_ratio):
        self.oracle_ratio = oracle_ratio

    """Balance"""

    def get_balance_Gwei(self):
        return self.balance_GAS / self.oracle_ratio

    def get_balance_GAS(self):
        return self.balance_GAS

    def update_balance_Gwei(self, amount_Gwei):
        if self.balance_GAS + (amount_Gwei * self.oracle_ratio) >= 0:
            self.balance_GAS += amount_Gwei * self.oracle_ratio
        else:
            raise Exception("invalid amount.")

    def update_balance_GAS(self, amount_GAS):
        if self.balance_GAS + amount_GAS >= 0:
            self.balance_GAS += amount_GAS
        else:
            raise Exception("invalid amount.")

    """Arbitraging"""

    # TODO: sell (liquidity providing)

    # def _sell_Gwei(self, pool):
    #     pass

    # def _sell_GAS(self, pool):
    #     pass

    def _buy_Gwei(self, pool):
        pass

    def _buy_GAS(self, pool):

        # TODO: cal. N
        N = 4000000  # > 85896
        N_Eth = N / self.oracle_ratio

        # Maximize gain
        delta_GAS = pool.Gwei_to_GAS(N_Eth, bool_update=False)
        gain = delta_GAS - N - self.tx_fee["Gwei2GAS"]
        print(">>> gain:", gain)

        # Buy GAS
        pool.Gwei_to_GAS(N_Eth, bool_update=True)
        self.update_balance_GAS(gain)

    def arbitrage(self, pool):
        current_Gwei, current_GAS = pool.Gwei, pool.GAS
        pool_ratio = float(current_GAS / current_Gwei)

        if pool_ratio > self.oracle_ratio:
            print("buy GAS")
            # self._sell_Gwei(pool)
            self._buy_GAS(pool)

        elif pool_ratio < self.oracle_ratio:
            print("buy Gwei")
            # self._sell_GAS(pool)
            self._buy_Gwei(pool)


if __name__ == "__main__":
    from uniswap import Uniswap

    import random

    # Arbitrager
    arbitrager = Arbitrager(1000000000, 200)

    """init"""
    us = Uniswap('-1', 100000, 20000000, 1000000)  # 1:200
    # us.print_pool_state(bool_LT=True)

    """Providing Liquidity"""
    us.join('0', 2000, 400001)
    # us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1):
        # TODO: N users
        if random.random() < 0.0:
            us.Gwei_to_GAS(20000)
        else:
            us.GAS_to_Gwei_exact(20000)

        print(us.Gwei, '\t', us.GAS, '\t', float(us.GAS / us.Gwei))
        arbitrager.arbitrage(us)
        print(us.Gwei, '\t', us.GAS, '\t', float(us.GAS / us.Gwei))

    # us.print_pool_state(bool_LT=False)

    """Removing Liquidity"""
    us.out('0', 20000)  # The LT holder takes extra fees
    # us.print_pool_state(bool_LT=True)

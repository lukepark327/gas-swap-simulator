from math import floor, sqrt


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

    def _best_number(self, X, Y, fee, unit):
        gamma = (1. - fee)
        N = floor(  # TODO: floor or ceil
            (sqrt(Y) * sqrt(gamma) * sqrt(X) / sqrt(unit) - X) / (gamma))
        return N

    def _buy_Gwei(self, pool):
        # Calculating the best N_GAS which maximize `gain`
        N_GAS = self._best_number(pool.GAS, pool.Gwei, pool.fee, (1. / self.oracle_ratio))

        # Buy Gwei
        delta_Gwei = pool.GAS_to_Gwei(N_GAS, bool_update=False)
        gain = delta_Gwei * self.oracle_ratio - N_GAS - self.tx_fee["GAS2Gwei"]  # profit - loss - fee

        if gain <= 0:
            pass
        else:
            self.update_balance_GAS(gain)
            pool.GAS_to_Gwei(N_GAS, bool_update=True)

    def _buy_GAS(self, pool):
        # Calculating the best N_Gwei which maximize `gain`
        N_Gwei = self._best_number(pool.Gwei, pool.GAS, pool.fee, self.oracle_ratio)

        # Buy GAS
        delta_GAS = pool.Gwei_to_GAS(N_Gwei, bool_update=False)
        gain = delta_GAS - N_Gwei * self.oracle_ratio - self.tx_fee["Gwei2GAS"]  # profit - loss - fee

        if gain <= 0:
            pass
        else:
            self.update_balance_GAS(gain)
            pool.Gwei_to_GAS(N_Gwei, bool_update=True)

    def arbitrage(self, pool):
        current_Gwei, current_GAS = pool.Gwei, pool.GAS
        pool_ratio = float(current_GAS / current_Gwei)

        if pool_ratio > self.oracle_ratio:
            # self._sell_Gwei(pool)
            self._buy_GAS(pool)

        elif pool_ratio < self.oracle_ratio:
            # self._sell_GAS(pool)
            self._buy_Gwei(pool)


if __name__ == "__main__":
    from uniswap import Uniswap

    import random
    import matplotlib.pyplot as plt

    random.seed(12345)

    # Arbitrager
    arbitrager = Arbitrager(1000000000, 200)
    balances = []

    """init"""
    us = Uniswap('-1', 100000, 20000000, 1000000)  # 1:200
    us.print_pool_state(bool_LT=True)

    """Providing Liquidity"""
    us.join('0', 2000, 400001)
    us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000):
        if random.random() < 0.5:
            us.Gwei_to_GAS(1000)
        else:
            us.GAS_to_Gwei_exact(1000)

        # print(us.Gwei, '\t', us.GAS, '\t', float(us.GAS / us.Gwei), '\t', arbitrager.balance_GAS)
        arbitrager.arbitrage(us)
        # print(us.Gwei, '\t', us.GAS, '\t', float(us.GAS / us.Gwei), '\t', arbitrager.balance_GAS)
        # print()
        balances.append(arbitrager.balance_GAS)

    # us.print_pool_state(bool_LT=False)

    """Removing Liquidity"""
    us.out('0', 20000)  # The LT holder takes extra fees
    us.print_pool_state(bool_LT=True)

    """Plot"""
    plt.plot(balances)
    plt.xlabel('round')
    plt.ylabel('balance')
    plt.show()

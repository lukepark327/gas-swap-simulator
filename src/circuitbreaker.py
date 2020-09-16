from math import floor

from uniswap import Uniswap


"""Circuit Breaker
# Algorithmical Arbitrager
# Protocol
# Run at critical moment(s)
"""
class Uniswap_with_CB(Uniswap):
    def __init__(self,
                 address,
                 amount_Gwei,       # ex) (1.) * n
                 amount_GAS,        # ex) (200. ~= 199.5) * n
                 init_LT,
                 fee=0.003,         # 0.3%
                 CB_mode="swap",    # "swap", "pause", "nothing"
                 threshold=0.05     # 5%
                 ):

        self.Gwei, self.GAS, self.LT = amount_Gwei, amount_GAS, init_LT
        self.k = self.Gwei * self.GAS  # constant product
        self.fee = fee

        self.LT_holders = {}
        self.LT_holders[address] = init_LT

        self.CB_mode = CB_mode
        self.threshold = threshold

        """Logging"""
        self.low, self.high, self.normal = 0, 0, 0

    """Circuit Breaker"""

    # def set_threshold(self, threshold):
    #     self.threshold = threshold

    def _swap_GAS_to_Gwei(self, oracle_ratio, pool_ratio):
        # Burn GAS & Mint ETH(Gwei)
        delta_Gwei = floor((self.GAS - self.Gwei * oracle_ratio) / (oracle_ratio + pool_ratio))
        Gwei_prime = self.Gwei + delta_Gwei
        GAS_prime = floor(self.GAS - delta_Gwei * pool_ratio)

        self._update(Gwei_prime, GAS_prime)

    def _swap_Gwei_to_GAS(self, oracle_ratio, pool_ratio):
        # Burn ETH(Gwei) & Mint GAS
        delta_Gwei = floor((self.Gwei * oracle_ratio - self.GAS) / (oracle_ratio + pool_ratio))
        Gwei_prime = self.Gwei - delta_Gwei
        GAS_prime = floor(self.GAS + delta_Gwei * pool_ratio)

        self._update(Gwei_prime, GAS_prime)

    def _cb_swap(self, oracle_ratio, pool_ratio):
        if pool_ratio > oracle_ratio:
            self._swap_GAS_to_Gwei(oracle_ratio, pool_ratio)
        elif pool_ratio < oracle_ratio:
            self._swap_Gwei_to_GAS(oracle_ratio, pool_ratio)

        return

    def _cb_pause(self):
        return

    def _cb_nothing(self):
        return

    def _cb(self, oracle_ratio, pool_ratio):
        if self.CB_mode == "swap":
            return self._cb_swap(oracle_ratio, pool_ratio)
        elif self.CB_mode == "pause":
            return self._cb_pause()
        else:  # nothing
            return self._cb_nothing()

    def circuit_break(self, oracle_ratio):
        pool_ratio = float(self.GAS / self.Gwei)

        # TODO: Dynamic Circuit Breaker (DCB)
        if (pool_ratio * (1. - self.threshold) >= oracle_ratio):
            # print("pool_ratio is too high")
            self.high += 1
            self._cb(oracle_ratio, pool_ratio)
        elif (pool_ratio * (1. + self.threshold) <= oracle_ratio):
            # print("pool_ratio is too low")
            self.low += 1
            self._cb(oracle_ratio, pool_ratio)
        else:
            # print("no problem")
            self.normal += 1
            pass


if __name__ == "__main__":
    import random

    random.seed(12345)
    # random.seed(950327)

    """init"""
    us = Uniswap_with_CB('-1', 100000, 20000000, 1000000,
                         CB_mode="swap", threshold=0.05)  # 1:200
    us.print_pool_state(bool_LT=True)

    """Providing Liquidity"""
    print(us.join('0', 2000, 400001))
    us.print_pool_state(bool_LT=True)
    us.circuit_break(oracle_ratio=200.)

    """Txs"""
    for _ in range(100000):
        if random.random() < 0.5:
            us.Gwei_to_GAS(10)
        else:
            us.GAS_to_Gwei_exact(10)
        us.circuit_break(oracle_ratio=200.)
    us.print_pool_state(bool_LT=False)
    print(us.low, us.high, us.normal)

    """Removing Liquidity"""
    print(us.out('0', 20000))  # The LT holder takes extra fees
    us.print_pool_state(bool_LT=True)

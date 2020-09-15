from math import floor, ceil  # for quantization
from pprint import pprint


class Uniswap:  # between Eth and Gas
    def __init__(self,
                 address,
                 amount_Gwei,   # ex) (1.) * n
                 amount_GAS,    # ex) (200. ~= 199.5) * n
                 init_LT=1000000,
                 fee=0.003      # 0.3%
                 ):

        self.Gwei, self.GAS, self.LT = amount_Gwei, amount_GAS, init_LT
        self.k = self.Gwei * self.GAS  # constant product
        self.fee = fee

        self.LT_holders = {}
        self.LT_holders[address] = init_LT

    def _update(self, Gwei_prime, GAS_prime, LT_prime=None):
        if LT_prime is not None:
            self.LT = LT_prime
        self.Gwei, self.GAS = Gwei_prime, GAS_prime
        self.k = self.Gwei * self.GAS

    """Swap Protocol"""

    def _get_input_price(self, delta_X, X, Y, bool_fee=True):
        # Validity check
        if (X == 0) or (Y == 0):
            raise Exception("invalid X: {} or Y: {}".format(X, Y))

        alpha = float(delta_X / X)
        gamma = (1. - self.fee) if bool_fee else (1.)

        delta_Y = floor(alpha * gamma / (1. + alpha * gamma) * Y)

        # Validity check
        if delta_Y >= Y:
            raise Exception("invalid delta_Y. {} >= {}".format(delta_Y, Y))

        return delta_Y

    def _get_output_price(self, delta_Y, Y, X, bool_fee=True):
        # Validity check
        if (X == 0) or (Y == 0):
            raise Exception("invalid X: {} or Y: {}".format(X, Y))
        if delta_Y >= Y:
            raise Exception("invalid delta_Y. {} >= {}".format(delta_Y, Y))

        beta = float(delta_Y / Y)
        gamma = (1. - self.fee) if bool_fee else (1.)

        delta_X = floor(beta / ((1. - beta) * gamma) * X) + 1
        return delta_X

    def Gwei_to_GAS(self, delta_Gwei, bool_fee=True, bool_update=True):
        Gwei_prime = self.Gwei + delta_Gwei
        delta_GAS = self._get_input_price(delta_Gwei, self.Gwei, self.GAS, bool_fee=bool_fee)
        GAS_prime = self.GAS - delta_GAS

        if bool_update:
            self._update(Gwei_prime, GAS_prime)  # Pool update
        return delta_GAS

    def Gwei_to_GAS_exact(self, delta_GAS, bool_fee=True, bool_update=True):
        delta_Gwei = self._get_output_price(delta_GAS, self.GAS, self.Gwei, bool_fee=bool_fee)
        Gwei_prime = self.Gwei + delta_Gwei
        GAS_prime = self.GAS - delta_GAS

        if bool_update:
            self._update(Gwei_prime, GAS_prime)  # Pool update
        return delta_Gwei

    def GAS_to_Gwei(self, delta_GAS, bool_fee=True, bool_update=True):
        GAS_prime = self.GAS + delta_GAS
        delta_Gwei = self._get_input_price(delta_GAS, self.GAS, self.Gwei, bool_fee=bool_fee)
        Gwei_prime = self.Gwei - delta_Gwei

        if bool_update:
            self._update(Gwei_prime, GAS_prime)  # Pool update
        return delta_Gwei

    def GAS_to_Gwei_exact(self, delta_Gwei, bool_fee=True, bool_update=True):
        delta_GAS = self._get_output_price(delta_Gwei, self.Gwei, self.GAS, bool_fee=bool_fee)
        GAS_prime = self.GAS + delta_GAS
        Gwei_prime = self.Gwei - delta_Gwei

        if bool_update:
            self._update(Gwei_prime, GAS_prime)  # Pool update
        return delta_GAS

    """Liquidity Protocol"""

    def required_GAS_for_liquidity(self, delta_Gwei):
        alpha = float(delta_Gwei / self.Gwei)

        GAS_prime = floor((1. + alpha) * self.GAS) + 1
        return GAS_prime - self.GAS

    def join(self, address, delta_Gwei, delta_GAS):
        # delta_GAS validity check
        current_required_GAS_for_liquidity = self.required_GAS_for_liquidity(delta_Gwei)
        if current_required_GAS_for_liquidity != delta_GAS:
            raise Exception("invalid delta_GAS. Require {} GAS but input is {}".format(
                current_required_GAS_for_liquidity, delta_GAS))

        delta_LT = self._mint(delta_Gwei, delta_GAS)
        if address in self.LT_holders.keys():
            self.LT_holders[address] += delta_LT
        else:
            self.LT_holders[address] = delta_LT

        return delta_LT

    def out(self, address, delta_LT):
        # Ownership validity check
        if address not in self.LT_holders.keys():
            raise Exception("invalid address")

        # delta_LT validity check
        if self.LT_holders[address] < delta_LT:
            raise Exception("invalid delta_LT. Have to be under {} LT but input is {}".format(
                self.LT_holders[address], delta_LT))

        delta_Gwei, delta_GAS = self._burn(delta_LT)
        self.LT_holders[address] -= delta_LT
        if self.LT_holders[address] == 0:
            del self.LT_holders[address]

        return delta_Gwei, delta_GAS

    def _mint(self, delta_Gwei, delta_GAS):  # add_liquidity
        alpha = float(delta_Gwei / self.Gwei)

        Gwei_prime = self.Gwei + delta_Gwei
        GAS_prime = floor((1. + alpha) * self.GAS) + 1
        LT_prime = floor((1. + alpha) * self.LT)
        delta_LT = LT_prime - self.LT

        self._update(Gwei_prime, GAS_prime, LT_prime)  # Pool update
        return delta_LT

    def _burn(self, delta_LT):  # remove_liquidity
        alpha = float(delta_LT / self.LT)

        Gwei_prime = ceil((1. - alpha) * self.Gwei)
        GAS_prime = ceil((1. - alpha) * self.GAS)
        LT_prime = self.LT - delta_LT
        delta_Gwei = self.Gwei - Gwei_prime
        delta_GAS = self.GAS - GAS_prime

        self._update(Gwei_prime, GAS_prime, LT_prime)  # burn LT
        return delta_Gwei, delta_GAS

    """Logging"""

    def print_pool_state(self, bool_LT=False):
        print("Gwei\t\tGAS\t\tk\t\tLT")
        print("{}\t\t{}\t{}\t{}".format(
            self.Gwei, self.GAS, self.k, self.LT))
        if bool_LT:
            pprint(self.LT_holders)
        print('\n')


if __name__ == "__main__":
    import random

    """init"""
    us = Uniswap('-1', 100000, 20000000)  # 1:200
    us.print_pool_state(bool_LT=True)

    """Providing Liquidity"""
    print(us.join('0', 2000, 400001))
    us.print_pool_state(bool_LT=True)

    """Txs"""
    for _ in range(1000000):
        if random.random() < 0.5:
            us.Gwei_to_GAS(2)
        else:
            us.GAS_to_Gwei_exact(2)
    us.print_pool_state(bool_LT=False)

    """Removing Liquidity"""
    print(us.out('0', 20000))  # The LT holder takes extra fees
    us.print_pool_state(bool_LT=True)

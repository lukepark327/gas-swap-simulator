# Calculating fee(s)
def _cal_fee(price, gas_limit):
    return price * gas_limit


# Total cost
def cost(amount, price, gas_limit):
    fee = _cal_fee(price, gas_limit)
    return amount + fee


if __name__ == "__main__":
    gas_default = 21000

    pass

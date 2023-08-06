def sum(*values_sum):
    result_sum = 0
    for value_sum in values_sum:
        result_sum += value_sum
    return result_sum


def sub(*values_sub):
    result_sub = 0
    for value_sub in values_sub:
        result_sub -= value_sub
    return result_sub


def mul(*values_mul):
    result_mul = 1
    for value_mul in values_mul:
        result_mul *= value_mul
    return result_mul


def div(numerator, denominator):
    return numerator / denominator

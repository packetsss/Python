print(3 ** 2)


def pwr(base, pow):
    result = 1
    for index in range(pow):
        result = result * base
    return result


print(pwr(2, 9))

#!/usr/bin/env python3

import matplotlib.pyplot as plt


def populate(data, current_sum, depth):
    values = list(range(1, 7))
    for value in values:
        if depth == 0:
            final_sum = current_sum + value
            if not final_sum in data:
                data[final_sum] = 0
            data[final_sum] += 1
        else:
            populate(data, current_sum + value, depth - 1)


def generate_data(n_dice, offset=0):

    combos = {}
    populate(combos, offset, n_dice-1)

    total_combo = float(sum(combos.values()))

    data = [[], []]
    for value in combos:
        data[0].append(value)
        data[1].append(combos[value]/total_combo)

    return data


def main():
    data = generate_data(3)
    s = 0
    for i in range(len(data[0])):
        value = 100*data[1][i]
        s += value
        print("{0:>2}: {1: 2.02f}%\t{2:.02f}".format(
            data[0][i],
            value,
            s))

    # plt.bar(data[0], data[1])
    # plt.show()


if __name__ == "__main__":
    main()
data_a = {}

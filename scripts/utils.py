import copy


def remove_whitespace(value):
    value = value.replace("\n", " ")\
        .replace("\r", " ")\
        .replace("\t", " ")

    while True:
        old_len = len(value)
        value = value.replace("  ", " ")
        if old_len == len(value):
            break

    return value.strip()


class Median(object):

    def __init__(self):
        self.data = []

    def add(self, value):
        self.data.append(value)

    def calc(self):
        if not self.data:
            return 0

        self.data.sort()

        index = int(round(len(self.data)/2.0))

        return self.data[index]


class Average(object):
    def __init__(self):
        self.sum = 0
        self.count = 0

    def add(self, value):
        self.sum += value
        self.count += 1

    def calc(self):
        return self.sum / self.count if self.count > 0 else 0

    def __str__(self):
        state = copy.deepcopy(self.__dict__)
        state["value"] = self.calc()
        return "{}".format(state)


def __permutate__(metric, count, total=0):
    for i in range(6):
        if count == 1:
            metric.add(total+i+1)
        else:
            __permutate__(metric, count-1,  total+i+1)


def avg_dmg(dice_count, offset=0, mult=1):
    a = Average()
    #a = Median()
    __permutate__(a, dice_count)
    return (a.calc()+offset)*mult


def analyze_damages():

    data = []

    dice_count = 5
    max_mult = 3

    for m in range(1, max_mult+1):
        for d in range(dice_count):
            key = ""
            if m == 1:
                key = str(d+1) + "d"
            else:
                key = "{}dx{}".format(d+1, m)
            data.append((key, avg_dmg(d+1, 0, m)))

    for o in range(-2, 3):
        for d in range(dice_count):
            key = str(d+1)+"d"
            if o < 0:
                key += str(o)
            elif o > 0:
                key += "+" + str(o)

            data.append((key, avg_dmg(d+1, o)))

    data.sort(key=lambda tup: tup[1])

    for item in data:
        print("{:>4}: {}".format(item[0], item[1]))


if __name__ == "__main__":
    analyze_damages()

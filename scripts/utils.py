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


def __get_avg__(count, av=Average(), total=0):

    for i in range(6):
        if count == 1:
            av.add(total+i+1)
        else:
            __get_avg__(count-1, av, total+i+1)

    return av


def avg_dmg(dice_count, offset=0, mult=1):

    a = __get_avg__(dice_count)
    return (a.calc()+offset)*mult


if __name__ == "__main__":
    print(avg_dmg(3))

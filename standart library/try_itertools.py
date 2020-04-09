from itertools import groupby


def sorted_runs(xs):
    indexes = range(len(xs) - 1)

    def is_increasing(idx):
        print(idx)
        return xs[idx] < xs[idx + 1]

    return groupby(indexes, is_increasing)


xs = [1, 2, 3, 5, 2, 0, 3, 1]

for inc, group in sorted_runs(xs):
    print(inc)
    print(
        '<' if inc else '>',
        ','.join(map(str, group)),
    )


def gen():
    for i in range(10):
        x = yield i
        print(x, 'gen')


g = gen()
# print(next(g), 'next')
print(g.send(None), 'send')
# print(g.send(72), 'send')
# print(g.send(88), 'send')
# print(next(g),'next')
# print(g.send(72), 'send')

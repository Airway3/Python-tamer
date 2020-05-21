from collections import deque
from functools import lru_cache


# ================================= 1 ===================================
# =============================== iter ==================================


# n = int(input())
# tree = [int(s) for s in input().split()]
tree = [int(s) for s in '9 7 5 5 2 9 9 9 2 -1'.split()]

graph = {}

for index, t in enumerate(tree):
    graph.setdefault(index, set())
    graph.setdefault(t, set()).add(index)


def get_h(n):
    h = 0
    q = deque()

    q.append(n)
    q.append(None)

    while q:
        n = q.popleft()

        if n is None:
            if q:
                q.append(None)

            h += 1
        else:
            for c in graph[n]:
                q.append(c)

    return h


if not graph:
    print(0)
else:
    print(get_h(-1))


# ================================= 2 ===================================
# =============================== recu ==================================


@lru_cache(maxsize=None)
def count(data, i):
    return (data[i] == -1 and 1 or count(data, data[i]) + 1)


num, data = int(input()), tuple(int(i) for i in input().split())
print(max(count(data, i) for i in range(num)))

import sys
from collections import deque, OrderedDict


# ================================= 1 ===================================
# =============================== sequ ==================================

# size, n = 7, 25
size, n = (int(i) for i in input().split())
packages = OrderedDict()
prev_ts = None

# for p in [i.split() for i in open('net_packages_input.txt')]:
for p in [input().split() for i in range(n)]:
    if prev_ts is None:
        prev_ts = int(p[0])
    packages.setdefault(int(p[0]), []).append(int(p[1]))


if n > 0:
    q = deque()
    timeline = prev_ts

    def arrive(ts):
        for duration in packages[ts]:
            if len(q) < size:
                if duration > 0 or duration == 0 and q:
                    q.append(duration)

                global timeline
                timeline = max(timeline, ts)
                print(timeline)
                timeline += duration
            else:
                print(-1)


    def process(diff):
        for i in range(len(q)):
            p = q.popleft()
            rest = p - diff

            if rest > 0:
                p -= diff
                q.appendleft(p)
                break
            else:
                diff = abs(rest)


    for ts in packages:
        if q:
            diff = ts - prev_ts
            process(diff)

        arrive(ts)
        prev_ts = ts


# ================================= 2 ===================================
# =============================== lazy ==================================
queue = deque()
size, count = map(int, input().split())
for arrival, duration in (map(int, input().split()) for _ in range(count)):
    while queue and queue[0] <= arrival:
        queue.popleft()

    if len(queue) >= size:
        print(-1)
    else:
        start = queue[-1] if queue else arrival
        queue.append(start + duration)
        print(start)


# ================================= 3 ===================================
# =============================== lazy ==================================
reader = (map(int, s.split()) for s in sys.stdin)
size, n = next(reader)
times = deque()
for a, d in reader:
    while times and times[0] <= a:
        times.popleft()

    if len(times) < size:
        if times:
            a = max(a, times[-1])
        print(a)
        times.append(a + d)
    else:
        print(-1)

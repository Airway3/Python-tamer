'''
Counter словарь счётчик
OrderedDict упорядоченный словарь

'''

import collections

c = collections.Counter()

for word in ['spam', 'egg', 'spam', 'counter', 'counter', 'counter']:
    c[word] += 1
print(c)

print(collections.Counter('abracadabra').most_common(3))

dc = {}
for word in ['spam', 'egg', 'spam', 'counter', 'counter', 'counter']:
    if word not in dc:
        dc[word] = 0
    dc[word] += 1
print(dc)


def firstfu():
    print('firstfu')

print(callable(firstfu))
print(callable(dc))
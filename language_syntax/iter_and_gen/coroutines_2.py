

"""
Делегирующий генератор - вызывающий другой (подгенератор).
"""


def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class CustomException(Exception):
    pass


def subgen():
    for i in 'Alligator':
        yield i


def delegator(g):
    for i in g:
        yield i


sg = subgen()
d = delegator(sg)

for i in d:
    print(i)


print('=' * 100)


@coroutine
def subgen2():
    while True:
        try:
            print('subgen')
            message = yield
        except CustomException:
            print('Kaboom')
        else:
            print('........', message)


@coroutine
def delegator2(g):
    while True:
        try:
            print('delegator')
            data = yield
            g.send(data)
        except CustomException as e:
            g.throw(e)


sg = subgen2()
d = delegator2(sg)

print('after coroutine init')
d.send('OK')
d.throw(CustomException)


print('=' * 100)


def subgen3():
    while True:
        try:
            print('subgen')
            message = yield
        except CustomException:
            print('Kaboom')
        else:
            print('........', message)


@coroutine
def delegator3(g):
    yield from g  # содержит в себе инициализацию генератора, поэтому не нужен декоратор в subgen2


sg = subgen3()
d = delegator3(sg)  # здесь же отработает первый send(None) у subgen3

print('after coroutine init')
d.send('OK')
d.throw(CustomException)


print('=' * 100)


def subgen4():
    while True:
        try:
            print('subgen')
            message = yield
        except CustomException:
            print('Kaboom')
            # break
        else:
            print('........', message)

    # return 'subgen result'


@coroutine
def delegator4(g):
    result = yield from g  # ждём пока генератор завершит свою работу - await
    print(result)


sg = subgen4()
d = delegator4(sg)

print('after coroutine init')
d.send('OK')
print(d.throw(CustomException))
print(d.throw(CustomException))
print(d.send('finish'))


print('=' * 100)


@coroutine
def alligator():
    yield from 'Alligator'


a = alligator()
for e in a:
    print(e)

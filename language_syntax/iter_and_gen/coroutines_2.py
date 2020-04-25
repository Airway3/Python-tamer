

"""
Делегирующий генератор - вызывающий другой (подгенератор).
"""


def init_gen(func):
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


@init_gen
def subgen2():
    while True:
        try:
            print('subgen')
            message = yield
        except CustomException:
            print('Kaboom')
        else:
            print('........', message)


@init_gen
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

print('after init_gen inner call')
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


@init_gen
def delegator3(g):
    yield from g  # содержит в себе инициализацию генератора, поэтому не нужен декоратор в subgen3


sg = subgen3()
d = delegator3(sg)  # здесь же отработает первый send(None) у subgen3

print('after init_gen inner call')
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


@init_gen
def delegator4(g):
    result = yield from g  # ждём пока генератор завершит свою работу - await
    print(result)


sg = subgen4()
d = delegator4(sg)

print('after init_gen inner call')
d.send('OK')
print(d.throw(CustomException))
print(d.throw(CustomException))
print(d.send('finish'))


print('=' * 100)


@init_gen
def alligator():
    yield from 'Alligator'


a = alligator()
for e in a:
    print(e)

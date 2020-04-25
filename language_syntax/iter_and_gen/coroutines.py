from inspect import getgeneratorstate


"""
Корутины - генераторы которые могут получать данные. через метод send.
Является средством обеспечения «легковесной» программной многопоточности в том смысле, 
что могут быть реализованы без использования механизмов переключений контекста операционной системы.

В моём понимании корутина - генератор который вызывает другой генератор.

Первый раз нужно передавать None. Это обязательное действие. Можно первый раз использовать next вместо send(None).
"""


def subgen():
    message = yield
    print('Subgen received:', message)


g = subgen()

print(getgeneratorstate(g))
# print(next(g))  # или send
print(g.send(None))  # генератор отрабатывает до первого yield
print(getgeneratorstate(g))
# print(g.send('OK'))

print('=' * 100)


def subgen2():
    x = 'Ready to accept message'
    message = yield x
    print('Subgen received:', message)


g = subgen2()

print(g.send(None))
# print(g.send('OK'))  # return 'Ready to accept message'

print('=' * 100)


def init_gen(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class CustomException(Exception):
    pass


@init_gen
def average():
    count = 0
    summ = 0
    result = None

    while True:
        try:
            x = yield result
        except StopIteration:
            print('Done')
            # break
        except CustomException:
            print('CustomException')
            # break
        else:
            count += 1
            summ += x
            result = round(summ / count, 2)

    return result


g = average()
print(getgeneratorstate(g))
print(g.send(4))
print(g.send(5))
print(g.send(10))
print(g.throw(CustomException))
print(g.send(10))
print(g.throw(StopIteration))
# try:
#     g.throw(CustomException)
#     g.throw(StopIteration)  # or this
# except StopIteration as e:
#     print('Average', e.value)
print(g.send(10))
print(g.send(10))

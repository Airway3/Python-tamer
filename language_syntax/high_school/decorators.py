import sys
import time
import functools
import warnings


# print utils
def get_stars_count(title, line_length=80):
    return line_length - title.__len__()


def block_title(title):
    print()
    stars = get_stars_count(title) // 2

    if title.__len__() % 2 == 0:
        print(stars * '-', title, stars * '-')
    else:
        print(stars * '-', title, (stars + 1) * '-')


def example_title(title):
    print((get_stars_count(title) // 2 * '-'), title)


# Декоратор сам по себе является вызываемым объектом, который возвращает вызываемый объект.

block_title('Декорирование функций и методов')


def decorator(f): # f – функция или метод, не связанный с экземпляром
    def wrapper(*args): # для методов - экземпляр класса в args[0]
        print('class instance', args[0])
        f(*args) # вызов функции или метода
    return wrapper


@decorator
def _sum(x, y):  # _sum = decorator(_sum)
    print(x + y)


_sum(8, 4)  # в действительности вызывает wrapper(8, 4)


class C:
    @decorator
    def method(self, x, y):  # method = decorator(method)
        print('call class method')


c = C()
c.method(9, 3)  # вызывает wrapper(c, 9, 3)

'''
Декорирование класса
C = decorator(C)
т.е. результат функции декоратора присвоится имени класса

@decorator
class C:
    ...

x = C(99)
Фактически вызовет decorator(C)(99)

Суть заключается в том, что позднее, при вызове имени класса, для создания экземпляра вместо оригинального класса будет вызван вызываемый объект,
возвращенный декоратором.
'''

block_title('Декорирование класса')


def class_decorator(class_X):
    # Обработать класс X
    return class_X # вернуть его


@class_decorator # C = class_decorator(C)
class C:
    pass


def getattr_decorator(cls):  # Вызывается на этапе декорирования @
    """ добавляет в объект обработку операций обращения к неопределенным атрибутам """
    class Wrapper:
        def __init__(self, *args):  # На этапе создании экземпляра
            self.wrapped = cls(*args)

        def __getattr__(self, name):  # Вызывается при обращении к атрибуту
            return getattr(self.wrapped, name)

    return Wrapper


@getattr_decorator
class K:  # K = getattr_decorator(K)
    def __init__(self, x, y):  # Вызывается методом Wrapper.__init__
        self.attr = x * 'spam ' + str(y)


x = K(6, 7)  # В действительности вызовет Wrapper(6, 7)
print(x)
print(x.attr) # Вызовет Wrapper.__getattr__, выведет “spam”

block_title('Декорирование функции')
example_title('tracer for funcs')


class tracer:
    def __init__(self, func):
        self.calls = 0
        self.func = func
        print('tracer init')

    def __call__(self, *args):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)


@tracer
def spam(a, b, c):
    print(a + b + c)


a = spam(7, 8, 9)  # spam = tracer(spam)(7, 8, 9) экземпляр трейсера создаётся с функцией спам в конструкторе
                   # и вызывается с передаваемыми в call числами
b = spam(6, 2, 4)  # это уже вызов созданного выше экземпляра, т.е. просто call, перезаписали переменную spam
print(id(a), id(b), a is b)
print(spam.func)  # в паяти спам это экземпляр трейсера, а функция спам в атрибуте
# если обернуть трейсером другую функцию то будет новый экземпляр со своими атрибутами calls и тд


example_title('tracer for funcs and methods')


# BEST CHOICE
def tracer(func):  # Вместо класса с методом __call__ используется функция,
    calls = 0      # иначе “self” будет представлять экземпляр декоратора!

    def on_call(*args, **kwargs):
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return on_call


# Может применяться к простым функциям
@tracer
def spam(a, b, c):  # spam = tracer(spam)
    print(a + b + c)  # onCall сохранит ссылку на spam


spam(1, 2, 3)  # Вызовет on_call(1, 2, 3)
spam(a=4, b=5, c=6)


# Может применяться к методам классов!
class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer
    def giveRaise(self, percent):  # giveRaise = tracer(giverRaise)
        self.pay *= (1.0 + percent)  # on_call сохранит ссылку на giveRaise

    @tracer
    def lastName(self):  # lastName = tracer(lastName)
        return self.name.split()[-1]


print('methods...')
bob = Person('Bob Smith', 50000)
sue = Person('Sue Jones', 100000)
print(bob.name, sue.name)
sue.giveRaise(.10)  # Выховет on_call(sue, .10)
print(sue.pay)
print(bob.lastName(), sue.lastName())  # Вызовет on_call(bob), lastName – в области видимости объемлющей функции


example_title('with descriptors')


class tracer(object):
    """ класс мозгокрут """
    def __init__(self, func):  # На этапе декорирования @
        self.calls = 0         # Сохраняет функцию для последующего вызова
        self.func = func

    def __call__(self, *args, **kwargs):  # Вызывается при обращениях к оригинальной функции
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):  # Вызывается при обращении к атрибуту
        return Wrapper(self, instance)


class Wrapper:
    def __init__(self, desc, subj):  # Сохраняет оба экземпляра
        self.desc = desc  # Делегирует вызов дескриптору
        self.subj = subj  # Person instance

    def __call__(self, *args, **kwargs):
        return self.desc(self.subj, *args, **kwargs)  # Вызовет tracer.__call__


@tracer
def spam(a, b, c):  # spam = tracer(spam)
    pass  # Использует только __call__ класса tracer


class Person:
    @tracer  # Создаст дескриптор giveRaise
    def giveRaise(self, percent):  # giveRaise = tracer(giverRaise)
        pass


example_title('short example with descriptor')


# short, general func instead class Wrapper
class tracer(object):
    def __init__(self, func):  # На этапе декорирования @
        self.calls = 0  # Сохраняет функцию для последующего вызова
        self.func = func

    def __call__(self, *args, **kwargs):  # Вызывается при обращениях к
        self.calls += 1  # оригинальной функции
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):  # Вызывается при обращении к методу
        def wrapper(*args, **kwargs):  # Сохраняет оба экземпляра
            return self(instance, *args, **kwargs)  # Вызовет __call__ дескриптора
        return wrapper


@tracer
def spam(a, b, c): # spam = tracer(spam)
    pass # Использует только __call__


class Man:
    @tracer  # Создаст дескриптор giveRaise
    def giveRaise(self, percent):  # giveRaise = tracer(giverRaise)
        pass


block_title('Хронометраж вызовов')
example_title('время единственного вызова и накопленное время всех вызовов')


class timer:
    def __init__(self, func):
        self.func = func
        self.alltime = 0

    def __call__(self, *args, **kargs):
        start = time.perf_counter()
        result = self.func(*args, **kargs)
        elapsed = time.perf_counter() - start
        self.alltime += elapsed
        print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
        return result


@timer
def listcomp(n):
    return [x * 2 for x in range(n)]


@timer
def mapcall(n):
    return list(map((lambda x: x * 2), range(n)))  # не создавая список, оставив просто итератор, меп победит без конкуренции


listcomp(5)
listcomp(50000)
listcomp(500000)
listcomp(1000000)
print('allTime = %s' % listcomp.alltime)  # Общее время всех вызовов listcomp
print('')
mapcall(5)
mapcall(50000)
mapcall(500000)
mapcall(1000000)
print('allTime = %s' % mapcall.alltime)  # Общее время всех вызовов mapcall

print('map/comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))

example_title('добавление аргументов декоратора')


def timer(label='', trace=True):  # Аргументы декоратора: сохраняются
    class Timer:
        def __init__(self, func):  # На этапе декорирования сохраняется
            self.func = func  # декорируемая функция, ниже это timer_inst
            self.alltime = 0

        def __call__(self, *args, **kargs):  # При вызове: вызывается оригинал
            start = time.perf_counter()
            result = self.func(*args, **kargs)
            elapsed = time.perf_counter() - start
            self.alltime += elapsed
            if trace:
                format = '%s %s: %.5f, %.5f'
                values = (label, self.func.__name__, elapsed, self.alltime)
                print(format % values)
            return result
    return Timer


@timer(label='[CCC]==>')
def timer_inst(N):  # timer_inst = timer(label='[CCC]==>')(timer_inst)
    return [x * 2 for x in range(N)]

'''
Внешняя функция timer вызывается непосредственно перед операцией декорирования, она просто возвращает класс Timer, 
который будет играть роль фактического декоратора. В момент
декорирования создается экземпляр класса Timer, который запоминает саму
декорируемую функцию, но при этом ему остаются доступными аргументы декоратора, 
находящиеся в области видимости объемлющей функции.
'''
print(timer_inst)

#page 1117


block_title('Примеры декораторов с уроков CS')

DEBUG = True


def trace(stream=sys.stdout):
    def decorator(f):
        if not DEBUG:
            return f

        @functools.wraps(f)
        def inner(*args, **kwargs):
            call = ", ".join(
                [str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]
            )
            print(f"{f.__name__}({call}) = ...", file=stream)
            res = f(*args, **kwargs)
            print(f"{f.__name__}({call}) = {res}", file=stream)
            return res

        return inner
    return decorator


# возможность декорировать как с аргументами так и без
def trace(f=None, *, stream=sys.stdout):
    if f is None:
        return functools.partial(trace, stream=stream)

    if not DEBUG:
        return f

    @functools.wraps(f)
    def inner(*args, **kwargs):
        call = ", ".join(
            [str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]
        )
        print(f"{f.__name__}({call}) = ...", file=stream)
        res = f(*args, **kwargs)
        print(f"{f.__name__}({call}) = {res}", file=stream)
        return res

    return inner


# ======================================================================
def once(f):
    called = False

    @functools.wraps(f)
    def inner(*args, **kwargs):
        nonlocal called
        if not called:
            called = True
            res = f(*args, **kwargs)
            assert res is None

    return inner


@once
def try_once():
    print('once')


try_once()
try_once()


# ======================================================================
def deprecated(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        warnings.warn(f"{f.__name__} is deprecated", category=DeprecationWarning)
        return f(*args, **kwargs)

    return inner


# ======================================================================
def profile(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = f(*args, **kwargs)
        elapsed = time.perf_counter() - start

        inner.__n_calls__ += 1
        inner.__total_time__ += elapsed
        return res

    inner.__n_calls__ = 0
    inner.__total_time__ = 0
    return inner


@profile
def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


# ======================================================================
def memoize(f):
    cache = {}

    @functools.wraps(f)
    def inner(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return inner


@memoize
def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)

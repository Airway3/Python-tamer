def output(title):
    stars = (80 - title.__len__()) // 2
    if title.__len__() % 2 == 0:
        print(stars * '-', title, stars * '-')
    else:
        print(stars * '-', title, (stars + 1) * '-')

def example(title):
    print(((80 - title.__len__()) // 2 * '-'), title)

'''
Декоратор сам по себе является вызываемым объектом, который возвращает вызываемый объект.
'''

output('Декорирование функций и методов')

def decorator(F): # F – функция или метод, не связанный с экземпляром
    def wrapper(*args): # для методов - экземпляр класса в args[0]
        print('hui', args[0])
        F(*args) # вызов функции или метода
    return wrapper

@decorator
def shit(x, y): # shit = decorator(shit)
    print(x + y)

shit(8, 4) # в действительности вызывает wrapper(8, 4)

class C:
    @decorator
    def method(self, x, y): # method = decorator(method)
        print('hui into method')

c = C()
c.method(9, 3) # вызывает wrapper(c, 9, 3)

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

output('Декорирование класса')

def class_decorator(class_X):
    # Обработать класс X
    return class_X # вернуть его

@class_decorator # C = class_decorator(C)
class C:
    pass

# ---------------------------------ПРИМЕР-----------------------------------
# добавляет в объект обработку операций обращения к неопределенным атрибутам

def decorator_example(cls): # На этапе декорирования @
    class Wrapper:
        def __init__(self, *args): # На этапе создании экземпляра
            self.wrapped = cls(*args)
        def __getattr__(self, name): # Вызывается при обращении к атрибуту
            return getattr(self.wrapped, name)
    return Wrapper

@decorator_example
class K: # K = decorator(K)
    def __init__(self, x, y): # Вызывается методом Wrapper.__init__
        self.attr = x * 'spam '

x = K(6, 7) # В действительности вызовет Wrapper(6, 7)
print(x)
print(x.attr) # Вызовет Wrapper.__getattr__, выведет “spam”

output('Декорирование функции')
example('tracer for funcs')

class tracer:
    def __init__(self, func):
        self.calls = 0
        self.func = func
        print('chlen')
    def __call__(self, *args):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)

@tracer
def spam(a, b, c):
    print(a + b + c)

a = spam(7, 8, 9) # spam = tracer(spam)(7, 8, 9) экземпляр трейсера создаётся с функцией спам в конструкторе
                  # и вызывается с передаваемыми в call числами
b = spam(6, 2, 4) # это уже вызов созданного выше экземпляра, т.е. просто call, перезаписали переменную spam
print(id(a), id(b), a is b)
# ясен хуй что если обернуть трейсеров другую функцию то будет новый экземпляр со своими атрибутами calls и тд

example('tracer for funcs and methods')
# BEST CHOICE
def tracer(func): # Вместо класса с методом __call__ используется функция,
    calls = 0     # иначе “self” будет представлять экземпляр декоратора!
    def onCall(*args, **kwargs):
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return onCall

# Может применяться к простым функциям
@tracer
def spam(a, b, c): # spam = tracer(spam)
    print(a + b + c) # onCall сохранит ссылку на spam
spam(1, 2, 3) # Вызовет onCall(1, 2, 3)
spam(a=4, b=5, c=6)

# Может применяться к методам классов!
class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer
    def giveRaise(self, percent): # giveRaise = tracer(giverRaise)
        self.pay *= (1.0 + percent) # onCall сохранит ссылку на giveRaise

    @tracer
    def lastName(self): # lastName = tracer(lastName)
        return self.name.split()[-1]

print('methods...')
bob = Person('Bob Smith', 50000)
sue = Person('Sue Jones', 100000)
print(bob.name, sue.name)
sue.giveRaise(.10) # Выховет onCall(sue, .10)
print(sue.pay)
print(bob.lastName(), sue.lastName()) # Вызовет onCall(bob), lastName – в области видимости объемлющей функции

example('with descriptors')

class tracer(object):
    def __init__(self, func): # На этапе декорирования @
        self.calls = 0        # Сохраняет функцию для последующего вызова
        self.func = func
    def __call__(self, *args, **kwargs): # Вызывается при обращениях к оригинальной функции
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner): # Вызывается при обращении к атрибуту
        return Wrapper(self, instance)

class Wrapper:
    def __init__(self, desc, subj): # Сохраняет оба экземпляра
        self.desc = desc # Делегирует вызов дескриптору
        self.subj = subj
    def __call__(self, *args, **kwargs):
        return self.desc(self.subj, *args, **kwargs) # Вызовет tracer.__call__

@tracer
def spam(a, b, c): # spam = tracer(spam)
    pass # Использует только __call__

class Person:
    @tracer
    def giveRaise(self, percent): # giveRaise = tracer(giverRaise)
        pass # Создаст дескриптор giveRaise


example('short example with descriptor')

# short, general func instead class Wrapper
class tracer(object):
    def __init__(self, func): # На этапе декорирования @
        self.calls = 0 # Сохраняет функцию для последующего вызова
        self.func = func
    def __call__(self, *args, **kwargs): # Вызывается при обращениях к
        self.calls += 1 # оригинальной функции
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner): # Вызывается при обращении к методу
        def wrapper(*args, **kwargs): # Сохраняет оба экземпляра
            return self(instance, *args, **kwargs) # Вызовет __call__ дескриптора
        return wrapper

@tracer
def spam(a, b, c): # spam = tracer(spam)
    pass # Использует только __call__

class Valerka:
    @tracer
    def giveRaise(self, percent): # giveRaise = tracer(giverRaise)
        pass # Создаст дескриптор giveRaise


output('Хронометраж вызовов')
example('время единственного вызова и накопленное время всех вызовов')

import time
class timer:
    def __init__(self, func):
        self.func = func
        self.alltime = 0
    def __call__(self, *args, **kargs):
        start = time.clock()
        result = self.func(*args, **kargs)
        elapsed = time.clock() - start
        self.alltime += elapsed
        print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
        return result

@timer
def listcomp(N):
    return [x * 2 for x in range(N)]

@timer
def mapcall(N):
    return list(map((lambda x: x * 2), range(N))) # не создавая список, оставив просто итератор, меп победит без конкуренции

listcomp(5)
listcomp(50000)
listcomp(500000)
listcomp(1000000)
print('allTime = %s' % listcomp.alltime) # Общее время всех вызовов listcomp
print('')
mapcall(5)
mapcall(50000)
mapcall(500000)
mapcall(1000000)
print('allTime = %s' % mapcall.alltime) # Общее время всех вызовов mapcall
print('map/comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))

example('добавление аргументов декоратора')

import time
def timer(label='', trace=True): # Аргументы декоратора: сохраняются
    class Timer:
        def __init__(self, func): # На этапе декорирования сохраняется
            self.func = func # декорируемая функция
            self.alltime = 0

        def __call__(self, *args, **kargs): # При вызове: вызывается оригинал
            start = time.clock()
            result = self.func(*args, **kargs)
            elapsed = time.clock() - start
            self.alltime += elapsed
            if trace:
                format = '%s %s: %.5f, %.5f'
                values = (label, self.func.__name__, elapsed, self.alltime)
                print(format % values)
            return result
    return Timer

@timer(label='[CCC]==>')
def timer_inst(N): # timer_inst = timer(label='[CCC]==>')(timer_inst)
    return [x * 2 for x in range(N)]

'''
Внешняя функция timer вызы-
вается непосредственно перед операцией декорирования, она просто возвраща-
ет класс Timer, который будет играть роль фактического декоратора. В момент
декорирования создается экземпляр класса Timer, который запоминает саму
декорируемую функцию, но при этом ему остаются доступными аргументы де-
коратора, находящиеся в области видимости объемлющей функции.
'''
print(timer_inst)

#page 1117
"""
АДВЕНС ШЫТ
"""
'''
В отличие от декораторов классов, которые обычно добавляют логику, вызы-
ваемую на этапе создания экземпляров, метаклассы выполняются на этапе соз-
дания классов – они представляют собой обработчики, которые используются
для управления классами, а не их экземплярами.

использовать когда нам хотелось бы иметь возможность добавлять некоторый программный код, который
автоматически вызывался бы в конце инструкции class для расширения класса.

Это именно то, что предлагают метаклассы – объявляя метакласс, мы сообщаем интерпретатору,
что он должен передать создание объекта класса другому классу, указанному нами:

def extra(self, arg):
    pass

class Extras(type):
    def __init__(Class, classname, superclasses, attributedict):
        if required():
            Class.extra = extra

class Client1(metaclass=Extras): ... # Метакласс достаточно просто объявить
class Client2(metaclass=Extras): ... # Клиентский класс – экземпляр метакласса
class Client3(metaclass=Extras): ...
X = Client1() # X – экземпляр класса Client1
X.extra()

Поскольку интерпретатор автоматически вызывает метакласс в конце инструк-
ции class, сразу после создания нового класса, он получает возможность рас-
ширить, зарегистрировать или выполнить другие необходимые операции над
классом.
'''

a = 5
b = 's'
print(type(a))


class MetaTest(type):
    def __new__(cls, name, bases, dict):  # создание класса
        klass = super(MetaTest, cls).__new__(cls, name, bases, dict)
        print("__new__(%r, %r, %r) -> %r" % (name, bases, dict, klass))
        return klass

    def __init__(cls, name, bases, dict):  # инициализация класса
        super(MetaTest, cls).__init__(name, bases, dict)
        print("__init__(%r, %r, %r)" % (name, bases, dict))

    def __call__(cls, *args, **kwargs):  # создание экз объекта
        obj = super(MetaTest, cls).__call__(*args, **kwargs)
        print("__call__(%r, %r) -> %r" % (args, kwargs, obj))
        return obj


class TestClass(metaclass=MetaTest):
    pass


test = TestClass()


'''
Метакласс AutoSuper добавляет приватный атрибут __super для доступа к атрибутам и методам базовых классов
'''


class AutoSuper(type):
    def __init__(cls, name, bases, dict):
        super(AutoSuper, cls).__init__(name, bases, dict)
        setattr(cls, "_%s__super" % name, super(cls))  # mangling - искажение артибута, псевдочастный атрибут


class A(metaclass=AutoSuper):
    def method(self):
        return "A"


class B(A):
    def method(self):
        return "B" + self.__super.method()


print(B().method())


'''
Метакласс, устанавливающий атрибуты для объектов создаваемых классом без необходимости определения конструктора класса
'''


class AttrInit(type):
    def __call__(cls, **kwargs):
        obj = super(AttrInit, cls).__call__()
        for name, value in kwargs.items():
            setattr(obj, name, value)
        return obj


class Message(metaclass=AttrInit):
    pass


class ResultRow(metaclass=AttrInit):
    pass


msg = Message(type='text', text='text body')
print(msg.type)
print(msg.text)
row = ResultRow(id=1, name='John')
print(row.id)
print(row.name)

'''
Такой метакласс может быть полезен для создания классов объекты которых служат в основном как хранилище атрибутов.
Например, классов описывающих передаваемые по сети пакеты данных,
или строки результата запроса к базе данных к полям которых удобнее обращаться как к атрибутам.
Таким образом, метаклассы позволяют создавать классы с достаточно необычным поведением,
но в тоже время вряд ли стоит их использовать в каждой программе.
'''

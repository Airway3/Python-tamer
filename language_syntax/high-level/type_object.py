"""
ПОЗНАЕМ ПИТОНЯЧИЙ ДЗЕН
"""

class A(object): # в питоне 3 версии можно не наследовать обжект
    num_instance = 0

    def __init__(self): # инициализатор наполняет созданный экз атрибутами
        A.num_instance += 1
        self.inst_atr = 'inst attr' # атрибуты уникальные для каждого экз-ра

    def test(self):
        print(self)
        print(isinstance(self, A))

    def instance_method(self):
        print('instance method')

    @staticmethod
    def static_method():
        print('static method')
        print(A.num_instance)

    @classmethod # может служить для создания альетрантивных конструкторов
    def class_method(cls):
        print('class method', cls)


print('\n', '---------------------    A instance    -----------------------')

a_obj = A() # создадим экземпляр класса А
print(a_obj.__dict__) # все атрибуты экземпляра и их значения, заполняется __init__ при создании экземпляра
# и функциями которые используют в работе атрибуты начинающиеся с self (пример self.dog_name)

"""
Когда методы вызываются через экземпляр класса, интерпретатор автоматически передает бъект экземпляра в
первом аргументе, когда  метод  вызывается  через  имя  класса,  экземпляр  необходимо  передавать
методам  вручную.
"""
a_obj.instance_method()
A.instance_method(a_obj)

"""
Статические не требует передачи экзмепляра.
Вызываются без аргумента с экземпляром, ограничены областью видимости класса.
Вызов через класс доступен и без статикметода, статикметод нужен для вызова через экзмепляр.
Нахуй нужен? ---> Имеют доустп к атрибутам класса, лужит для работы с ними.
Манипулирвоание данными класса.
Метод не создаётся у объекта экземпляра , что повышает производителньость.
"""
a_obj.static_method()

"""
Методы класса похожи  на  них,  но  интерпретатор  автоматически  передает
методам класса сам класс (а не экземпляр) в первом аргументе, независимо от того,
вызываются они через имя класса или через экземпляр. 893 страница (изучаем питон Лутца).
Вызывая через класс наследник, перелаётся обхект класса наследника.
Управлять атрибутами конкретного/текущего класса.
"""
A.class_method()
a_obj.class_method()

print('\n', '--------------------    type / instance    -------------------')

a_obj.test() # isinstance - можем ли использовать данный объект в качестве объекта данного типа?
print('A is type instance:', isinstance(A, type)) # можем ли исп А в качестве типа?
print('A() is type instance:', isinstance(A(), type)) # можем ли исп экз А в качестве типа?
print('A() is A instance:', isinstance(A(), A)) # можем ли исп экз А в качестве класса/типа А?

print('\n', '-------------------    Class equal type    -------------------')

# все классы это типы и наоборот
print(object.__class__)
print(type.__class__)
print(type(object))
print(type(type))
print(type(A))
print(A.__class__)
print()

print(object.__name__)
print(type.__name__)
print(object.__bases__)
print(type.__bases__) # Экземпляры типа или класса object — это объекты (любые). Т.е. любой объект — экземпляр класса object
print(object.__dict__)
print(type.__dict__)
print()

print(isinstance(object, object))
print(isinstance(object, type)) # Т.к. object и type — тоже классы, то они являются экземплярами класса type
print(isinstance(type, type)) # Т.к. object и type — тоже классы, то они являются экземплярами класса type

print(issubclass(type, object)) # Т.к. множество классов (типов) являются подмножеством множества объектов, то логично предположить,
print(issubclass(object, type)) # что type является подклассом object


print('\n', '---------------------    Class A info    ---------------------')

print(A.__dict__) # все атрибуты класса и их значения
print(A.__bases__)
print(A.__name__)
print(A().__class__)
print(type(A()))

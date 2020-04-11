import math

'''
Flyweight design pattern: Slots
'''


class Circle(object):
    """ An advanced circle analytic toolkit """

    __slots__ = ['diameter'] # экземпляры без словаря (не можем добавл атр и инспектировать словарь),
    # а выделяется один указатель под диаметр. Слоты не наследуются
    version = '0.3'

    def __init__(self, radius):
        self.radius = radius

    '''
    Преобразует прямой доступ к свойству
    '''
    @property
    def radius(self):
        """ Radius of sircle """
        return self.diameter / 2.0

    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.0

    # def area(self):
    #     return math.pi * self.radius ** 2.0

    '''
    Вдруг, спецификация требует искать радиус через периметр для расчёта площади,
    вводим доп переменную, чтобы не поломать расширенный метод периметр у Tier
    '''

    def area(self):
        p = self.__perimeter()
        r = p / math.pi / 2.0
        return math.pi * r ** 2.0

    def perimeter(self):
        return 2.0 * math.pi * self.radius

    '''
    А согласно неофиц соглашению, имена начинающиеся с одного _ не должны изменяться за пределами класса
    '''

    __perimeter = perimeter # (mangling - искажение артибутов, они не частные, типо сделать локальными)
    # тут хранится оригинал функции периметр, а __perimeter автоматически расширяется именем класса _Circle__perimeter
    # нужно для избегания конфликтов, а не приватности

    '''
    Частое применение это создание альтернативных конструкторов
    '''

    @classmethod
    def from_bbd(cls, bbd):
        """ Construct a circle from a bounding box diagonal """
        radius = bbd / 2.0 / math.sqrt(2.0) # приводим диагональ к радиусу
        return cls(radius) # было Circle(radius), но а если вызов через наследника? для поддержки наследования исп cls

    '''
    Просто закрепление функции за классом
    '''
    @staticmethod
    def angle_to_grade(angle):  # цель статик метода - присоединить функц классам,  не привязывать к экземпляру
        """ Convert angle in degree to a percentage grade """
        return math.tan(math.radians(angle)) * 100.0  # мы просто добавляем нужный инструмент в наш класс, но не для работы с кругами


class Tire(Circle):
    """ Tires are circles with a corrected perimeter' """

    def perimeter(self):
        """ Circumference corrected for the rubber """
        return Circle.perimeter(self) * 1.25

    __perimeter = perimeter # _Tire__perimeter

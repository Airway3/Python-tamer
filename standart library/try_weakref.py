import weakref


# class Account(object):
#     def __init__(self,name,balance):
#         self.name = name
#         self.balance = balance
#         self.observers = set()
#
#     def __del__(self):
#         for ob in self.observers:
#             ob.close()
#
#         print('bye acc obs')
#         del self.observers
#         print('bye %s acc' % self.name)
#
#     def register(self,observer):
#         self.observers.add(observer)
#
#     def unregister(self, observer):
#         print('unregister observer %s' % observer)
#         observer.close()
#         self.observers.remove(observer)
#
#     def notify(self):
#         for ob in self.observers:
#             ob.update()
#
#     def withdraw(self,amt):
#         self.balance -= amt
#         self.notify()
#
#
# class AccountObserver(object):
#     def __init__(self, theaccount):
#         self.accountref = weakref.ref(theaccount) # Создаст слабую ссылку
#         theaccount.register(self)
#
#     def __del__(self):
#         print('del obs', self)
#         acc = self.accountref()    # Вернет объект счета
#         if acc:                    # Прекратить наблюдение, если существует
#             print(acc.observers)
#
#     def update(self):
#         print('Баланс: %0.2f' % self.accountref().balance)
#
#     def close(self):
#         print('Наблюдение за счетом окончено', self.accountref())
#
#
# # Пример создания
# a = Account('Дейв', 1000.00)
# a_ob = AccountObserver(a)
# a_2_ob = AccountObserver(a)
# a_3_ob = AccountObserver(a)
#
# print('script start')
# del a
#
# # a.unregister(a_ob)
# # del a_ob
#
# print('script ending')


def finalizer(ref):
    print("Объект больше не достижим")


obj = set()
reference = weakref.ref(obj, finalizer)

d = {
    'key': obj
}
del obj
del d

ws = weakref.WeakSet()
wd = weakref.WeakKeyDictionary()
wv = weakref.WeakValueDictionary()

print('script ending')
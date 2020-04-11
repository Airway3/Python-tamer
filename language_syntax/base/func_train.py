

def f(immutable):
    print(immutable, id(immutable))
    immutable += 100
    print(immutable, id(immutable))


b = 5
f(b)
print(b, id(b))
print('-' * 100)


def f2(lis):
    print(lis, id(lis))
    lis = lis + [200] # create new lis LOCAL variable
    print(lis, id(lis)) # local lis id


c = []
f2(c)
print(c, id(c))

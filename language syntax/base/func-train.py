
def f(lis):
    print(lis, id(lis))
    lis += 100
    print(lis, id(lis))

b = 5
f(b)
print(b, id(b))



def f2(lis):
    lis = lis + [200] # create new lis LOCAL variable
    print(lis, id(lis)) # local lis id

c = []
f2(c)
print(c, id(c))
print('Test №1')

global_var = True

def test():
    global_var = False # объявлена локальная переменная
    print('local:', global_var)

test()
print('global:', global_var, '| global var no changed', '\n')


print('Test №2')

global_var2 = True

def try_global():
    global global_var2 # через запятую можно несколько
    global_var2 = False # переопределяем глобальную переменную
    print('local:', global_var2)

try_global()
print('global:', global_var2, '| global var changed', '\n')


print('Test №3')

def try_nonlocal():
    local_var = 5
    def inner():
        nonlocal local_var # нонлокал - переменная которая будет найдена по пути от локального неймспейса к глобалу, не включая их
        local_var = 7 # переопределяем переменную между глобал и локал неймспейсами

    print('local var:', local_var)
    inner()
    print('func inner change local_var:', local_var)

try_nonlocal()


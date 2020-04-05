import sys
print(sys.platform, sys.getdefaultencoding())

b = bytes([104, 117, 105])
for i in b:
    print(chr(i))

byte_string = b'byte_string'
print(byte_string)
for i in byte_string:
    print(i)

print(len(str(byte_string))) # без указания кодировки перегоняет в строку некорректно вместе с символом b

# разберёмся с представлением символов через 16 ричные числа
print(chr(0xc4), '\xc4', '\u00c4')
"""
шестнадцатеричные  экранированные  последовательности значений байтов могут представлять только значения отдельных байтов
а экранированные  последовательности  значений  символов  Юникода могут определять символы, состоящие из двух или четырех байтов
"""
print('\xc4\xc7') # не ASCII символы в 16 реичной системе через X можно указать только один байт
print('\u00c4\u00c7') # не ASCII символы в 16 реичной системе через U можно указать символы из 2, 4 байт
print(ord('Ы'), 0x42b, '\u042b') # чтобы вывести Ы нужно два байта
print('Ы'.encode('utf-8'))


with open('test.txt', 'wb') as f:
    print(f.write(b)) # number of characters written

with open('test.txt', 'rb') as f:
    print(f.read())

# print(ord('\xc8'), 0b100)
#
# o1 = object()
# print(hash(o1))

# def recursive_map(f, lis):
#     if lis:
#         yield f(lis[0])
#         yield from recursive_map(f, lis[1:])
#
#
# print(list(recursive_map(str, [5, 8, 3, 9, 1])))


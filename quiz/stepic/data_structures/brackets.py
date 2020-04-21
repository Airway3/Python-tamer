

BRACKETS_MAP = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def check_bracket(string):
    stack = []  # [(2, '('), (3, '{'), (8, '(')]

    for i, s in enumerate(string):
        if s in BRACKETS_MAP:
            stack.append((i + 1, s))
        elif s in BRACKETS_MAP.values():
            if not stack:
                return i + 1
            else:
                position, top = stack.pop()
                if (top == '(' and s != ')') or (top == '[' and s != ']') or (top == '{' and s != '}'):
                    return i + 1

    return stack[0][0] if stack else 'Success'


i = input()
print(check_bracket(i))
# print(check_bracket('()[]}'))
# print(check_bracket('{{[()]}'))

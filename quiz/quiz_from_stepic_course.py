def all_parents(cl, parents):
    try:
        for parent in parents:
            d[cl].add(parent)
            all_parents(cl, d[parent])
    except RuntimeError:
        return None

# d = {'A':set(), 'G':{'F'}, 'B': {'A'}, 'C': {'A'}, 'D': {'B', 'C'}, 'E': {'D'}, 'F': {'D'}, 'X': set(), 'Y': {'X', 'A'},
#      'Z': {'X'}, 'V': {'Z', 'Y'}, 'W': {'V'}}
d = {}
n = int(input())
for m in range(n):
    class_and_parents = input().split()
    current_class = class_and_parents[0]
    d[current_class] = set()
    for parent in range(2, len(class_and_parents)):
        d.get(current_class).add(class_and_parents[parent])

for classs, set_parents in d.items():
    all_parents(classs, set_parents)

print(d)

query = int(input())
for q in range(query):
    inst_string = input().split()
    if inst_string[0] not in d.keys():
        print('No')
    elif inst_string[1] not in d.keys():
        print('No')
    elif inst_string[0] == inst_string[1]:
        print('Yes')
    elif inst_string[0] in d.get(inst_string[1]):
        print('Yes')
    elif inst_string[0] == inst_string[1]:
        print('Yes')
    else:
        print('No')
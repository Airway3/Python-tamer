#
#
# from random import randint
#
#
# def linear(some_list):
#     if len(some_list) == 0:
#         return [some_list]
#
#     branch_list = []
#
#     # for i in range(len(some_list)):
#     # # for i in range(len(some_list), -1, -1):
#     #     branch_list.extend(linear(some_list[i]))
#     for l in some_list:
#         branch_list.extend(linear(l))
#
#     return branch_list
#
#
# def tree(depth, parent_list):
#     if depth == 1:
#         return parent_list
#
#     # for i in range(1, depth):
#     new_list = [[]] * randint(1, depth)
#     random_child = parent_list[randint(0, len(parent_list) - 1)]
#     random_child.append(new_list)
#
#     return tree(depth - 1, random_child)
#
#
# def generate_nested_lists(depth, roots_count=3):
#     depth = max(depth, 1)
#     return [tree(depth, [[]] * randint(1, depth)) for i in range(1, roots_count + 1)]
#
#
# lst = generate_nested_lists(3)
#
#
# print(lst)
# print('==='* 10)
# for l in lst:
#     print(l)
# print('==='* 10)
# print(*linear(lst))
# print(*linear([[], [[], [[], []]], []]))




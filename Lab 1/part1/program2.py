a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print('a = [', end='')
print(*a, sep=', ', end='')
print(']')
b = []
user_number = int(input('Enter number: '))
[b.append(i) for i in a if i < user_number]
print('b = [', end='')
print(*b, sep=', ', end='')
print(']')
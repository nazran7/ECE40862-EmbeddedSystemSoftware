user_input = int(input('How many Fibonacci numbers would you like to generate? '))
x, y = 0, 1
z =[]
for i in range(user_input):
       z.append(y)
       x, y = y, x+y
       i = i+1
print('The Fibonacci Sequence is: ', end='')
print(*z, sep=', ', end='')
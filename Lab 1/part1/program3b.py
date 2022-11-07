import random
x = random.randint(0, 10)
guesses = 0
user_input = int(input('Enter your guess:'))
while guesses <= 1:
    if  user_input == x:
        break
    else:
        guesses = guesses + 1
        user_input = int(input('Enter your guess:'))

if user_input == x:
    print('You win!')
else:
    print('You lose!')
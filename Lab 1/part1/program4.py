birthdays = {
        'Tony Stark': '10/18/1979',
        'Stephen Strange': '09/19/2006',
        'Bruce Wayne': '12/12/2015',
        'John Wick': '03/12/2001',
        'James Bond': '01/11/1999'}
print('Welcome to the birthday dictionary. We know the birthdays of:')
print('Tony Stark')
print('Stephen Strange')
print('Bruce Wayne')
print('John Wick')
print('James Bond')
print('Whose birthday do you want to look up?')
name = input()
print(f"{name}'s birthday is {birthdays[name]}.")
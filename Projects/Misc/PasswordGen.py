import random
print('Welcome to the Password Generator!')
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'
length = int(input('Enter the desired length of the password: '))
password = ''.join(random.choice(chars) for _ in range(length))
print('Your random password is:', password)
import random

def starting_numbers():
    i = 0
    l = []
    while i < 5:
        x = random.randint(10000,20000)
        if x % 6 == 0:
            l.append(x)
            i+=1
    return l

print(starting_numbers())

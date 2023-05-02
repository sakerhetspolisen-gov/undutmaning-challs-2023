import random

x_max = 100
y_max = 25

art = open('ascii_flag').readlines()
l = []

for y, v in enumerate(art):
    for x, v2 in enumerate(v):
        if v2 == '@':
            l.append((x, y))

for i in range(75):
    x = random.randrange(1, x_max - 1)
    y = random.randrange(1, y_max - 1)
    if (x, y) in l:
        continue
    l.append((x, y))

random.shuffle(l)
for _, x in enumerate(l):
    print('{%s, %s},' %(x[1], x[0]))
print(f'array length: {len(l)}')

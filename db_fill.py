from random import randint
import pandas as pd

avail = []
d = pd.read_excel('DATA.xlsx')
used = set(d.ID)
for i in range(1000000, 10000000):
    if i not in used:
        avail.append(i)
del used

count = int(input("Total count:"))
d = d.append([d.iloc[-1]] * (count - 1))
ids = avail[:count]
del avail[:count]
d.iloc[-count:, 0] = ids
print(d.tail(-count - 2))
if 'y' in input('Write to db?: ').lower():
    d.to_excel('DATA.xlsx', index=False)

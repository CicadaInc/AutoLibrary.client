from PPI import Print
import pandas as pd

d = pd.read_excel("DATA.xlsx")
count = int(input("Count: "))
name = input("Name: ")
author = input("Author: ")
p = Print()
p.print_multiple([(name, author, e) for e in d.iloc[-count:, 0]])

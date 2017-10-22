import csv
import re

atomic_masses = {}

with open('periodic_table.csv') as csvfile:
    ptable_reader = csv.reader(csvfile, delimiter=',')
    for row in ptable_reader:
        element_symbol = str(row[0])
        atomic_mass = float(row[1])
        atomic_masses[element_symbol] = atomic_mass

chemical_formula = input()

pattern = re.compile(r'([A-Z][a-z]?)([0-9]*)')
mass = 0
for symbol, number in re.findall(pattern, chemical_formula):
    if not number:
        number = 1

    mass = mass + number*atomic_masses[symbol]

print('{}'.format(mass))

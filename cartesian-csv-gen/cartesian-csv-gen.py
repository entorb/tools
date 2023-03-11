from configparser import ConfigParser
import itertools

#
# by Dr. Torben Menke, 24.09.2019
#

"""
reads config.ini
extracts dynamic parameters (list of values per parameter, sep. by ," )
generates cartesian product of dynamic parameters
"""

config = ConfigParser()
config.read('cartesian-csv-gen.ini')

listOfKeys = []
listsOfValues = []

for k in config.options('dynamic'):
    s = config.get('dynamic', k)
    listOfKeys.append(k)
    l = s.split(",")
    l = [v.strip() for v in l]  # trim white spaces
    listsOfValues.append(l)

FILE = open("out.csv", "w", newline="\n")
FILE.write('\t'.join(listOfKeys))
FILE.write("\n")

# Cartesian product of the listsOfDynVars
for combination in itertools.product(*listsOfValues):
    FILE.write('\t'.join(combination))
    FILE.write("\n")

FILE.close()

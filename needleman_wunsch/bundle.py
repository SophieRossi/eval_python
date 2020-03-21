# imports
import sys
import math
import numpy as np
from colorama import Fore, Style
from ruler import Ruler

file_name = sys.argv[1]

# on ouvre le fichier pour compter ses lignes et enlever les lignes vides
with open(file_name, "r") as reader:
    nb_lines = 0
    for line in reader:
        nb_lines += 1
    if nb_lines % 2 != 0:
        nb_lines -= 1  # on ingnorera la ligne orpheline
reader.close()

"""
On ouvre à nouveau le fichier pour lire deux à deux les lignes (en ignorant la
dernière si jamais le nombre de lignes du fichier est impair).

On construit pour chaque couple de lignes le Ruler correspondant, et on
appelle les méthodes compute et report qui donnent respectivement la distance et
les chaine avec en rouge les différences.
"""

with open(file_name, "r") as reader:
    i = 0
    while i < nb_lines:
        line1 = reader.readline()
        line2 = reader.readline()
        r = Ruler(line1, line2)
        r.compute()
        distance = r.distance
        top, bottom = r.report()
        print("distance = ", distance)
        print(top)
        print(bottom)
        i += 2

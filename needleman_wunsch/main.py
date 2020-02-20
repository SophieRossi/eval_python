# imports
import math
import random
import numpy as np
import time
from colorama import Fore, Style
from ruler import Ruler
from random import randint


# on crée un objet pour mesurer
#la distance entre deux chaines
ruler = Ruler("abcdefghi", "abcdfghi")

# on impose à l'utilisateur de la classe
# de lancer explicitement le calcul
ruler.compute()

# on obtient la distance
print(ruler.distance)

# et pour afficher les différences
top, bottom = ruler.report()
print(top)
print(bottom)


"""
TEMPS D'EXECUTION

Afin de m'assurer de la performance de mon code, je calcule le temps d'exécution
de la comparaison de 2 chaines d'une longueur de 1000 caractères.

Pour cela, à l'aide de la méthode random.randint() on crée une chaine d'ADN
aléatoire. On la modifie ensuite, en supprimant et en remplaçant aléatoirement
des nucléotides. On compare enfin les deux chaines obtenues.

On utilise le module time de python: la méthode process_time() (ou time.clock()
pour les versions de python avant 3.3) donne l'heure "exacte". Le temps de
comparaison des chaines correspond au temps d'exécution de la méthode compute().

Après avoir fait tourner ce code plusieurs fois, le temps d'exécution que
j'obtiens oscille autour de 2.3 secondes, et reste donc inférieur à 3 secondes.
"""

# génération d'une chaine d'ADN aléatoire de 1000 caractères
N = ["A", "T", "C", "G"]
ch1 = ""
for i in range(1000):
    n = random.randint(0, 3)
    ch1 += N[n]

# modification de la chaine
ch2 = ""
for i in range(1000):
    n = random.randint(0, 2)
    if n == 0:
        ch2 += ""  # suppression
    if n == 1:
        ch2 += ch1[i]  # aucun changement
    if n == 2:
        k = random.randint(0, 3)
        ch2 += N[k]  # remplacement avec une probabilité 3/4

# horloge
r = Ruler(ch1, ch2)
time1 = time.process_time()
r.compute()
time2 = time.process_time()
print("La distance est: ", r.distance)
top, bottom = r.report()
print("\n \nExemple d'un temps d'exécution")
print("Comparaison de chaines aléatoires de 1000 caractères")
print("Voici la chaine initiale:\n", top)
print("Voici la chaine mutée:\n", bottom)
print("Le temps d'exécution de la comparaison est: ", time2-time1)

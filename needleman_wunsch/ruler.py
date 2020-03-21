# imports
import math
from colorama import Fore, Style
import numpy as np


# on reprend la méthode fournie dans l'énoncé pour colorer un texte en rouge
def red_text(text: str):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


"""
Dans toute mon implémentation, j'ai construit des méthodes consistant à
maximiser l'alignement, ce qui correspond à minimiser la distance.
C'est pourquoi, le paramètre de "pénalité de trou" (insertion/ délétion) d et
les valeurs dans la matrice de similarité S sont négatives.



Discussion sur l'adaptabilité du code:

Le paramètre d est une donnée du problème: il a une valeur par défaut (-1) qui
est facilement modifiable lors de la construction d'un Ruler: l'instruction
correspondante est r = Ruler(str1, str2, d_1)

On appelle S_0 la matrice de similarité: pour une liste de caractères donnée
(par exemple ATCG, abcdefghi etc.) elle donne les valeurs des couples (i, j)
c'est à dire la valeur d'un remplacement d'un caractère par un autre.

Dans notre cas le remplacement vaut toujours -1 sauf si i = j. On peut alors
aisément construire S la matrice de similarité pour 2 chaines données (cf
description plus détaillée dans calcul_S()).

Afin de prendre en compte des valeurs de remplacement différentes, on pourrait
passer en paramètre la matrice S_0 et créer l'attribut correspondant. Il
faudrait alors réécrire la fonction calcul_S de sorte qu'à chaque couple de
caractères (k1, k2) en position (i, j) de (str1, str2) leur valeur S(i, j)
corresponde à S_0(k1, k2).



Discussion sur la complexité:

La méthode la plus lourde en termes de complexité est calcul_F(), en ce qu'il
s'agit d'une méthode récursive.

Elle est appelée dans compute() et report().

En effet, init() est en O(1), calcul_S() est en O(n^2), et si compute() a déjà
été appelée, report() est en O(1).


"""


class Ruler:

    def __init__(self, str1: str, str2: str, d=-1):
        """
        Un objet Ruler prend en paramètre les 2 chaines à comparer.
        On ajoute le paramètre d qui est la "pénalité de trou" et qui
        vaut -1 par défaut.

        On ajoute les attributs suivants:
            - S la matrice de similarité pour le couple (str1, str2)
            - F la matrice telle que Fij donne l'alignement maximal pour les i
            premiers caractères de str1 et les j premiers de str2
            - distance qui renvoie le nombre de différences (insertion,
            délétion, remplacemnet) entre les deux chaines
            - top et bottom qui sont les chaines avec la "bonne" mise en forme
            et les caractères en rouge afin de visualiser les différences

        Initialisation des attributs:
            - distance, top et bottom sont initialisés comme None, ce qui est
            exploité et détaillé dans les méthodes report() et compute()
            - S et F sont initialisées comme les matrices nulles de la bonne
            taille
        """

        self.str1 = str1
        self.str2 = str2
        self.distance = 0
        self.S = np.zeros((len(self.str2), len(self.str1)))
        self.F = np.zeros((len(self.str2) + 1, len(self.str1) + 1))
        self.d = d
        self.distance = None
        self.top = None
        self.bottom = None

    def calcul_S(self):
        """
        Cette méthode lit tous les couples (k1, k2) de caractères de
        (str1, str2).
        Si k1 = k2 alors il n'y a pas de différences à cet endroit: ainsi
        S(i, j) = 0 si on note i (resp. j) la position de k1 (resp. k2) dans
        str1 (resp. str2).
        Sinon, la valeur associée à une modification est -1.
        """

        for i in range(len(self.str2)):
            for j in range(len(self.str1)):
                if self.str2[i] != self.str1[j]:
                    self.S[i][j] = -1
                else:
                    self.S[i][j] = 0

    def calcul_F(self):
        """
        Cette méthode récursive calcule F telle que Fij soit l'alignement
        maximal pour les i premiers caractères de str1 et les j premiers de
        str2.

        Pour cela, il y a une colonne et une ligne supplémentaires par rapport
        à S (et donc à la taille de str1 et str2) qui sont l'objet de
        l'initialisation.
        Au préalable, on calcule S qui va servir lors de la récursion.
        """
        # initialisation
        S = self.calcul_S()
        l = len(self.str1) + 1
        c = len(self.str2) + 1
        self.F[0][0] = 0
        for i in range(c):
            self.F[i][0] = self.d*i
        for j in range(l):
            self.F[0][j] = self.d*j
        # récursion
        for i in range(1, c):
            for j in range(1, l):
                self.F[i][j] = max(self.F[i-1][j-1] + self.S[i-1][j-1],
                                   self.F[i-1][j] + self.d, self.F[i][j-1] + self.d)

    def compute(self):
        """
        Cette méthode a pour but de calculer la distance entre les 2 chaines,
        c'est à dire le nombre d'insertions/suppressions/remplacements desquels
        elles diffèrent.

        Cette méthode ne doit tourner qu'une seule fois pour un Ruler donné
        (sinon on multiplie la valeur de d). En particulier, report() fait appel
        à compute() ce qui pourrait faire augmenter d. Comme on initialise d à
        None, ce phénomène est empeché par l'instruction :
        "if self.distance == None".

        On traite successivement tous les cas possibles (str1[i] et str2[j] sont
        alignés, décalés vers le "haut" ou vers la "gauche") et si il y a une
        différence on incrémente la distance de 1. L'attribut distance est
        directement modifié et est renvoyé à la fin.

        C'est également dans cette méthode que l'on construit les chaines top et
        bottom qui vont permettre la visualisation en rouge des différences.

        La méthode modifie directement les attributs du Ruler, ce qui fait qu'il
        est suffisant de la faire tourner une seule fois étant donnée sa
        complexité. Par la suite, il suffira de faire appel aux attributs
        directement.

        NB: l'indiçage sur F n'est pas le meme que sur S, str1 et str2. Ceci est
        du au fait que F a en plus une ligne et une colonne d'initialisation.
        """

        if self.distance == None:

            # initialisation
            self.distance = 0  # au mieux les 2 chaines sont les memes
            symbol = "="  # sert dans l'expression pour colorer en rouge
            self.calcul_S()
            self.calcul_F()
            align_str1, align_str2 = "", ""
            j = len(self.str1)
            i = len(self.str2)

            while (i > 0 and j > 0):
                # On a trois cas possibles selon la valeur du max (par
                # construction de F[i][j])

                # Cas 1: str1[i-1] et str2[j-1] sont alignés
                if self.F[i][j] == self.F[i-1][j-1] + self.S[i-1][j-1]:
                    # soit les caractères sont les memes
                    if self.str1[j-1] == self.str2[i-1]:  
                        align_str1 = self.str1[j-1] + align_str1
                        align_str2 = self.str2[i-1] + align_str2

                    else:
                        # soit les caractères sont différents donc on les met en rouge
                        align_str1 = f"{red_text(self.str1[j-1])}{align_str1}"
                        align_str2 = f"{red_text(self.str2[i-1])}{align_str2}"
                        self.distance += 1
                    i -= 1
                    j -= 1

                # Cas 2: Décalage gauche ie str1[i-1] aligné avec un trou
                elif self.F[i][j] == self.F[i-1][j] + self.d:
                    align_str1 = f"{red_text(symbol)}{align_str1}"
                    align_str2 = self.str2[i-1] + align_str2
                    self.distance += 1
                    i -= 1

                # Cas 3: Décalage "haut" ie str2[j-1] aligné avec un trou
                else:
                    align_str1 = self.str1[j-1] + align_str1
                    align_str2 = f"{red_text(symbol)}{align_str2}"
                    self.distance += 1
                    j -= 1

            # les 2 chaines ne sont pas, a priori, de meme longueur
            # on traite les cas restants:
            while j > 0:
                align_str1 = self.str1[j-1] + align_str1
                align_str2 = f"{red_text(symbol)}{align_str2}"
                self.distance += 1
                j -= 1

            while i > 0:
                align_str1 = f"{red_text(symbol)}{align_str1}"
                align_str2 = self.str2[i-1] + align_str2
                self.distance += 1
                i -= 1

            self.top, self.bottom = align_str1, align_str2

        return self.distance

    def report(self):
        """
        Cette méthode renvoie les 2 chaines de caractères où sont clairement
        identifiées les différences en rouge.

        Les attributs top et bottom sont obtenus par la méthode compute(), qu'on
        ne veut faire tourner qu'une seule fois. On vérifie cela en regardant si
        bottom et top ne sont pas None (qui correspond à leur initialisation).
        """

        if self.top == None and self.bottom == None:
            self.compute()
        return self.top, self.bottom

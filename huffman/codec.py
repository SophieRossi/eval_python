class Node:
    """
    La classe Node construit les noeuds qui vont ensuite constituer les arbres
    binaires.

    Les Node sont porteurs de 2 informations (paramètres puis attributs):
        - une chaine de caractères
        - une fréquence: si la chaine est constituée d'un unique caractère, elle
        correspond à la fréquence du caractère dans le texte. Sinon cette valeur
        est calculée dans Treebuilder.tree() (et ne correspond plus vraiment à
        une fréquence!)

    De plus, un noeud a au plus un fils gauche et un fils droit, initialisés à
    None et qui peuvent etre ajoutés grace aux méthodes new_left_child et
    new_right_child.
    """

    def __init__(self, ch: str, freq: float):
        self.ch = ch
        self.freq = freq
        self.left = None  # fils gauche
        self.right = None  # fils droit

    def new_left_child(self, node):  # crée le fils gauche
        self.left = node

    def new_right_child(self, node):  # crée le fils droit
        self.right = node


class TreeBuilder:
    """
    La classe Treebuilder a pour but de construire l'arbre binaire servant au
    codage de Huffman, grace à la méthode tree().

    Cet arbre est construit à partir des occurrences de chaque caractère dans le
    texte saisi en paramètre. Pour cela on construit un dictionnaire contenant
    les caractères (clés) et leur fréquences (valeurs): c'est l'objet de la
    méthode dico_freq().

    Un TreeBuilder possède donc 2 attributs: le texte à coder (qui est aussi un
    paramètre) et le dictionnaire.

    La méthode build_list_nodes() est une méthode intermédiaire permettant
    d'alléger le code de tree().
    """

    def __init__(self, text: str):
        self.text = text
        self.dico = {}  # on initialise un dictionnaire vide

    def dico_freq(self):

        for el in self.text:
            if not el in self.dico:
                # si le caractère n'est pas dans le dictionnaire, on le rajoute
                self.dico[el] = 0
            self.dico[el] += 1  # incrémentation de sa fréquence d'apparition

    def build_list_nodes(self):
        """
        Cette méthode construit une liste où chaque élément est lui meme une
        liste contenant un Node (en position 0) et la fréquence de ce noeud (en
        position 1).

        Cette méthode sera appelée dans tree() pour construire tous les noeuds
        initiaux (où ch est un seul caractère) à partir du dictionnaire.

        Le fait d'avoir des éléments du type [Node, freq] permettra de trier la
        liste par rapport à la deuxième variable (dans tree()).
        """

        L = []
        self.dico_freq()
        for key in self.dico:
            node = Node(key, self.dico[key])
            L.append([node, self.dico[key]])
        return L

    def tree(self):
        """
        Cette méthode construit l'arbre selon le principe suivant: pour les 2
        noeuds de plus petit freq on crée leur parent. C'est alors le noeud qui
        a pour ch la concaténation des ch de ses enfants et qui a pour freq la
        somme des fréquences de ses enfants.

        Pour commencer, on crée la liste des noeuds avec build_list_nodes().
        A chaque itération, on supprime les 2 noeuds fils de la liste et on
        ajoute le nouveau noeud parent. On trie alors la liste selon la deuxième
        variable.

        On itère jusqu'à ce que la liste ne contienne plus qu'un seul élément:
        c'est l'arbre entier!
        """
        L = self.build_list_nodes()
        while len(L) > 1:
            L.sort(key=(lambda x: x[1]))  # expression lambda pour trier L
            tree1 = L[0][0]
            tree2 = L[1][0]
            val = tree1.freq + tree2.freq
            ch = tree1.ch + tree2.ch
            parent = Node(ch, val)
            parent.new_left_child(tree1)
            parent.new_right_child(tree2)
            L.append([parent, val])
            L.pop(0)  # suppression du fils1
            L.pop(0)  # suppression du fils2
        tree = L[0][0]
        return tree


class Codec:
    """
    La classe Codec a pour but de construire un codeur/décodeur pour le codage
    de Huffman à partir de l'arbre binaire (obtenu par Treebuilder.tree()) en
    paramètre.

    On munit un Codec d'un autre attribut: un dictionnaire qui va
    contenir les codes des caractères. Ces codes étant obtenus par la méthode
    tree_codes() qui fait elle-meme appel à give_codes().

    Les méthodes encode() et decode() assurent le codage et décodage du texte
    saisi en paramètre.
    """

    def __init__(self, tree: Node):
        self.tree = tree
        # contiendra les (clé, valeur) = (caractère, code)
        self.dico_codes = {}

    def give_codes(self, node: Node, code=""):
        """
        C'est une méthode récursive qui construit les codes à partir d'un noeud
        donné. On descend à travers sa descendance: un fils gauche correspond
        à un 0 et un fils droit à un 1.
        Les (caractère, code) constituent un dictionnaire.
        """

        if node == None:
            return
        else:
            self.dico_codes[node.ch] = code
            self.give_codes(node.left, code + "0")
            self.give_codes(node.right, code + "1")

    def tree_codes(self):
        """
        On construit les codes pour l'arbre saisi en entrée.
        En effet tree est aussi le Node racine.
        """

        self.give_codes(self.tree)

    def encode(self, text: str):
        """
        On initialise encoded à une chaine vide.
        Codage: on lit un à un les caractères du texte et on concatène le code
        correspondant (obtenu à partir du dictionnaire) à encoded.
        """

        self.tree_codes()
        ch = text
        encoded = ""
        for el in ch:
            if not el in self.dico_codes.keys():
                print("Pb: le caractère absent du dico donc pas de code!")
                break
            else:
                encoded += str(self.dico_codes[el])
        return encoded

    def decode(self, code: str):
        """
        On redescend l'arbre en partant de la racine en lisant chaque caractère
        du code. Si c'est un 0 alors on va vers le fils gauche, si c'est un 1
        vers le fils droit. On fait ceci jusqu'à arriver dans une feuille: on a
        alors trouvé le caractère ch correspondant.

        On réitère ce processus jusqu'à ce qu'on ait lu tous les caractères du
        code.
        """
        node = self.tree  # on part de la racine
        ch = code
        result = ""
        for i in range(len(ch)):
            if ch[i] == "0":
                node = node.left
            else:
                node = node.right
            if node.left == None and node.right == None:
                result += node.ch
                node = self.tree
        return result

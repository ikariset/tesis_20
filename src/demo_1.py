# import classes.RankedTree
import numpy
# from classes import RankerTree
from classes.RankerTree import RankerTree


# import __init__


def demo1():
    # Creacion de la matriz que se analizara
    elem = 20
    docs = 20

    matrix = numpy.random.rand(docs, elem).round()

    # Se crea el objeto que albergara el arbol
    tree = RankerTree(matrix)

    tree.unwrapTree()

    print ("Cabeza de arbol: \n{}\nRanking de documentos: \n{}" .format(tree.topNode.matrix, tree.topNode.ranking))
    # Demo controlado para una matriz de 4 x 4
    print ("Por la izquierda: \n{} \nPor la derecha: \n{}" .format(tree.topNode.leftNode.matrix, tree.topNode.rightNode.matrix))
    print ("Por la izquierda: \n{} \nPor la derecha: \n{}".format(tree.topNode.leftNode.leftNode.matrix, tree.topNode.leftNode.rightNode.matrix))


if __name__ == "__main__":
    demo1()

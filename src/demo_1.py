import numpy as np
from classes.RankerTree import RankerTree


def demo1():
    # Creacion de la matriz que se analizara
    elem = 10
    docs = 10

    matrix = np.random.rand(docs, elem).round()

    print("Esta es la Matriz: \n{}" .format(matrix))

    # Se crea el objeto que albergara el arbol
    tree = RankerTree(matrix)
    tree.unwrapTree()

    print("Cabeza de arbol: \n{}\nRanking de documentos: \n{}" .format(tree.topNode.matrix, tree.topNode.ranking))
    # Demo controlado para una matriz de 4 x 4
    print("Por la izquierda: \n{} \nPor la derecha: \n{}" .format(tree.topNode.leftNode.matrix, tree.topNode.rightNode.matrix))
    print("Por la izquierda: \n{} \nPor la derecha: \n{}\n".format(tree.topNode.leftNode.leftNode.matrix, tree.topNode.leftNode.rightNode.matrix))

    # print("Esta es la matriz ordenada: \n{}" .format(orderedMatrix))

    # tree.getRunsData(matrix)
    runsArray = tree.getRunsData()
    print("Este es el array de Runs: {}\n De esta matriz ordenada: \n{}" .format(runsArray, tree.getOrderedMatrix()))

    runsArray = tree.getRunsData(matrix)
    print("Este es el array de Runs: {}\n De esta matriz ordenada: \n{}".format(runsArray, matrix))


if __name__ == "__main__":
    demo1()

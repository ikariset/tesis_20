import numpy as np
from classes.RankerTree import RankerTree
from classes.InvertedIndexFactory import InvertedIndexClass
import matplotlib.pyplot as plt


def get_demo_data(docnum, termsnum):
    # Demo Data Generation

    # Mock Document names generation
    docnames = []
    for i in range(1, docnum + 1):
        docnames.append("doc" + str(i) + ".txt")

    # Mock Terms generation
    terms = []
    for i in range(1, termsnum + 1):
        terms.append("t" + str(i))

    matrix = np.random.rand(len(docnames), len(terms)).round()

    return matrix, docnames, terms


def get_run_process(demo_mode=False):
    _matrix = []
    _docnames = []
    _terms = []

    inv_index = InvertedIndexClass()
    _matrix, _docnames, _terms = inv_index.get_data_from_input()

    # RankerTree Object creation
    tree = RankerTree(_matrix,_docnames,_terms)
    tree.unwrapTree()

    """
    print("Cabeza de arbol: \n{}\nRanking de documentos: \n{}" .format(tree.topNode.matrix, tree.topNode.ranking))
    # Demo controlado para una matriz de 4 x 4
    print("Por la izquierda: \n{} \nPor la derecha: \n{}" .format(tree.topNode.leftNode.matrix, tree.topNode.rightNode.matrix))
    print("Por la izquierda: \n{} \nPor la derecha: \n{}\n".format(tree.topNode.leftNode.leftNode.matrix, tree.topNode.leftNode.rightNode.matrix))
    """

    # Creating plot for Ordered Matrix
    tree.getRunsPlotAndData()

    # Creating plot for Unordered Matrix
    tree.getRunsPlotAndData(_matrix)

    plt.show()


if __name__ == "__main__":
    get_run_process(demo_mode=True)

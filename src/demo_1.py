import numpy as np
from classes.RankerTree import RankerTree
from classes.InvertedIndexFactory import InvertedIndexClass
import matplotlib.pyplot as plt

def get_demo_data(docnum, termsnum):
    # Creacion de la matriz que se analizara

    # Creación de array de documentos
    docnames = []
    for i in range(1, docnum + 1):
        docnames.append("doc" + str(i) + ".txt")

    # Creación de array de términos
    terms = []
    for i in range(1, termsnum + 1):
        terms.append("t" + str(i))

    matrix = np.random.rand(len(docnames), len(terms)).round()

    return matrix, docnames, terms

def get_run_process(demo_mode=False):
    _matrix = []
    _docnames = []
    _terms = []

    if demo_mode:
        _matrix, _docnames, _terms = get_demo_data(4, 4)

        _matrix = np.matrix(_matrix)
        _docnames = np.array(_docnames)
        _terms = np.array(_terms)
    else:
        inv_index = InvertedIndexClass()
        _matrix, _docnames, _terms = inv_index.get_data_from_input()

    # Se crea el objeto que albergara el arbol
    tree = RankerTree(_matrix,_docnames,_terms)
    tree.unwrapTree()

    """
    print("Cabeza de arbol: \n{}\nRanking de documentos: \n{}" .format(tree.topNode.matrix, tree.topNode.ranking))
    # Demo controlado para una matriz de 4 x 4
    print("Por la izquierda: \n{} \nPor la derecha: \n{}" .format(tree.topNode.leftNode.matrix, tree.topNode.rightNode.matrix))
    print("Por la izquierda: \n{} \nPor la derecha: \n{}\n".format(tree.topNode.leftNode.leftNode.matrix, tree.topNode.leftNode.rightNode.matrix))
    """

    unordered_runs_count = np.matrix(tree.getRunsData(_matrix)).transpose()
    """
    print(f"Previous Matrix Run Length Histogram.\nMatrix preview\n{_matrix}\nRuns length data\n{unordered_runs_count}\n")
    """
    # ordered_runs_count = tree.getRunsData()
    ordered_runs_count = np.matrix(tree.getRunsData()).transpose()
    print(
    f'Current Matrix Run Length Histogram.\nMatrix preview\n{tree.getOrderedMatrix()}\nRuns length data\n{ordered_runs_count}\n')

    print(f"Valores: {ordered_runs_count[:][0]}")
    plt.subplot(ordered_runs_count[0][:], ordered_runs_count[1][:], color="red", linestyle='solid')
    # plt.scatter(ordered_runs_count.transpose()[0][:], ordered_runs_count.transpose()[1][:])
    # plt.hist(ordered_runs_count, bins='auto')  # arguments are passed to np.histogram
    plt.subplot(unordered_runs_count[0][:], unordered_runs_count[1][:], color="red", linestyle='solid')
    plt.title("Largo de RUNs vs. Cantidad ")
    plt.xlabel("Runs Lenght")
    plt.ylabel("Number")

    plt.show()


if __name__ == "__main__":
    get_run_process(demo_mode=False)

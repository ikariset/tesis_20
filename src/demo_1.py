import numpy as np
from classes.RankerTree import RankerTree
from classes.InvertedIndexFactory import InvertedIndexClass
import matplotlib.pyplot as plt
import argparse


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


def get_run_process(demo_mode=False, store_plot=False, show_plot=False):
    _matrix = []
    _docnames = []
    _terms = []

    if demo_mode:
        _matrix, _docnames, _terms = get_demo_data(40, 40)

        _matrix = np.matrix(_matrix)
        _docnames = np.array(_docnames)
        _terms = np.array(_terms)
    else:
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
    tree.getRunsPlotAndData(store_plot=store_plot, show_plot=show_plot)

    # Creating plot for Unordered Matrix
    tree.getRunsPlotAndData(_matrix, store_plot=store_plot, show_plot=show_plot)

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--demo-mode", help="Activar el Modo Demo", action="store_true")
    parser.add_argument("-p", "--show-plot", help="Mostrar el/los gráficos obtenidos", action="store_true")
    parser.add_argument("-s", "--store-plot", help="Guardar el/los gráficos obtenidos en /output/", action="store_true")
    arg_gui = parser.parse_args()

    get_run_process(demo_mode=(True if arg_gui.demo_mode else False),
                    store_plot=(True if arg_gui.store_plot else False),
                    show_plot=(True if arg_gui.show_plot else False))

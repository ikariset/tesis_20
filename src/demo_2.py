from classes.RankerTree import RankerTree
from classes.InvertedIndexFactory import InvertedIndexClass
import argparse
# import matplotlib.pyplot as plt


def get_run_process(demo_mode=False, store_plot=False, show_plot=False):
    _matrix = []
    _docnames = []
    _terms = []

    if demo_mode is False:
        inv_index = InvertedIndexClass("../../../../data/home7/gov2_completa/", "gov2_completa_urls.txt")
    else:
        inv_index = InvertedIndexClass("../../hola/", "dump_10_lineas.txt")

    _matrix, _docnames, _terms = inv_index.get_data_from_collection()

    # RankerTree Object creation
    tree = RankerTree(_matrix,_docnames,_terms)
    tree.unwrapTree()

    # Creating plot for Ordered Matrix
    #tree.getRunsPlotAndData(store_plot=True)

    # Creating plot for Unordered Matrix
    #tree.getRunsPlotAndData(_matrix, store_plot=True)

    tree.getComparisonPlot(data=_matrix, store_plot=store_plot, show_plot=show_plot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--demo-mode", help="Activar el Modo Demo", action="store_true")
    parser.add_argument("-p", "--show-plot", help="Mostrar el/los gráficos obtenidos",  action="store_true")
    parser.add_argument("-s", "--store-plot", help="Guardar el/los gráficos obtenidos en /output/",  action="store_true")
    arg_gui = parser.parse_args()

    get_run_process(demo_mode=(True if arg_gui.demo_mode else False),
                    store_plot=(True if arg_gui.store_plot else False),
                    show_plot=(True if arg_gui.show_plot else False))

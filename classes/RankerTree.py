import numpy as np, json as js, datetime as dt, time as tm, os, matplotlib.pyplot as plt, pandas as pd
from classes.RankerNode import RankerNode
from pylab import *


# CLASE RANKERTREE - Clase que representa el arbol
class RankerTree:
    def __init__(self, matrix, docnames, terms):
        self.topNode = RankerNode()
        self.topNode.setMatrix(matrix)
        self.topNode.setDocnames(docnames)
        self.topNode.setTerms(terms)

    # Procedimiento para desenvolver la matriz cargada en el nodo principal del arbol, generando todos los nodos hijos de este
    def unwrapTree(self):
        print("Getting Top Node Matrix Ranking...")
        self.topNode.getRanking()
        print("Sorting Top Node Matrix...")
        self.topNode.sortMatrix()
        print("Unwrapping all childs from Top Node Matrix")
        _splitted_matrix, _splitted_docnames = self.topNode.splitMatrix(0)
        self.topNode.setChild(_splitted_matrix, _splitted_docnames, 'left')
        _splitted_matrix, _splitted_docnames = self.topNode.splitMatrix(1)
        self.topNode.setChild(_splitted_matrix, _splitted_docnames, 'right')
        self.topNode.unwrapChilds()
        print("Unwrapping process completed!")

    def getOrderedMatrix(self):
        print("Getting Ordered Matrix from this instance.")
        result = []
        if self.topNode != []:
            result = np.concatenate((self.topNode.leftNode.accessDeepLeaf(), self.topNode.rightNode.accessDeepLeaf()), axis=0)
            print("Ordered Matrix was returned successfully!")
        else:
            print("Top Node is empty. \nPlease assign and unwrap a tree before getting an ordered matrix.")
        return result

    def saveFigToOutput(self, mat_type=None, comparable=False, figdir=None, filename=None):
        foldername = "/output/"
        folderloc = os.path.join(os.path.dirname(__file__), '..')

        print(type(mat_type))
        # print(plottype)
        if figdir is not None and filename is not None:
            foldername = re.sub('((\/|\\\)?(\.\.))+', "", figdir)
            folderloc = os.path.join(os.path.dirname(__file__), re.sub(foldername, "", figdir))

            if not os.path.exists(folderloc):
                os.makedirs(folderloc)

        save_fileloc = folderloc + foldername + ('' if comparable is True else str(mat_type).lower()) + \
                        ('comparison' if comparable is True else '-single') + "-plot-" + \
                        dt.datetime.fromtimestamp(tm.time()).strftime('%Y%m%d-%H%M%S') + ".png"

        plt.savefig(save_fileloc, dpi=100)

    def getRunsData(self, data=[]):
        if data == []:
            matrix_type = "new"
            orderedMatrix = self.getOrderedMatrix().copy()
        else:
            print("Assigning retrieved data to this instance.")
            matrix_type = "old"
            orderedMatrix = data.copy()

        if len(orderedMatrix) > 0:
            runsArray = []
            histogram = []

            # Getting Run Data from Ordered Matrix
            for document in np.asarray(orderedMatrix.transpose()):
                aux = 0
                term_ptr = 0
                for term in np.array(document):
                    if term == 1:
                        aux += 1
                    else:
                        if term_ptr < len(orderedMatrix):
                            runsArray.append(aux)
                            aux = 0

                    term_ptr += 1

                runsArray.append(aux)

            # Removing 0-length Runs
            runsArray = list(filter(lambda a: a != 0, runsArray))

            # Generating Histogram Data
            histogram_json = '{"runCount":['
            for i in range(1, np.max(runsArray) + 1):
                runCount = len(list(filter(lambda a: a == i, runsArray)))
                if runCount > 0:
                    auxHistogram = [i, runCount]
                    histogram_json += '{"length": ' + str(i) + ', "count": ' + str(len(list(filter(lambda a: a == i, runsArray)))) + '},'
                    histogram.append(auxHistogram)

            print("Runs Lenght Histogram data from", 'given Unordered' if data == [] else 'this instance\'s Ordered',
                  'Matrix was created.\n')
        else:
            print("No Ordered Matrix found in this instance. Please check for compatible data.\n")

        # Histogram JSON and output file creation
        histogram_json += ']}'
        normalizer = histogram_json.rfind(",")
        histogram_json = js.loads((histogram_json[0:normalizer] + histogram_json[(normalizer + 1):]))

        # File creation
        current_dir = os.path.join(os.path.dirname(__file__), '..')
        if not os.path.exists(current_dir + "/output/"):
            os.makedirs(current_dir + "/output/")

        output = open(current_dir + "/output/" + matrix_type + "_histogram_data_" + dt.datetime.fromtimestamp(tm.time()).strftime('%Y%m%d_%H%M%S') + ".json", "w")
        output.write(js.dumps(histogram_json, indent=4, sort_keys=False))
        output.close()

        return histogram

    def getRunsPlotAndData(self, data=[], store_plot=False):
        if data == []:
            matrix_type = 'Ordered'
            matrix_color = 'g'
            runsData = np.matrix(self.getRunsData())

        else:
            print("Creating scatterplot using external data.")
            matrix_type = 'Unordered'
            matrix_color = 'b'
            runsData = np.matrix(self.getRunsData(data))

        plotdata = pd.DataFrame(runsData)

        if len(runsData) > 0:
            plt.figure('Run Length Occurrence Scatter (' + matrix_type + ')')
            plt.plot(plotdata[0][0:], plotdata[1][0:], color=matrix_color, linewidth=1.0, linestyle="-")
            plt.scatter(plotdata[0][0:], plotdata[1][0:], linestyle='solid', marker='o', edgecolors=matrix_color, color=matrix_color)
            plt.xlabel("Run Length")
            plt.ylabel("Frequency")
            plt.title("Run Length vs. Frequency")
            if store_plot is True:
                self.saveFigToOutput(matrix_type, comparable=False)

    def getComparisonPlot(self, data=[], store_plot=True):
        if data is not []:
            unord_data = pd.DataFrame(np.matrix(self.getRunsData(data)))
            ord_data = pd.DataFrame(np.matrix(self.getRunsData()))

            if len(unord_data) > 0 and len(ord_data) > 0:
                plt.figure('Run Length Occurrence Scatter (Comparison)')
                unord, = plt.plot(unord_data[0][0:], unord_data[1][0:], color='b', linewidth=1.0, linestyle="-", label='Unsorted Incidence Matrix')
                plt.scatter(unord_data[0][0:], unord_data[1][0:], linestyle='solid', marker='o', edgecolors='b',
                            color='b')
                ord, = plt.plot(ord_data[0][0:], ord_data[1][0:], color='g', linewidth=1.0, linestyle="-", label='Sorted Incidence Matrix')
                plt.scatter(ord_data[0][0:], ord_data[1][0:], linestyle='solid', marker='o', edgecolors='g',
                            color='g')
                plt.xlabel("Run Length")
                plt.ylabel("Frequency")
                plt.title("Run Length vs. Frequency")
                plt.legend(handles=[unord, ord])
                if store_plot is True:
                    self.saveFigToOutput(comparable=True)
        else:
            print("Error!")

# FIN CLASE RANKERTREE - Clase que representa el arbol

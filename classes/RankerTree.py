import numpy as np, json as js, datetime as dt, time as tm, os, matplotlib.pyplot as plt
from classes.RankerNode import RankerNode


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
            histogram = []
            histogram_json = '{"runCount":['
            for i in range(1, np.max(runsArray) + 1):
                runCount = len(list(filter(lambda a: a == i, runsArray)))
                if runCount > 0:
                    auxHistogram = [i, runCount]
                    histogram_json += '{"length": ' + str(i) + ', "count": ' + str(len(list(filter(lambda a: a == i, runsArray)))) + '},'
                    histogram.append(auxHistogram)

            print("Runs Lenght Histogram data from this instance's Ordered Matrix was created.\n")
        else:
            print("No Ordered Matrix found in this instance. Please check for compatible data.\n")
            histogram = []

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


# FIN CLASE RANKERTREE - Clase que representa el arbol

import numpy as np
from classes.RankerNode import RankerNode


# CLASE RANKERTREE - Clase que representa el arbol
class RankerTree:
    def __init__(self, matrix):
        self.topNode = RankerNode()
        self.topNode.setMatrix(matrix)

    # Procedimiento para desenvolver la matriz cargada en el nodo principal del arbol, generando todos los nodos hijos de este
    def unwrapTree(self):
        print("Generando Ranking del Padre...")
        self.topNode.getRanking()
        print("Ordenando las tuplas del Padre...")
        self.topNode.sortMatrix()

        self.topNode.setChild(self.topNode.splitMatrix(0), 'left')
        self.topNode.setChild(self.topNode.splitMatrix(1), 'right')

        self.topNode.unwrapChilds()

    def rank(self, side, symbol):
        # 1. En topNode, revisa en dónde se encuentra el símbolo (el índice)
        print("En construccion")

    def access(self, symbol):
        print("En construccion")

    def select(self, symbol):
        print("En construccion")

    def getOrderedMatrix(self):
        print("Getting Ordered Matrix from this instance.")
        result = []
        if self.topNode != []:
            result = np.concatenate((self.topNode.leftNode.accessDeepLeaf(), self.topNode.rightNode.accessDeepLeaf()), axis=0)
        else:
            print("Top Node is empty. \nPlease assign and unwrap a tree after getting a ordered matrix.")
        return result

    def getRunsData(self, data=[]):
        print("This is data: \n{}" .format(data))
        if data == []:
            orderedMatrix = self.getOrderedMatrix()
        else:
            print("Assigning retrieved data to this instance.")
            orderedMatrix = data

        if len(orderedMatrix) > 0:
            runsArray = []

            # Getting Run Data from Ordered Matrix
            for i in range(0, len(orderedMatrix[:]), 1):
                aux = 0

                for j in range(0, len(orderedMatrix[i]), 1):
                    if orderedMatrix[j][i] == 1:
                        aux += 1
                    else:
                        if j < len(orderedMatrix):
                            runsArray.append(aux)
                            aux = 0

                runsArray.append(aux)

            # Removing 0-length Runs
            runsArray = list(filter(lambda a: a != 0, runsArray))

            # Generating Histogram Data
            histogram = []
            for i in range(1, np.max(runsArray) + 1):
                auxHistogram = [i, len(list(filter(lambda a: a == i, runsArray)))]
                print("Esta es la salida del detalle de runs para {}:\n{}" .format(i, list(filter(lambda a: a == i, runsArray))))
                histogram.append(auxHistogram)

            print("Esta es la salida para el detalle de cada Run leído:\n{}" .format(runsArray))
        else:
            print("No Ordered Matrix found in this instance. Please check for compatible data.\n")
            histogram = []

        return histogram


# FIN CLASE RANKERTREE - Clase que representa el arbol

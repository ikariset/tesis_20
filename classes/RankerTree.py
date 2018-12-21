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
        print("Obteniendo Matrix Ordenada")
        result = []
        if self.topNode != []:
            result = np.concatenate((self.topNode.leftNode.accessDeepLeaf(), self.topNode.rightNode.accessDeepLeaf()), axis=0)
        else:
            print("Top Node is empty. \nPlease assign and unwrap a tree after getting a ordered matrix.")
        return result

    def getRunsData(self, data=[]):
        if data == []:
            orderedMatrix = self.getOrderedMatrix()
        else:
            print("Obteniendo datos de Run con matriz entregada")
            orderedMatrix = data

        print(orderedMatrix)


# FIN CLASE RANKERTREE - Clase que representa el arbol

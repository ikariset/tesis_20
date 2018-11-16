import math, nmap


class RankerNode:
    def __init__(self):
        self.matrix = []
        self.ranking = []
        self.leftNode = RankerNode()
        self.rightNode = RankerNode()

    def setMatrix(self, matrix):
        if matrix != None:
            self.matrix = matrix
            return '1'
        else:
            return '-9'

    def getRanking(self):
        print "loquesea"
        #Procedimiento para generar las sumatorias de existencias

    def sortMatrix(self):
        print "loquesea"
        #Procedimiento para ordenar la matriz en base al ranking generado con getRanking

    def setChild(self, matrix, side):
        #Procedimiento para asignar una matriz a un nodo hijo
        if side == 'left':
            return self.leftNode.setMatrix(matrix)
        elif side == 'right':
            return self.rightNode.setMatrix(matrix)
        else:
            return '-1'

    def splitMatrix(self):
        print "loquesea"
        #Procedimiento para separar las matrices dentro del nodo

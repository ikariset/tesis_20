import math, nmap, numpy
from numpy import ndarray


# CLASE RANKERTREE - Clase que representa el arbol
class RankerTree:
    def __init__(self, matrix):
        self.topNode = RankerNode()
        self.topNode.setMatrix(matrix)

    # Procedimiento para desenvolver la matriz cargada en el nodo principal del arbol, generando todos los nodos hijos de este
    def unwrapTree(self):
        print "Generando Ranking del Padre..."
        self.topNode.getRanking()
        print "Ordenando las tuplas del Padre..."
        self.topNode.sortMatrix()

        self.topNode.setChild(self.topNode.splitMatrix(0), 'left')
        self.topNode.setChild(self.topNode.splitMatrix(1), 'right')

        self.topNode.unwrapChilds()

    # Falta procedimiento para desenvolver los hijos de la derecha y los de la izquierda

# FIN CLASE RANKERTREE - Clase que representa el arbol


# CLASE RANKERNODE - Clase que representara los nodos, utilizando recursividad
class RankerNode:
    def __init__(self):
        self.matrix = []
        self.ranking = []
        self.leftNode = None
        self.rightNode = None

    def setMatrix(self, matrix):
        if matrix.any():
            self.matrix = matrix
            return '1'
        else:
            return '-9'

    # Procedimiento para generar las sumatorias de existencias
    def getRanking(self):
        rank = []

        for i in range(0, len(self.matrix[:]), 1):
            aux = 0
            for j in range(0, len(self.matrix[i]), 1):
                if self.matrix[i][j] == 1:
                    aux += 1

            rank.append(aux)

        self.ranking = rank
        return 1

    # Modificacion de quicksort para aceptar el ranking y la matriz de pertenencia
    def quickSortDocs(self):
        self.quickSortHelper(0, (len(self.ranking) - 1))

    def quickSortHelper(self, first, last):
        if first < last:
            splitpoint = self.partition(first, last)

            self.quickSortHelper(first, (splitpoint - 1))
            self.quickSortHelper((splitpoint + 1), last)

    def partition(self, first, last):
        pivotvalue = self.ranking[first]

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:
            # print ("Sali del while? {}" .format(done))
            while leftmark <= rightmark and self.ranking[leftmark] <= pivotvalue:
                leftmark = leftmark + 1

            while self.ranking[rightmark] >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            # print ("Esto es el marcado por la izquierda: %d" % leftmark)
            # print ("Esto es el marcado por la derecha: %d" % rightmark)

            if rightmark < leftmark:
                done = True
                # print ("Ya sali del while: {}" .format(done))

            else:
                # print ("Estoy en el else:\n--------------------------------RANKING-------------------------------------")
                temp = self.ranking[leftmark]
                # print ("Ranking, valor temporal: {}" .format(temp))
                self.ranking[leftmark] = self.ranking[rightmark]
                # print ("Ranking, valores de punteros izquierda y derecha: {}, {}" .format(self.ranking[leftmark], self.ranking[rightmark]))
                self.ranking[rightmark] = temp
                # print ("Ranking, valores de punteros izquierda y derecha: {}, {}" .format(self.ranking[leftmark], self.ranking[rightmark]))

                # print "--------------------------------MATRIX-------------------------------------"
                temp2 = numpy.array(self.matrix[leftmark])
                # print ("Matrix, valor temporal: {}".format(temp2))
                self.matrix[leftmark] = self.matrix[rightmark]
                # print ("Matrix, valores de punteros izquierda y derecha: {}, {}, {}" .format(self.matrix[leftmark], self.matrix[rightmark], temp2))
                self.matrix[rightmark] = temp2
                # print ("Matrix, valores de punteros izquierda y derecha: {}, {}" .format(self.matrix[leftmark], self.matrix[rightmark]))

        # print "Estoy fuera del while:", "\n", "--------------------------------RANKING-------------------------------------"
        temp = self.ranking[first]
        # print ("Ranking, valor temporal: {}".format(temp))
        self.ranking[first] = self.ranking[rightmark]
        # print ("Ranking, valores de punteros primero y derecha: {}, {}" .format(self.ranking[first], self.ranking[rightmark]))
        self.ranking[rightmark] = temp
        # print ("Ranking, valores de punteros primero y derecha: {}, {}" .format(self.ranking[first], self.ranking[rightmark]))

        # print "--------------------------------MATRIX-------------------------------------"
        temp2 = numpy.array(self.matrix[first])
        # print ("Matrix, valor temporal: {}".format(temp2))
        self.matrix[first] = self.matrix[rightmark]
        # print ("Matrix, valores de punteros primero y derecha: {}, {}" .format(self.matrix[first], self.matrix[rightmark]))
        self.matrix[rightmark] = temp2
        # print ("Matrix, valores de punteros primero y derecha: {}, {}" .format(self.matrix[first], self.matrix[rightmark]))

        return rightmark
    # Fin Mod. de quicksort

    # Procedimiento para ordenar la matriz en base al ranking generado con getRanking
    def sortMatrix(self):
        aux = numpy.array(self.matrix)
        aux2 = numpy.array(self.ranking)
        self.quickSortDocs()

        # print "Matriz, antes:\n", aux, "\n", "despues:\n", self.matrix, "\nRanking, antes: \n", aux2, "\n", "despues:\n", self.ranking

    def setChild(self, matrix, side):
        #Procedimiento para asignar una matriz a un nodo hijo
        if side == 'left':
            self.leftNode = RankerNode()
            return self.leftNode.setMatrix(matrix)
        elif side == 'right':
            self.rightNode = RankerNode()
            return self.rightNode.setMatrix(matrix)
        else:
            return '-1'

    def splitMatrix(self, slice):
        # Para saber si es impar o par la division

        if len(self.matrix[:, 0]) % 2 == 0:
            sublen = len(self.matrix[:, 0]) / 2
        else:
            sublen = (len(self.matrix[:, 0]) + 1) / 2

        print len(self.matrix[0]), len(self.matrix[:, 0]), sublen

        # genera la separacion de la matriz
        if slice == 0:
            print self.matrix[0:(sublen), 0:len(self.matrix[0])]
            return self.matrix[0:(sublen), 0:len(self.matrix[0])]
        elif slice == 1:
            print self.matrix[(sublen):len(self.matrix[:]), 0:len(self.matrix[0])]
            return self.matrix[(sublen):len(self.matrix[:]), 0:len(self.matrix[0])]
        else:
            return '-1'
        #Procedimiento para separar las matrices dentro del nodo

    # Procedimiento para desenrrollar toda la matriz dentro de nodos en el arbol
    def unwrapChilds(self):
        print "Generando Nodo"
        self.getRanking()
        print "Ordenando Matriz de Nodo"
        self.sortMatrix()

        if len(self.matrix) > 1:
            self.setChild(self.splitMatrix(0), 'left')
            self.setChild(self.splitMatrix(1), 'right')

            self.leftNode.unwrapChilds()
            self.rightNode.unwrapChilds()

# FIN CLASE RANKERNODE - Clase que representara los nodos, utilizando recursividad
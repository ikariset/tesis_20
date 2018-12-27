import numpy as np


# CLASE RANKERNODE - Clase que representara los nodos, utilizando recursividad
class RankerNode:
    def __init__(self):
        self.matrix = []
        self.ranking = []
        self.leftNode = None
        self.rightNode = None

    def setMatrix(self, matrix):
        if matrix.any():
            self.matrix = matrix.copy()
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
            while leftmark <= rightmark and self.ranking[leftmark] >= pivotvalue:
                leftmark = leftmark + 1

            while self.ranking[rightmark] <= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True

            else:
                # print ("Estoy en el else:\n--------------------------------RANKING-------------------------------------")
                temp = self.ranking[leftmark]
                # print ("Ranking, valor temporal: {}" .format(temp))
                self.ranking[leftmark] = self.ranking[rightmark]
                # print ("Ranking, valores de punteros izquierda y derecha: {}, {}" .format(self.ranking[leftmark], self.ranking[rightmark]))
                self.ranking[rightmark] = temp
                # print ("Ranking, valores de punteros izquierda y derecha: {}, {}" .format(self.ranking[leftmark], self.ranking[rightmark]))

                # print "--------------------------------MATRIX-------------------------------------"
                temp2 = np.array(self.matrix[leftmark])
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
        temp2 = np.array(self.matrix[first])
        # print ("Matrix, valor temporal: {}".format(temp2))
        self.matrix[first] = self.matrix[rightmark]
        # print ("Matrix, valores de punteros primero y derecha: {}, {}" .format(self.matrix[first], self.matrix[rightmark]))
        self.matrix[rightmark] = temp2
        # print ("Matrix, valores de punteros primero y derecha: {}, {}" .format(self.matrix[first], self.matrix[rightmark]))

        return rightmark
    # Fin Mod. de quicksort

    # Procedimiento para ordenar la matriz en base al ranking generado con getRanking
    def sortMatrix(self):
        aux = np.array(self.matrix)
        aux2 = np.array(self.ranking)
        self.quickSortDocs()

        # print "Matriz, antes:\n", aux, "\n", "despues:\n", self.matrix, "\nRanking, antes: \n", aux2, "\n", "despues:\n", self.ranking

    #Procedimiento para asignar una matriz a un nodo hijo
    def setChild(self, matrix, side):
        if side == 'left':
            self.leftNode = RankerNode()
            return self.leftNode.setMatrix(matrix)
        elif side == 'right':
            self.rightNode = RankerNode()
            return self.rightNode.setMatrix(matrix)
        else:
            return '-1'

    #Procedimiento para separar las matrices dentro del nodo
    def splitMatrix(self, slice):
        # Para saber si es impar o par la division
        # el split que se debe hacer ahora es a partir del promedio del array ranking
        # print("Esto es Ranking {}" .format(self.ranking))
        # value = round(sum(self.ranking)/len(self.ranking))
        # print("Esto es value {}".format(value))
        # split_matrix = [i for i, x in enumerate(self.ranking) if x == value]
        # print("Esto es split_matrix {} y su largo es {}. \nEl medio sería {}".format(split_matrix, len(split_matrix), round(len(split_matrix) / 2)))

        # if len(split_matrix) < 2:
        # sublen = split_matrix[0]
        # else:
        # if len(split_matrix) % 2 == 0:
        # sublen = split_matrix[round((len(split_matrix) / 2))]
        # else:
        # sublen = split_matrix[round((len(split_matrix) + 1) / 2)]

        # Función anterior ==> Separa en la mitad el array
        if len(self.matrix[:, 0]) % 2 == 0:
            sublen = round(len(self.matrix[:, 0]) / 2)
        else:
            sublen = round((len(self.matrix[:, 0]) + 1) / 2)

        # Splitting current node matrix by previously obtained sub-length
        if slice == 0:
            return self.matrix[0:sublen, 0:len(self.matrix[0])]
        elif slice == 1:
            return self.matrix[sublen:len(self.matrix[:]), 0:len(self.matrix[0])]
        else:
            print("Using splitMatrix(slice = {0: upper slice / 1: lower slice})")
            return '-1'

    # Procedimiento para desenrrollar toda la matriz dentro de nodos en el arbol
    def unwrapChilds(self):
        self.getRanking()
        self.sortMatrix()

        if len(self.matrix) > 1:
            self.setChild(self.splitMatrix(0), 'left')
            self.setChild(self.splitMatrix(1), 'right')

            self.leftNode.unwrapChilds()
            self.rightNode.unwrapChilds()

    # Procedimiento para acceder a todos las hojas más profundas del árbol y obtener la matriz que posee esa hoja
    def accessDeepLeaf(self):
        if len(self.matrix) > 1:
            self.leftNode.accessDeepLeaf()
            self.rightNode.accessDeepLeaf()

        return np.array(self.matrix)

# FIN CLASE RANKERNODE - Clase que representara los nodos, utilizando recursividad

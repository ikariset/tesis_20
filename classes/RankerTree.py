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
        print("En construccion")

    def access(self, symbol):
        print("En construccion")

    def select(self, symbol):
        print("En construccion")

# FIN CLASE RANKERTREE - Clase que representa el arbol


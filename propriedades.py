
class Enumerator():
    def __init__(self):
        self.color = [[1, "Yellow"], [2, "Blue"], [3, "Gray"]]
        self.type = [[1, "Hatch"], [2, "Sedan"], [3, "Convertible"]]

    def getColors(self):
        return self.color

    def getCor(self, indice):
        return self.getColors()[indice-1][1]

    def getTypes(self):
        return self.type

    def getTipo(self, indice):
        return self.getTypes()[indice-1][1]

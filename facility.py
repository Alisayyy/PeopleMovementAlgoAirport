import person as person


class Facility:
    def __init__(self, id, name, type, maxOccupancy, medium=5, variance=1):
        self.id = id
        self.name = name
        self.outNeighbor = {}
        self.people = []
        self.type = type
        self.maxOccupancy = maxOccupancy
        self.medium = medium
        self.variance = variance
        self.lastMinNumPeople = 0

    def addOutNeighbor(self, nbrid, weight):
        self.outNeighbor[nbrid] = weight

    def removeOutNeighbor(self, nbrid):
        self.outNeighbor.pop(nbrid)

    def getWeight(self, nbrid):
        return self.outNeighbor[nbrid]



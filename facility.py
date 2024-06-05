import myQueue

class Facility:
    def __init__(self, id, name, type, maxOccupancy=None, medium=None, variance=None):
        self.id = id
        self.name = name
        self.outNeighbor = {} # does not include itself
        self.people = []
        self.type = type
        self.maxOccupancy = maxOccupancy
        self.medium = medium
        self.variance = variance
        self.lastMinNumPeople = 0
        self.peopleInLine = None
        self.timeCounter = None

        if self.type == "Counter" or self.type == "Security":
            self.peopleInLine = myQueue.Queue()
            self.timeCounter = 0

    def addOutNeighbor(self, nbrid, weight):
        self.outNeighbor[nbrid] = weight

    def removeOutNeighbor(self, nbrid):
        self.outNeighbor.pop(nbrid)

    def getWeight(self, nbrid):
        return self.outNeighbor[nbrid]



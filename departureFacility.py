import myQueue
import departurePerson as person

class departureFacility:

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.peopleInLine = myQueue.Queue()
        self.type = type
        self.timeCounter = 0


    # def addOutNeighbor(self, nbrid, weight):
    #     self.outNeighbor[nbrid] = weight
    #
    # def removeOutNeighbor(self, nbrid):
    #     self.outNeighbor.pop(nbrid)
    #
    # def getWeight(self, nbrid):
    #     return self.outNeighbor[nbrid]
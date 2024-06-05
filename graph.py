import facility as facility


class Graph:
    def __init__(self, distanceMap):
        self.facilityList = {}
        self.numFacilities = 0
        self.counter = []
        self.security = []
        self.airportMapDistance = distanceMap

    def addFacility(self, id, name, type, maxOccupancy=None, medium=None, variance=None):
        newFacility = facility.Facility(id, name, type, maxOccupancy, medium, variance)
        self.facilityList[id] = newFacility
        self.numFacilities += 1

    # edge of fid1 to fid2
    def addEdge(self, fid1, fid2, weight):
        self.facilityList[fid1].addOutNeighbor(fid2, weight)

    # edge of fid1 to fid2
    def removeEdge(self, fid1, fid2):
        self.facilityList[fid1].removeOutNeighbor(fid2)

    def connectAllFacilities(self):
        for ids in self.facilityList:
            for nbrids in self.facilityList:
                if nbrids != ids:
                    if self.facilityList[ids].type == 'Counter':
                        if self.facilityList[nbrids].type == 'Security':
                            self.facilityList[ids].addOutNeighbor(nbrids, self.airportMapDistance[ids][nbrids])
                    elif self.facilityList[ids].type == 'Security':
                        if self.facilityList[nbrids].type != 'Counter' and self.facilityList[nbrids].type != 'Security':
                            self.facilityList[ids].addOutNeighbor(nbrids, self.airportMapDistance[ids][nbrids])
                    elif self.facilityList[ids].type == 'BC' or self.facilityList[ids].type == 'Exit':
                        if self.facilityList[nbrids].type == 'BC' or self.facilityList[nbrids].type == 'Exit':
                            self.facilityList[ids].addOutNeighbor(nbrids, self.airportMapDistance[ids][nbrids])
                    else:
                        if self.facilityList[nbrids].type != 'Security' and self.facilityList[nbrids].type != 'Counter':
                            self.facilityList[ids].addOutNeighbor(nbrids, self.airportMapDistance[ids][nbrids])

    def getDistance(self, fid1, fid2):
        return self.airportMapDistance[fid1][fid2]
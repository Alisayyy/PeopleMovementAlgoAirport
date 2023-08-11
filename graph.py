import facility as facility

class Graph:
    def __init__(self, distanceMap):
        self.facilityList = {}
        self.numFacilities = 0
        self.airportMapDistance = distanceMap

    def addFacility(self, id, name, type, maxOccupancy, medium=5, variance=1):
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
                self.facilityList[ids].addOutNeighbor(nbrids, self.airportMapDistance[ids][nbrids])
                self.facilityList[nbrids].addOutNeighbor(ids, self.airportMapDistance[ids][nbrids])

    def getDistance(self, fid1, fid2):
        return self.airportMapDistance[fid1][fid2]
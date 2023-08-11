import random


class Person:

    def __init__(self, id, arrivalTime, FlightID, destination):
        self.id = id
        self.arrivalTime = arrivalTime
        self.enteredTime = 0
        self.exitTime = -1
        self.flightID = FlightID
        self.currentFacility = FlightID
        self.nextFacility = None
        self.destination = destination
        self.movementTrack = []
        # time to be appended as hallway and facility
        self.toBeAppend = [0, 0]
        self.facilityPassed = []
        # only for visualization
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))




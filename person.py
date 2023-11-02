import random
import config as cg

class Person:

    def __init__(self, id, destination, currentFacility=None, arrivalTime=None, checked=None, departureTime=None, enteredTime = None):
        self.id = id
        self.enteredTime = enteredTime
        self.exitTime = None
        #self.flightID = flightID
        self.speed = random.randint(cg.minWalkingSpeed, cg.maxWalkingSpeed)


        self.currentFacility = currentFacility
        self.nextFacility = None
        self.destination = destination
        self.movementTrack = []
        self.toBeAppend = [0, 0]  # time to be appended as hallway and facility
        self.facilityPassed = set()

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # for visualization

        # specific to arrival
        self.arrivalTime = arrivalTime

        # specific to departure
        self.checked = checked
        self.departureTime = departureTime

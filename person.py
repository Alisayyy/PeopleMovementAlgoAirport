import random
import config as config

class Person:

    def __init__(self, id, destination, currentFacility=None, arrivalTime=None, checked=None, departureTime=None):
        self.id = id
        self.enteredTime = None
        self.exitTime = None
        #self.flightID = flightID

        self.currentFacility = currentFacility
        self.nextFacility = None
        self.destination = destination
        self.movementTrack = []
        self.toBeAppend = [0, 0]  # time to be appended as hallway and facility
        self.facilityPassed = []

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # for visualization

        # specific to arrival
        self.arrivalTime = arrivalTime

        # specific to departure
        self.checked = checked
        self.departureTime = departureTime

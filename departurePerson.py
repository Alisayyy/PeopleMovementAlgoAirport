import random
import config as config

class departurePerson():

    def __init__(self, id):
        self.id = id
        self.enteredTime = random.randint(0, 50)
        self.currentFacility = None
        self.checked = random.random() > (1 - config.rate_self_checked)
        self.movementTrack = []


        # self.arrivalTime = arrivalTime
        # self.enteredTime = 0
        # self.exitTime = -1
        # self.flightID = FlightID
        # self.currentFacility = FlightID
        # self.nextFacility = None
        # self.destination = destination
        # self.movementTrack = []
        # # time to be appended as hallway and facility
        # self.toBeAppend = [0, 0]
        # self.facilityPassed = []
        # self.departureTime = departureTime
        # # only for visualization
        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
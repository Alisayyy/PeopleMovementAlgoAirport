# pygame visualization
backgroundColor = (230, 230, 230)
textColor = (0, 0, 0)
textSize = 25
personRadius = 5
facilityBoxSize = 38


# departure
rate_self_checked = 0.1
check_time = 2 # min
security_time = 4 # min
maxBefore = 200 # if the plane departures at t, earliest person will come to airport at t-200
minBefore = 100 # if the plane departures at t, latest person will come to airport at t-100
boardingTime = 30 # min before departure time
boardingDecisionTime = 40


# arrival
num_people_off_plane = 15  # per min


# flight info
# flightId : [Arrival("A"), Gate, Time, numPassenger, ExitId, connectedInfo(connectedFlightId: numConnected)]
# flightId : Departure("D"), Gate, Time, total number of passengers, number of passengers not from connects]
flightInfo = {
    1: ["A", 0, 0, 150, 12, {3: 50}],
    2: ["A", 1, 30, 200, 12, {3: 10}],
    3: ["D", 1, 230, 150, 90]
}

# airport map info
mapWidth = 600
mapLength = 800
# id: [name, type, X, Y, maxOccupancy, medium, variance]
facilityInfo = {
    0:  ['gate1',          'Gate',      30,  350, 500,   60,  16],
    1:  ['gate2',          'Gate',      280, 550, 500,   60,  16],
    2:  ['restroom1',      'Restroom',  130, 350, 20,    3,  1],
    3:  ['restaurant1',    'Food',      280, 350, 50,    15, 4],
    4:  ['store1',         'Shopping',  380, 350, 10,    3,  1],
    5:  ['restaurant2',    'Food',      450, 350, 20,    10, 4],
    6:  ['restroom2',      'Restroom',  550, 350, 10,    2,  1],
    7:  ['restroom3',      'Restroom',  280, 480, 15,    2,  1],
    8:  ['store2',         'Shopping',  380, 220, 15,    5,  1],
    9:  ['restaurant3',    'Food',      450, 280, 40,    10, 4],
    10: ['baggage claim1', 'BC',        670, 290, 300,   20, 4],
    11: ['baggage claim2', 'BC',        670, 390, 300,   19, 4],
    12: ['exit',           'Exit',      750, 350, 10000, 0,  0],
    13: ['counter1',       'Counter',   190, 50,  None,   None,  None],
    14: ['counter2',       'Counter',   270, 50,  None,   None,  None],
    15: ['counter3',       'Counter',   350, 50,  None,   None,  None],
    16: ['security1',      'Security',  190, 150, None,   None,  None],
    17: ['security2',      'Security',  270, 150, None,   None,  None],
    18: ['security3',      'Security',  350, 150, None,   None,  None]
}


# weight of different factors when calculating the next facility
weight_1 = 0.1 # distance between current and next facility
weight_2 = 0.7 # distance between next facility and destination
weight_3 = 0.1 # facility type
weight_4 = 0.1 # occupancy of current and next facility


# person speed
minWalkingSpeed = 30
maxWalkingSpeed = 40




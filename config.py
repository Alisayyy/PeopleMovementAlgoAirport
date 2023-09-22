# airport map info
mapWidth = 600
mapLength = 800
distanceMap = [[0, 7, 1, 6, 9, 11, 13, 6, 13, 12, 18, 19, 21, 15, 15, 15],
               [7, 0, 6, 4, 7, 9, 11, 1, 12, 10, 16, 17, 19, 16, 16, 16],
               [1, 6, 0, 5, 8, 10, 12, 4, 10, 9, 17, 18, 20, 14, 14, 14],
               [6, 4, 5, 0, 3, 5, 7, 3, 3, 4, 12, 13, 15, 10, 10, 10],
               [9, 7, 8, 3, 0, 2, 4, 4, 5, 2, 9, 10, 12, 6, 6, 6],
               [11, 9, 10, 5, 2, 0, 2, 7, 6, 1, 7, 8, 10, 8, 8, 8],
               [13, 11, 12, 7, 4, 2, 0, 8, 6, 1, 5, 6, 8, 9, 9, 9],
               [6, 1, 4, 3, 4, 7, 8, 0, 11, 13, 15, 16, 18, 5, 5, 5],
               [13, 12, 10, 3, 5, 6, 6, 11, 0, 3, 14, 15, 17, 2, 2, 2],
               [12, 10, 9, 4, 2, 1, 1, 13, 3, 0, 8, 9, 11, 4, 4, 4],
               [18, 16, 17, 12, 9, 7, 5, 15, 14, 8, 0, 1, 2, 0, 0, 0],
               [19, 17, 18, 13, 10, 8, 6, 16, 15, 9, 1, 0, 2, 0, 0, 0],
               [21, 19, 20, 15, 12, 10, 8, 18, 17, 11, 2, 2, 0, 0, 0, 0],
               [15, 16, 14, 10, 6, 8, 9, 5, 2, 4, 0, 0, 0, 0, 0, 0],
               [15, 16, 14, 10, 6, 8, 9, 5, 2, 4, 0, 0, 0, 0, 0, 0],
               [15, 16, 14, 10, 6, 8, 9, 5, 2, 4, 0, 0, 0, 0, 0, 0]]



# departure
rate_self_checked = 0.1
check_time = 3 # min
security_time = 5 # min

# arrival
num_people_off_plane = 15  # per min

# id: [name, type, X, Y, maxOccupancy, medium, variance]
facilityInfo = {
    0:  ['gate1',          'Gate',      30,  350, 500,   0,  0],
    1:  ['gate2',          'Gate',      280, 550, 500,   0,  0],
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

facilityBoxSize = 38
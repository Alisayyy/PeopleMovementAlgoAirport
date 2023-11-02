import person as person
import graph as g
import random
import numpy as np
import pygame
import config as cg
import math


def buildMap():
    # calculate distance map according to user input
    numFacilities = len(cg.facilityInfo)
    distanceMap = np.arange(numFacilities * numFacilities).reshape(numFacilities,numFacilities)
    for i in range(numFacilities):
        for j in range(i, numFacilities):
            x1 = cg.facilityInfo[i][2]
            y1 = cg.facilityInfo[i][3]
            x2 = cg.facilityInfo[j][2]
            y2 = cg.facilityInfo[j][3]
            d = int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))
            distanceMap[i][j] = d
            distanceMap[j][i] = d
    # initialize airport map and all facilities
    airportMap = g.Graph(distanceMap)

    for i in range(numFacilities):
        airportMap.addFacility(i, cg.facilityInfo[i][0], cg.facilityInfo[i][1],
                               cg.facilityInfo[i][4], cg.facilityInfo[i][5],
                               cg.facilityInfo[i][6])
        if cg.facilityInfo[i][1] == 'Counter':
            airportMap.counter.append(airportMap.facilityList[i])
        elif cg.facilityInfo[i][1] == 'Security':
            airportMap.security.append(airportMap.facilityList[i])

    airportMap.connectAllFacilities()

    # # print connectivity info
    # for fa in airportMap.facilityList:
    #     print("Facility Name: ", airportMap.facilityList[fa].name)
    #     print("Out Neighbour: ", end=" ")
    #     for nfa in airportMap.facilityList[fa].outNeighbor:
    #         print(airportMap.facilityList[nfa].name, end=" ")
    #     print("\n")
    return airportMap


def number_of_certain_probability(sequence, probability):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(sequence, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def calTimeSpent(medium, variance):
    return abs(int(np.random.normal(medium, variance))) + 1


def normalize(probList):
    sumofProb = sum(probList)
    for i in range(len(probList)):
        probList[i] = probList[i] / sumofProb
    return probList


def compute_next_location(person, airportMap, t):
    sequence = []
    currentFacility = airportMap.facilityList[person.currentFacility]
    prob_a = []
    prob_b = []
    prob_c = []
    prob_d = []

    if person.departureTime is not None:
        if person.departureTime - t <= cg.boardingTime:
            person.nextFacility = person.destination
            person.toBeAppend[0] = int(
                airportMap.getDistance(person.currentFacility, person.nextFacility) / person.speed)
            person.toBeAppend[1] = person.departureTime - t
            return

    for id in currentFacility.outNeighbor:
        sequence.append(id)
        nextFacility = airportMap.facilityList[id]
        # distance between current and next facility
        prob_a.append(1 / airportMap.getDistance(person.currentFacility, id))

        # distance between next facility and destination
        if id == person.destination:
            prob_b.append(1)
        else:
            prob_b.append(1 / airportMap.getDistance(id, person.destination))

        # facility type
        if nextFacility.type == 'Gate' and id != person.destination:
            prob_c.append(0)
        elif person.departureTime is not None and (nextFacility.type == 'BC' or nextFacility.type == 'Exit'):
            prob_c.append(0)
        elif nextFacility.type == currentFacility.type:
            prob_c.append(0.1)
        else:
            prob_c.append(1)

        # occupancy of current and next facility
        prob_d.append(abs(nextFacility.lastMinNumPeople - nextFacility.maxOccupancy) / nextFacility.maxOccupancy)

        # f. probability of staying (a function of ...)

        # e. override all other prob
        # 1- (exit time - current time) / (exit time - entered time), hop to next
        # set all previous facilities to zero, set the remaining to be prob * (1/distance)

    prob_a = normalize(prob_a)
    prob_b = normalize(prob_b)
    prob_c = normalize(prob_c)
    prob_d = normalize(prob_d)

    # combining all factors into one probability list
    length = len(sequence)
    final_prob = []
    for i in range(length):
        if prob_a[i] == 0 or prob_b[i] == 0 or prob_c[i] == 0 or prob_a[i] == 0:
            # or sequence[i] in person.facilityPassed
            final_prob.append(0)
        else:
            final_prob.append(cg.weight_1*prob_a[i] + cg.weight_2*prob_b[i] + cg.weight_3*prob_c[i] + cg.weight_4*prob_d[i])

    if sum(final_prob) != 0:

        final_prob = normalize(final_prob)

        # choose the nextFacility based on probability list
        person.nextFacility = random.choices(sequence, final_prob)[0]
        if person.nextFacility != person.destination:
            person.facilityPassed.add(person.nextFacility)
        nextFacility = airportMap.facilityList[person.nextFacility]
    else:
        print("here")
        person.nextFacility =person.destination
        nextFacility = airportMap.facilityList[person.nextFacility]


    person.toBeAppend[0] = int(airportMap.getDistance(person.currentFacility, person.nextFacility) / person.speed)
    person.toBeAppend[1] = calTimeSpent(nextFacility.medium, nextFacility.variance)
    return


def plotFacilities():
    for i in range(len(cg.facilityInfo)):
        screen.blit(myfont.render(cg.facilityInfo[i][0], True, (255, 0, 0)),
                    (cg.facilityInfo[i][2], cg.facilityInfo[i][3] - 20))
        pygame.draw.rect(screen, [255, 0, 0], [cg.facilityInfo[i][2], cg.facilityInfo[i][3],
                                               cg.facilityBoxSize, cg.facilityBoxSize], 2)

def plotPersonPosition(currentPosition):
    if currentPosition != -1:
        pygame.draw.circle(screen, person.color, (cg.facilityInfo[currentPosition][2] + cg.facilityBoxSize/2 + random.randint(-15, 15),
                                                  cg.facilityInfo[currentPosition][3] + cg.facilityBoxSize/2 + random.randint(-15, 15)),
                           cg.personRadius)


def print_person_info(person):
    print('id = ', person.id)
    print('entered time = ', person.enteredTime)
    print('exit time = ', person.exitTime)
    print('departure time = ', person.departureTime)
    print(person.movementTrack)
    print('length of movementTrack = ', len(person.movementTrack))
    print('current location = ', person.currentFacility)
    print('destination = ', person.destination)
    print('next facility = ', person.nextFacility)
    print('facilities passed = ', person.facilityPassed)
    print('\n')


def createPopulation():
    populationFront, populationMain, removedPopulation = [], [], []
    c = 0

    for flightId, flightInfo in cg.flightInfo.items():
        flag, gate, time, totalPassenger = flightInfo[0], flightInfo[1], flightInfo[2], flightInfo[3]

        # arrival flights
        if flag == 'A':
            cBeforeCurrent = c
            exitId= flightInfo[4]
            numConnected = 0
            if len(flightInfo) == 6:
                connectedInfo = flightInfo[5]
                for key, value in connectedInfo.items():
                    for i in range(c, c+value):
                        populationMain.append(person.Person(i, cg.flightInfo[key][1], currentFacility=gate,
                                                            arrivalTime=time, departureTime=cg.flightInfo[key][2],
                                                            enteredTime=time + int((i-cBeforeCurrent)/cg.num_people_off_plane)))
                    c += value
                    numConnected += value
            for i in range(c, c + totalPassenger - numConnected):
                populationMain.append(person.Person(i, exitId, currentFacility=gate, arrivalTime=time,
                                                    enteredTime=time + int((i-cBeforeCurrent)/cg.num_people_off_plane)))
            c += totalPassenger - numConnected

        # departure flights
        else:
            numPassengerNotConnected = flightInfo[4]
            for i in range(c, c+numPassengerNotConnected):
                checked = random.random() > (1 - cg.rate_self_checked)
                enteredTime = random.randint(time-cg.maxBefore, time-cg.minBefore)
                populationFront.append(person.Person(i, gate, checked=checked, departureTime=time, enteredTime= enteredTime))
            c += numPassengerNotConnected

    return populationFront, populationMain, removedPopulation


def findLeastCounter(counter):
    least = counter[0]
    for c in counter:
        if c.peopleInLine.size() < least.peopleInLine.size():
            least = c
    return least


def findLeastSecurity(security):
    least = security[0]
    for s in security:
        if s.peopleInLine.size() < least.peopleInLine.size():
            least = s
    return least


if __name__ == '__main__':
    airportMap = buildMap()
    populationFront, populationMain, removedPopulation = createPopulation()

    t = 0
    for t in range(300):
        # front
        for person in populationFront:
            if t >= person.enteredTime:
                if person.currentFacility == None and not person.checked:
                    c = findLeastCounter(airportMap.counter)
                    c.peopleInLine.enqueue(person)
                    person.currentFacility = c.id
                elif person.currentFacility == None and person.checked:
                    s = findLeastSecurity(airportMap.security)
                    s.peopleInLine.enqueue(person)
                    person.currentFacility = s.id
                person.movementTrack.append(person.currentFacility)

        # process each counter
        for c in airportMap.counter:
            if not c.peopleInLine.empty():
                c.timeCounter += 1
                if c.timeCounter == cg.check_time:
                    person = c.peopleInLine.dequeue()
                    person.currentFacility = None
                    person.checked = True
                    c.timeCounter = 0
        # process each security
        for s in airportMap.security:
            if not s.peopleInLine.empty():
                s.timeCounter += 1
                if s.timeCounter == cg.security_time:
                    person = s.peopleInLine.dequeue()
                    populationMain.append(person)
                    populationFront.remove(person)
                    s.timeCounter = 0

        # main
        for facility in airportMap.facilityList:
            airportMap.facilityList[facility].lastMinNumPeople = len(airportMap.facilityList[facility].people)
            airportMap.facilityList[facility].people = []

        for person in populationMain:
            if t >= person.enteredTime:
                # still in hallway
                if person.toBeAppend[0] != 0:
                    person.currentFacility = -1
                    person.toBeAppend[0] -= 1
                else:
                    if person.toBeAppend[1] != 0:
                        if person.nextFacility is not None:
                            person.currentFacility = person.nextFacility
                            person.nextFacility = None
                        person.toBeAppend[1] -= 1
                    # if person.currentFacility != 12 and person.currentFacility != person.destination and person.toBeAppend[1] == 0:
                    # if person.currentFacility != person.destination and person.toBeAppend[1] == 0:
                    if airportMap.facilityList[person.currentFacility].type != 'Exit' and person.toBeAppend[1] == 0:
                        compute_next_location(person, airportMap, t)

                # append current position
                person.movementTrack.append(person.currentFacility)

                if person.currentFacility != -1:
                    airportMap.facilityList[person.currentFacility].people.append(person.id)

                if person.currentFacility == person.destination:
                    if airportMap.facilityList[person.destination].type == 'Exit':
                        person.exitTime = t
                        person.toBeAppend[0] = 0
                        person.toBeAppend[1] = 0
                        removedPopulation.append(person)

                    elif airportMap.facilityList[person.destination].type == 'Gate' and person.departureTime - t <= 30:
                        if person.exitTime is None:
                            person.exitTime = random.randint(t, person.departureTime)
                            person.toBeAppend[1] = person.exitTime - t
                        if person.exitTime == t:
                            removedPopulation.append(person)


        for person in removedPopulation:
            if person in populationMain:
                populationMain.remove(person)

    for person in removedPopulation:
        print_person_info(person)

    print('populationFront: ', len(populationFront))
    print('populationMain: ', len(populationMain))
    print('removedPopulation:', len(removedPopulation))


    pygame.init()
    screen = pygame.display.set_mode((cg.mapLength, cg.mapWidth))
    bg_color = cg.backgroundColor

    pygame.display.set_caption("Airport Map")
    keep_going = True
    personRadius = cg.personRadius
    myfont = pygame.font.Font(None, cg.textSize)
    t = 0

    while keep_going:
        screen.fill(bg_color)
        plotFacilities()
        screen.blit(myfont.render('t = ', True, cg.textColor), (10, 10))
        screen.blit(myfont.render(str(t), True, cg.textColor), (36, 10))

        for person in removedPopulation:
            if person.enteredTime <= t <= person.exitTime:
                currentPosition = person.movementTrack[t-person.enteredTime]
                plotPersonPosition(currentPosition)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        pygame.display.update()
        pygame.time.delay(300)
        t += 1

    pygame.quit()

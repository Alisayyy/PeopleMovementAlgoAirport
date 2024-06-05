import csv
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

    return airportMap


def setInfected():
    probability = random.random()
    if probability <= cg.percentageInfected:
        return 1
    else:
        return 0


def createPopulation():
    populationFront, populationMain, removedPopulation, populationFtoM, initialInfected = [], [], [], [], []
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
                        infect = setInfected()
                        populationMain.append(person.Person(i, cg.flightInfo[key][1], infected=infect, currentFacility=gate,
                                                            arrivalTime=time, departureTime=cg.flightInfo[key][2],
                                                            enteredTime=time + int((i-cBeforeCurrent)/cg.num_people_off_plane)))
                        if infect:
                            initialInfected.append(populationMain[-1])
                    c += value
                    numConnected += value
            for i in range(c, c + totalPassenger - numConnected):
                infect = setInfected()
                populationMain.append(person.Person(i, exitId, infected=infect, currentFacility=gate, arrivalTime=time,
                                                    enteredTime=time + int((i-cBeforeCurrent)/cg.num_people_off_plane)))
                if infect:
                    initialInfected.append(populationMain[-1])
            c += totalPassenger - numConnected

        # departure flights
        else:
            numPassengerNotConnected = flightInfo[4]
            for i in range(c, c+numPassengerNotConnected):
                infect = setInfected()
                checked = random.random() > (1 - cg.rate_self_checked)
                enteredTime = random.randint(time-cg.maxBefore, time-cg.minBefore)
                populationFront.append(person.Person(i, gate, infected=infect, checked=checked, departureTime=time, enteredTime= enteredTime))
                if infect:
                    initialInfected.append(populationFront[-1])
            c += numPassengerNotConnected

    return populationFront, populationMain, removedPopulation, populationFtoM, initialInfected


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
        # Force person to go to destination if within certain minutes of departure
        if person.departureTime - t <= cg.boardingDecisionTime:
            person.nextFacility = person.destination
            person.toBeAppend[0] = int(
                airportMap.getDistance(person.currentFacility, person.nextFacility) / person.speed)
            person.toBeAppend[1] = person.departureTime - t
            return

    for id in currentFacility.outNeighbor:
        sequence.append(id)
        nextFacility = airportMap.facilityList[id]

        # a. distance between current and next facility
        prob_a.append(1 / airportMap.getDistance(person.currentFacility, id))

        # b. distance between next facility and destination
        if id == person.destination:
            prob_b.append(1)
        else:
            prob_b.append(1 / airportMap.getDistance(id, person.destination))

        # c. facility type
        if nextFacility.type == 'Gate' and id != person.destination:
            prob_c.append(0)
        elif person.departureTime is not None and (nextFacility.type == 'BC' or nextFacility.type == 'Exit'):
            prob_c.append(0)
        elif nextFacility.type == currentFacility.type:
            prob_c.append(0.1)
        else:
            prob_c.append(1)

        # d. occupancy of current and next facility
        prob_d.append(abs(nextFacility.lastMinNumPeople - nextFacility.maxOccupancy) / nextFacility.maxOccupancy)

        # TODO: Other factors?

    prob_a = normalize(prob_a)
    prob_b = normalize(prob_b)
    prob_c = normalize(prob_c)
    prob_d = normalize(prob_d)

    # combining all factors into one probability list
    length = len(sequence)
    final_prob = []
    for i in range(length):
        if prob_a[i] == 0 or prob_b[i] == 0 or prob_c[i] == 0 or prob_a[i] == 0:
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
        person.nextFacility =person.destination
        nextFacility = airportMap.facilityList[person.nextFacility]

    person.toBeAppend[0] = int(airportMap.getDistance(person.currentFacility, person.nextFacility) / person.speed)
    person.toBeAppend[1] = calTimeSpent(nextFacility.medium, nextFacility.variance)
    return


# Convert data to a format that the infectious model takes in
def DataFormatConverter(initialInfected, removedPopulation):
    facilityInfectedTime = {}
    peopleFacilityTime = {}
    # create facilityInfectedTime
    for person in initialInfected:
        currentFacility = None
        enterTime = None
        for i, facility_id in enumerate(person.movementTrack):
            if facility_id == -1:
                if currentFacility is not None:
                    facilityInfectedTime.setdefault(currentFacility, []).append((enterTime, i + person.enteredTime))
                    currentFacility = None
            else:
                if currentFacility is None:
                    currentFacility = facility_id
                    enterTime = i + person.enteredTime
        if currentFacility is not None:
            facilityInfectedTime.setdefault(currentFacility, []).append(
                (enterTime, len(person.movementTrack) + person.enteredTime))

    # create peopleFacilityTime
    for person in removedPopulation:
        if person not in initialInfected:
            peopleFacilityTime.setdefault(person.id, {})

            currentFacility = None
            enterTime = None
            for i, facility_id in enumerate(person.movementTrack):
                if facility_id == -1:
                    if currentFacility is not None:
                        peopleFacilityTime[person.id].setdefault(currentFacility, []).append(
                            (enterTime, i + person.enteredTime))
                        currentFacility = None
                else:
                    if currentFacility is None:
                        currentFacility = facility_id
                        enterTime = i + person.enteredTime
            if currentFacility is not None:
                peopleFacilityTime[person.id].setdefault(currentFacility, []).append(
                    (enterTime, len(person.movementTrack) + person.enteredTime))

    with open("formatted_data.py", "w") as f:
        f.write("facilityInfectedTime = {\n")
        for facility_id, infected_times in facilityInfectedTime.items():
            f.write(f"    {facility_id}: {infected_times},\n")
        f.write("}\n\n")

        f.write("peopleFacilityTime = {\n")
        for person_id, visited_facilities in peopleFacilityTime.items():
            f.write(f"    {person_id}: {visited_facilities},\n")
        f.write("}\n")


def plotFacilities(screen, myfont):
    for i in range(len(cg.facilityInfo)):
        screen.blit(myfont.render(cg.facilityInfo[i][0], True, (255, 0, 0)),
                    (cg.facilityInfo[i][2], cg.facilityInfo[i][3] - 20))
        pygame.draw.rect(screen, [255, 0, 0], [cg.facilityInfo[i][2], cg.facilityInfo[i][3],
                                               cg.facilityBoxSize, cg.facilityBoxSize], 2)

def plotPersonPosition(screen, person, currentPosition):
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


def run_simulation(pygameFlag, exportData, errorCheckingFlag):
    airportMap = buildMap()

    # initialize passengers based on flight information
    populationFront, populationMain, removedPopulation, populationFtoM, initialInfected = createPopulation()
    numMissedPlane = 0
    # default saved data
    timeFacilityPeopleList = {}

    t = 0
    for t in range(cg.runningTimesteps):
        timeFacilityPeopleList[t] = {}

        # count the number of people in each facility in the previous timestep
        # and clear people list to create new one for this timestep
        for facility in airportMap.facilityList:
            airportMap.facilityList[facility].lastMinNumPeople = len(airportMap.facilityList[facility].people)
        airportMap.facilityList[facility].people = []

        # Counter and Security area
        # every person must go through security, and have a probability of going to check bag or not
        # assume every person will find the counter/security with the least number of people in line
        for person in populationFront:
            if t >= person.enteredTime:
                # find counter
                if person.currentFacility == None and not person.checked:
                # find a counter and get in queue
                    c = findLeastCounter(airportMap.counter)
                    c.peopleInLine.enqueue(person)
                    person.currentFacility = c.id
                # find security
                elif person.currentFacility == None and person.checked:
                # find a security and get in queue
                    s = findLeastSecurity(airportMap.security)
                    s.peopleInLine.enqueue(person)
                    person.currentFacility = s.id
                person.movementTrack.append(person.currentFacility)

                if person.currentFacility is not None and person.currentFacility != -1:
                    airportMap.facilityList[person.currentFacility].people.append(person.id)

        # process the queue of each counter
        for c in airportMap.counter:
            if not c.peopleInLine.empty():
                c.timeCounter += 1
                if c.timeCounter == cg.check_time:
                    person = c.peopleInLine.dequeue()
                    person.currentFacility = None
                    person.checked = True
                    c.timeCounter = 0
        # process the queue of each security
        for s in airportMap.security:
            if not s.peopleInLine.empty():
                s.timeCounter += 1
                if s.timeCounter == cg.security_time:
                    person = s.peopleInLine.dequeue()
                    populationFtoM.append(person)
                    s.timeCounter = 0

        # Main departure hall
        for person in populationMain:
            if t >= person.enteredTime:
                # walking in the hallway to get to the next facility
                if person.toBeAppend[0] != 0:
                    person.currentFacility = -1
                    person.toBeAppend[0] -= 1
                # spending time inside a facility
                else:
                    if person.toBeAppend[1] != 0:
                        if person.nextFacility is not None:
                            person.currentFacility = person.nextFacility
                            person.nextFacility = None
                        person.toBeAppend[1] -= 1
                    if airportMap.facilityList[person.currentFacility].type != 'Exit' and person.toBeAppend[1] == 0:
                        compute_next_location(person, airportMap, t)

                # append current position
                person.movementTrack.append(person.currentFacility)

                # when person arrive at their assigned destination
                if person.currentFacility == person.destination:
                    if airportMap.facilityList[person.destination].type == 'Exit':
                        person.exitTime = t
                        person.toBeAppend[0] = 0
                        person.toBeAppend[1] = 0
                        removedPopulation.append(person)

                    elif airportMap.facilityList[person.destination].type == 'Gate':
                        if person.departureTime < t:
                            removedPopulation.append(person)
                            numMissedPlane += 1
                        elif person.departureTime - t <= 30:
                            if person.exitTime is None:
                                person.exitTime = random.randint(t, person.departureTime)
                                person.toBeAppend[1] = person.exitTime - t
                            if person.exitTime == t:
                                removedPopulation.append(person)
                        else:
                            pass

                if person.currentFacility != -1:
                    airportMap.facilityList[person.currentFacility].people.append(person.id)

        for f in airportMap.facilityList:
            timeFacilityPeopleList[t][f] = airportMap.facilityList[f].people

        for person in removedPopulation:
            if person in populationMain:
                populationMain.remove(person)
        for person in populationFtoM:
            populationMain.append(person)
            populationFront.remove(person)
        populationFtoM= []

    print('number of passengers missed the flight:', numMissedPlane)
    print('populationFront: ', len(populationFront))
    print('populationMain: ', len(populationMain))
    print('removedPopulation:', len(removedPopulation))

    if errorCheckingFlag:
        errorCounter = 0
        for person in removedPopulation:
            if person.exitTime - person.enteredTime + 1 != len(person.movementTrack):
                print_person_info(person)
                errorCounter += 1
        print(errorCounter)

    if exportData:
        with open('movementTrack.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['ID', 'enteredTime', 'movementTrack', 'exitTime'])
            for person in removedPopulation:
                csv_writer.writerow([person.id, person.enteredTime, person.movementTrack, person.exitTime])
                # print_person_info(person)

        DataFormatConverter(initialInfected, removedPopulation)

    # pygame visualization
    if pygameFlag:
        pygame.init()
        screen = pygame.display.set_mode((cg.mapLength, cg.mapWidth))
        bg_color = cg.backgroundColor

        pygame.display.set_caption("Airport Map")
        keep_going = True
        myfont = pygame.font.Font(None, cg.textSize)

        while keep_going:
            screen.fill(bg_color)
            plotFacilities(screen, myfont)
            screen.blit(myfont.render('t = ', True, cg.textColor), (10, 10))
            screen.blit(myfont.render(str(t), True, cg.textColor), (36, 10))

            for person in removedPopulation:
                if person.enteredTime <= t <= person.exitTime:
                    currentPosition = person.movementTrack[t - person.enteredTime]
                    plotPersonPosition(screen, person, currentPosition)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
            pygame.display.update()
            pygame.time.delay(300)

        pygame.quit()


if __name__ == '__main__':
    pygameFlag = True
    exportData = True
    errorCheckingFlag = False
    run_simulation(pygameFlag, exportData, errorCheckingFlag)

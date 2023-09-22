import person as person
import facility as facility
import graph as g
import random
import numpy as np
import matplotlib.pyplot as plt
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

    # need a better way of removing edges
    airportMap.connectAllFacilities()

    # remove connection from main to front facilities
    for i in range(0, 13):
        for j in range(13, 19):
            airportMap.removeEdge(i, j)
    # remove connection from counter to main
    for i in range(0, 16):
        airportMap.removeEdge(13, i)
        airportMap.removeEdge(14, i)
        airportMap.removeEdge(15, i)
    # remove connection from security to counter
    for i in range(13, 19):
        airportMap.removeEdge(16, i)
        airportMap.removeEdge(17, i)
        airportMap.removeEdge(18, i)
    for i in range(0, 10):
        airportMap.removeEdge(10, i)
    airportMap.removeEdge(10, 11)
    for i in range(0, 11):
        airportMap.removeEdge(11, i)
    for i in range(0, 12):
        airportMap.removeEdge(12, i)
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
    for id in currentFacility.outNeighbor:
        sequence.append(id)
        nextFacility = airportMap.facilityList[id]
        # distance between current and next facility
        if id != person.currentFacility:
            prob_a.append(1/airportMap.getDistance(person.currentFacility, id))
        else:
            prob_a.append(0)

        # distance between next facility and destination
        if id == person.destination:
            prob_b.append(1)
        elif id != person.currentFacility:
            prob_b.append(1 / airportMap.getDistance(id, person.destination))
        else:
            prob_b.append(0)

        # facility type
        if nextFacility.type == 'Gate' and id != person.destination:
            prob_c.append(0)
        elif nextFacility.type == currentFacility.type:
            prob_c.append(0.1)
        else:
            prob_c.append(1)

        if nextFacility.maxOccupancy == None:
            print(currentFacility.name)
            print(nextFacility.name)
        # occupancy of current and next facility
        prob_d.append(abs(nextFacility.lastMinNumPeople - nextFacility.maxOccupancy) / nextFacility.maxOccupancy)

        # f. probability of staying (a function of ...)

        # e. override all other prob
        # 1- (exit time - current time) / (exit time - entered time), hop to next
        # set all previous facilities to zero, set the remaining to be prob * (1/distance)

    if sum(prob_a) == 0:
        print(prob_a)
        print(person.currentFacility)
    prob_a = normalize(prob_a)
    prob_b = normalize(prob_b)
    prob_c = normalize(prob_c)
    prob_d = normalize(prob_d)

    length = len(sequence)
    final_prob = []
    for i in range(length):
        if prob_a[i] == 0 or prob_b[i] == 0 or prob_c[i] == 0 or prob_a[i] == 0 or i in person.facilityPassed:
            final_prob.append(0)
        else:
            final_prob.append(0.1*prob_a[i] + 0.7*prob_b[i] + 0.1*prob_c[i] + 0.1*prob_d[i])
    # if person.departureTime is not None:
    #     final_prob[10] = 0
    #     final_prob[11] = 0
    #     final_prob[12] = 0
    final_prob = normalize(final_prob)

    person.nextFacility = number_of_certain_probability(sequence, final_prob)
    person.facilityPassed.append(person.nextFacility)
    nextFacility = airportMap.facilityList[person.nextFacility]

    person.toBeAppend[0] = int(airportMap.getDistance(person.currentFacility, person.nextFacility) / 40)
    person.toBeAppend[1] = calTimeSpent(nextFacility.medium, nextFacility.variance)


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
                           personRadius)


def print_person_info(person):
    print('id = ', person.id)
    print('entered time = ', person.enteredTime)
    print('exit time = ', person.exitTime)
    print(person.movementTrack)
    print('length of movementTrack = ', len(person.movementTrack))
    print('current location = ', person.currentFacility)
    print('next facility = ', person.nextFacility)
    print('facilities passed = ', person.facilityPassed)
    print('\n')


def createPopulation():
    populationFront = []
    populationMain = []
    removedPopulation = []
    # arrival and connect
    for a in range(50):
        populationMain.append(person.Person(a, 1, currentFacility=0, arrivalTime=0, departureTime=150))
        populationMain[a].enteredTime = populationMain[a].arrivalTime + int(a / cg.num_people_off_plane)
    # arrival and exit
    for b in range(50, 150):
        populationMain.append(person.Person(b, 12, currentFacility=0, arrivalTime=0))
        populationMain[b].enteredTime = populationMain[b].arrivalTime + int(b / cg.num_people_off_plane)
    for c in range(150, 350):
        populationMain.append(person.Person(c, 12, currentFacility=1, arrivalTime=30))
        populationMain[c].enteredTime = populationMain[c].arrivalTime + int((c-150) / cg.num_people_off_plane)
    # departure
    for d in range(350, 550):
        temp = random.random() > (1 - cg.rate_self_checked)
        populationFront.append(person.Person(d, 1, checked=temp, departureTime=150))
        populationFront[d-350].enteredTime = random.randint(0, 50)

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

    # population = []
    # removedPopulation = []
    # num_exits = []
    # # TODO： replace with people creation function which can take in flight info
    # for j in range(100):
    #     population.append(person.Person(j, 0, 0, 1, 100))
    # for j in range(100, 200):
    #     population.append(person.Person(j, 30, 1, 12))
    # # num_people_off_plane = 15  # per min
    #
    # for person in population:
    #     person.enteredTime = person.arrivalTime + int((person.id % 100) / config.num_people_off_plane)

    populationFront, populationMain, removedPopulation = createPopulation()


    t = 0
    for t in range(200):
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

        for c in airportMap.counter:
            if not c.peopleInLine.empty():
                c.timeCounter += 1
                if c.timeCounter == cg.check_time:
                    person = c.peopleInLine.dequeue()
                    person.currentFacility = None
                    person.checked = True
                    c.timeCounter = 0
        for s in airportMap.security:
            if not s.peopleInLine.empty():
                s.timeCounter += 1
                if s.timeCounter == cg.security_time:
                    person = s.peopleInLine.dequeue()
                    #person.currentFacility = None
                    s.timeCounter = 0
                    populationMain.append(person)
                    populationFront.remove(person)

        for facility in airportMap.facilityList:
            airportMap.facilityList[facility].lastMinNumPeople = len(airportMap.facilityList[facility].people)
            airportMap.facilityList[facility].people = []
        # main
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
                    if person.currentFacility != 12 and person.currentFacility != person.destination and person.toBeAppend[1] == 0:
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
                    elif airportMap.facilityList[person.destination].type == 'Gate':
                        if t == person.departureTime:
                            person.exitTime = t
                            removedPopulation.append(person)
                        else:
                            person.toBeAppend[1] = person.departureTime - t




        # print('t = ', str(t), end=' ')
        # print(len(airportMap.facilityList[12].people))
        # num_exits.append(len(airportMap.facilityList[12].people))

        for person in removedPopulation:
            if person in populationMain:
                populationMain.remove(person)

    # plt.plot([sum(num_exits[:k]) for k in range(len(num_exits))])
    # plt.savefig('cumulative.jpg')
    # plt.close()
    # plt.plot(num_exits)
    # plt.savefig('perMin.jpg')

    # print('sum of people exiting', sum(num_exits))
    for person in removedPopulation:
        print_person_info(person)
    for person in populationMain:
        print_person_info(person)
    print('remainPopulation: ', len(populationMain))
    print('removedPopulation:', len(removedPopulation))


    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode((800, 600))  # Pygame窗口
    bg_color = (230, 230, 230)

    pygame.display.set_caption("Airport Map")  # 标题
    keep_going = True
    personRadius = 5
    myfont = pygame.font.Font(None, 25)
    t = 0

    # 游戏循环
    while keep_going:
        screen.fill(bg_color)
        plotFacilities()
        screen.blit(myfont.render('t = ', True, (0, 0, 0)), (10, 10))
        screen.blit(myfont.render(str(t), True, (0, 0, 0)), (36, 10))

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



# defined exit time
# defined hallway time and time spent in facility
# how to perfectly exit at that time


# 95% confidence interval
# time factor

# infectiouness in hallway

# input
# that will not crush the general system

import person as person
import facility as facility
import graph as g
import random
import numpy as np
import matplotlib.pyplot as plt
import pygame

def buildMap():
    # user input
    distanceMap = [[0 , 7 , 1 , 6 , 9 , 11, 13, 6 , 13, 12, 18, 19, 21],
                   [7 , 0 , 6 , 4 , 7 , 9 , 11, 1 , 12, 10, 16, 17, 19],
                   [1 , 6 , 0 , 5 , 8 , 10, 12, 4 , 10, 9 , 17, 18, 20],
                   [6 , 4 , 5 , 0 , 3 , 5 , 7 , 3 , 3 , 4 , 12, 13, 15],
                   [9 , 7 , 8 , 3 , 0 , 2 , 4 , 4 , 5 , 2 , 9 , 10, 12],
                   [11, 9 , 10, 5 , 2 , 0 , 2 , 7 , 6 , 1 , 7 , 8 , 10],
                   [13, 11, 12, 7 , 4 , 2 , 0 , 8 , 6 , 1 , 5 ,6 , 8 ],
                   [6 , 1 , 4 , 3 , 4 , 7 , 8 , 0 , 11, 13, 15, 16, 18],
                   [13, 12, 10, 3 , 5 , 6 , 6 , 11, 0 , 3 , 14, 15, 17],
                   [12, 10, 9 , 4 , 2 , 1 , 1 , 13, 3 , 0 , 8 , 9 , 11],
                   [18, 16, 17, 12, 9 , 7 , 5 , 15, 14, 8 , 0 , 1 , 2 ],
                   [19, 17, 18, 13, 10, 8 , 6 , 16, 15, 9 , 1 , 0 , 2 ],
                   [21, 19, 20, 15, 12, 10, 8 , 18, 17, 11, 2 , 2,  0 ]]

    airportMap = g.Graph(distanceMap)
    # user input
    facilityNames = ['gate1', 'gate2', 'restroom1', 'restaurant1', 'store1', 'restaurant2', 'restroom2', 'restroom3',
                     'store2', 'restaurant3', 'baggage claim1', 'baggage claim2', 'exit']
    idList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    typeList = ['Gate', 'Gate', 'Restroom', 'Food', 'Shopping', 'Food', 'Restroom', 'Restroom', 'Shopping', 'Drink', 'BC', 'BC', 'Exit']
    maxOccupancyList = [300, 300, 20, 50, 10, 20, 10, 15, 15, 10, 300, 300, 1000]
    mediumList = [0, 0, 3, 15, 3, 10, 2, 2, 5, 10, 20, 19, 0]
    varianceList = [0, 0, 1, 4, 1, 4, 1, 1, 1, 4, 4, 4, 0]
    for i in range(len(facilityNames)):
        airportMap.addFacility(idList[i], facilityNames[i], typeList[i], maxOccupancyList[i], mediumList[i], varianceList[i])
    airportMap.connectAllFacilities()
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

        # occupancy of current and next facility
        prob_d.append(abs(nextFacility.lastMinNumPeople - nextFacility.maxOccupancy) / nextFacility.maxOccupancy)

        # f. probability of staying (a function of ...)

        # e. override all other prob
        # 1- (exit time - current time) / (exit time - entered time), hop to next
        # set all previous facilities to zero, set the remaining to be prob * (1/distance)

        # how many people have left within how many time
        #
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
    final_prob = normalize(final_prob)

    person.nextFacility = number_of_certain_probability(sequence, final_prob)
    person.facilityPassed.append(person.nextFacility)
    nextFacility = airportMap.facilityList[person.nextFacility]

    person.toBeAppend[0] = airportMap.getDistance(person.currentFacility, person.nextFacility)
    person.toBeAppend[1] = calTimeSpent(nextFacility.medium, nextFacility.variance)





    # def compute_next_location(agent_object, graph):
    # a. 1/distance between current facility and the next one;
    # prob_a = [list of all locations](zero out current location) 1/distance c-n for the rest
    # normalize it

    # b. 1/distance between destination and the next facility;
    # prob_b = [list of all locations](zero out destination) 1/distance n-d for the rest
    # normalize it

    # c. non repeats facility type
    # 0.1 for current type, 1 for all the rest
    # normalize it

    # (d. everyone's needs)
    # food, restroom, shopping, drink, utilities


    # e. occupancy of I current and II next destination -> just pass
    # check occupancy
    # abs(occupancy of each facility - average occupancy) / max occupancy
    # average occupancy low for outside

    # f. probability of staying (a function of ...)
    # average time for every facility
    # iterate back from movementTrack until hit another facility
    # if smaller than average time, 0.9 on current facility and 0.1 on others
    # if greater, 0 on
    # distribution of staying time in advance

# def calculateNextFacility(person):
#     currentFacility = airportMap.facilityList[person.currentFacility]
#     sequence = []
#     prob = []
#     # calculate the probability going to every out neighbor
#     # ???
#     if currentFacility.id not in person.definedPath:
#         for id in currentFacility.outNeighbor:
#             sequence.append(id)
#             if id in person.facilityPassed or id == currentFacility.id or id not in person.definedPath:
#                 prob.append(0)
#             else:
#                 prob.append(1/currentFacility.getWeight(id) * airportMap.facilityList[id].prob)
#     else:
#         for id in currentFacility.outNeighbor:
#             sequence.append(id)
#             # cannot go to a facility twice
#             if id in person.facilityPassed or id == currentFacility.id:
#                 prob.append(0)
#             else:
#                 if id not in person.definedPath:
#                     prob.append(0.05 * 1/currentFacility.getWeight(id))
#                 elif person.definedPath.index(id) < person.definedPath.index(currentFacility.id):
#                     prob.append(0.05 * 1/currentFacility.getWeight(id))
#                 else:
#                     probability = 1
#                     for i in range(person.definedPath.index(currentFacility.id) + 1, person.definedPath.index(id)):
#                         probability *= (1 - airportMap.facilityList[definedPath[i]].prob)
#                     probability *= airportMap.facilityList[id].prob
#                     prob.append(probability)
#     sumofProb = sum(prob)
#     for i in range(len(prob)):
#         prob[i] = prob[i] / sumofProb
#
#     nextFacilityId = number_of_certain_probability(sequence, prob)
#     nextFacility = airportMap.facilityList[nextFacilityId]
#
#     person.movementTrack += currentFacility.getWeight(nextFacilityId) * [0]
#     if nextFacilityId != person.destination:
#         time_spent = calTimeSpent(nextFacility.medium, nextFacility.variance)
#         person.movementTrack += time_spent * [nextFacilityId]
#
#     person.facilityPassed.add(currentFacility.id)
#     person.lastFacility = currentFacility.id
#     person.currentFacility = nextFacilityId
def plotFacilities():
    screen.blit(myfont.render("gate1", True, (255, 0, 0)), (10, 230))
    pygame.draw.rect(screen, [255, 0, 0], [10, 250, 50, 50], 2)  # 0
    screen.blit(myfont.render("restroom1", True, (255, 0, 0)), (80, 230))
    pygame.draw.rect(screen, [255, 0, 0], [80, 250, 50, 50], 2)  # 2
    screen.blit(myfont.render("restaurant1", True, (255, 0, 0)), (230, 230))
    pygame.draw.rect(screen, [255, 0, 0], [230, 250, 50, 50], 2)  # 3
    screen.blit(myfont.render("store1", True, (255, 0, 0)), (340, 230))
    pygame.draw.rect(screen, [255, 0, 0], [340, 250, 50, 50], 2)  # 4
    screen.blit(myfont.render("restaurant2", True, (255, 0, 0)), (430, 320))
    pygame.draw.rect(screen, [255, 0, 0], [430, 250, 50, 50], 2)  # 5
    screen.blit(myfont.render("restroom2", True, (255, 0, 0)), (520, 230))
    pygame.draw.rect(screen, [255, 0, 0], [520, 250, 50, 50], 2)  # 6
    screen.blit(myfont.render("baggage claim1", True, (255, 0, 0)), (660, 170))
    pygame.draw.rect(screen, [255, 0, 0], [660, 190, 50, 50], 2)  # 10
    screen.blit(myfont.render("exit", True, (255, 0, 0)), (740, 230))
    pygame.draw.rect(screen, [255, 0, 0], [740, 250, 50, 50], 2)  # 12
    screen.blit(myfont.render("restroom3", True, (255, 0, 0)), (230, 350))
    pygame.draw.rect(screen, [255, 0, 0], [230, 370, 50, 50], 2)  # 7
    screen.blit(myfont.render("gate2", True, (255, 0, 0)), (230, 500))
    pygame.draw.rect(screen, [255, 0, 0], [230, 440, 50, 50], 2)  # 1
    screen.blit(myfont.render("store2", True, (255, 0, 0)), (340, 70))
    pygame.draw.rect(screen, [255, 0, 0], [340, 90, 50, 50], 2)  # 8
    screen.blit(myfont.render("restaurant3", True, (255, 0, 0)), (430, 170))
    pygame.draw.rect(screen, [255, 0, 0], [430, 190, 50, 50], 2)  # 9
    screen.blit(myfont.render("baggage claim2", True, (255, 0, 0)), (660, 320))
    pygame.draw.rect(screen, [255, 0, 0], [660, 340, 50, 50], 2)  # 11

def plotPersonPosition(currentPosition):
    if currentPosition == 0:
        pygame.draw.circle(screen, person.color, (35 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 1:
        pygame.draw.circle(screen, person.color, (255 + random.randint(-20, 20), 465 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 2:
        pygame.draw.circle(screen, person.color, (105 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 3:
        pygame.draw.circle(screen, person.color, (255 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 4:
        pygame.draw.circle(screen, person.color, (365 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 5:
        pygame.draw.circle(screen, person.color, (455 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 6:
        pygame.draw.circle(screen, person.color, (545 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 7:
        pygame.draw.circle(screen, person.color, (255 + random.randint(-20, 20), 395 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 8:
        pygame.draw.circle(screen, person.color, (365 + random.randint(-20, 20), 115 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 9:
        pygame.draw.circle(screen, person.color, (455 + random.randint(-20, 20), 215 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 10:
        pygame.draw.circle(screen, person.color, (685 + random.randint(-20, 20), 215 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 11:
        pygame.draw.circle(screen, person.color, (685 + random.randint(-20, 20), 365 + random.randint(-20, 20)),
                           personRadius)
    elif currentPosition == 12:
        pygame.draw.circle(screen, person.color, (765 + random.randint(-20, 20), 275 + random.randint(-20, 20)),
                           personRadius)
    else:
        pass


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


if __name__ == '__main__':
    airportMap = buildMap()
    population = []
    removedPopulation = []
    num_exits = []
    # TODO： replace with people creation function which can take in flight info
    for j in range(200):
        population.append(person.Person(j, 0, 0, 12))
    for j in range(200, 400):
        population.append(person.Person(j, 30, 1, 12))
    num_people_off_plane = 15  # per min
    for id in population:
        id.enteredTime = id.arrivalTime + int((id.id % 200) / num_people_off_plane)

    t = 0
    for t in range(100):
        for facility in airportMap.facilityList:
            airportMap.facilityList[facility].lastMinNumPeople = len(airportMap.facilityList[facility].people)
            airportMap.facilityList[facility].people = []

        for person in population:
            if t >= person.enteredTime:
                if person.toBeAppend[0] != 0:
                    person.currentFacility = -1
                    person.toBeAppend[0] -= 1
                else:
                    if person.toBeAppend[1] != 0:
                        if person.nextFacility is not None:
                            person.currentFacility = person.nextFacility
                            person.nextFacility = None
                        person.toBeAppend[1] -= 1
                    if person.currentFacility != 12 and person.toBeAppend[1] == 0:
                        compute_next_location(person, airportMap, t)
                person.movementTrack.append(person.currentFacility)

                if person.currentFacility != -1:
                    airportMap.facilityList[person.currentFacility].people.append(person.id)

                if person.currentFacility == person.destination:
                    person.exitTime = t
                    person.toBeAppend[0] = 0
                    person.toBeAppend[1] = 0
                    removedPopulation.append(person)

        # print('t = ', str(t), end=' ')
        # print(len(airportMap.facilityList[12].people))
        # num_exits.append(len(airportMap.facilityList[12].people))

        for person in removedPopulation:
            if person in population:
                population.remove(person)

    # plt.plot([sum(num_exits[:k]) for k in range(len(num_exits))])
    # plt.savefig('cumulative.jpg')
    # plt.close()
    # plt.plot(num_exits)
    # plt.savefig('perMin.jpg')

    # print('sum of people exiting', sum(num_exits))
    # for person in removedPopulation:
    #     print_person_info(person)
    print('remainPopulation: ', len(population))
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

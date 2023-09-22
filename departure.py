import departurePerson as person
import departureFacility as facility
import random
import numpy as np
import matplotlib.pyplot as plt
import config as config


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


def print_person_info(person):
    print('id = ', person.id)
    print('entered time = ', person.enteredTime)
    print(person.movementTrack)
    print('current location = ', person.currentFacility)
    print('\n')

if __name__ == '__main__':
    counter = []
    counter.append(facility.Facility(1, 'counter1', 'counter'))
    counter.append(facility.Facility(2, 'counter2', 'counter'))
    counter.append(facility.Facility(3, 'counter3', 'counter'))
    security = []
    security.append(facility.Facility(4, 'security1', 'security'))
    security.append(facility.Facility(5, 'security2', 'security'))
    security.append(facility.Facility(6, 'security3', 'security'))

    population = []
    for i in range(200):
        population.append(person.departurePerson(i))
    removedPopulation = []

    t = 0
    for t in range(300):
        for person in population:
            if t >= person.enteredTime:
                if person.currentFacility == None and not person.checked:
                    c = findLeastCounter(counter)
                    c.peopleInLine.enqueue(person)
                    person.currentFacility = c.id
                elif person.currentFacility == None and person.checked:
                    s = findLeastSecurity(security)
                    s.peopleInLine.enqueue(person)
                    person.currentFacility = s.id

                person.movementTrack.append(person.currentFacility)

        for c in counter:
            if not c.peopleInLine.empty():
                c.timeCounter += 1
                if c.timeCounter == config.check_time:
                    person = c.peopleInLine.dequeue()
                    person.currentFacility = None
                    person.checked = True
                    c.timeCounter = 0
        for s in security:
            if not s.peopleInLine.empty():
                s.timeCounter += 1
                if s.timeCounter == config.security_time:
                    person = s.peopleInLine.dequeue()
                    person.currentFacility = None
                    s.timeCounter = 0
                    removedPopulation.append(person)
                    population.remove(person)

        c = counter[0]
        print('t=', t)
        print('counter', c.id)
        for person in c.peopleInLine.items:
            print(person.id, end = ' ')
        print('\n')

    for person in removedPopulation:
        print_person_info(person)
    print(len(removedPopulation))
    print(len(population))


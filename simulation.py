"""
Program: Coronavirus Simulation
Author: Nathan Verghis
Date: March 18, 2020
I created this program in light of the coronavirus epidemic. I was inspired by
the vast confusion people had surrounding the need for isolation. I felt that by
creating this program, it could better teach people about why isolation is so
important in preventing the spread of a virus. Plans on expanding in the future
could involve creating a special member of the People class (compromised person)
to show the effectiveness of herd immunity on protecting a member of the
population who can't be relied on recovering from a disease on their own. I can
also expand the program to collect data from different iterations at different
values of infected and isolation to then graph in Matlab to better depict the
effect of isolation.
"""
import sys
import pygame
from pygame.locals import *
from random import randint
import time


# Game Settings
print("Please enter an isolation constant (0-100):")
isolation = float(input())

print("Please enter an starting infected population (0-100):")
infected = int(input())

mortality = 2
recovery = 15

pygame.init()
pygame.display.set_caption("Coronavirus Infection Simulation")
size = width, height = 1300, 650
speed = [25, 0]
black = 0, 0, 0
day_counter = 0
count = 0


# Creating People object
class Person:
    """A single person in the game. Has attributes of being sick, isolated, and
    alive. Meant to interact with another member of its population to create
    the simulation."""
    def __init__(self, isolated, sick):
        self.alive = True
        self.isolated = isolated
        self.sick = sick
        if self.isolated:
            self.speed = [0, 0]
        else:
            self.speed = [randint(-100, 100) * 0.25, randint(-100, 100) * 0.25]
        if sick:
            self.image = pygame.image.load("red box.jpg")
        else:
            self.image = pygame.image.load("white box.png")
        self.ps = self.image.get_rect()
        self.left = randint(1, 51)
        self.top = randint(1, 25)

    def new_day(self):
        """The change from day to day for a sick person.
        They can either recover or die
        If dead then they have no more impact on the population"""
        if self.sick:
            change = randint(1, 100)
            if change < mortality:
                self.isolated = True
                self.speed = [0, 0]
                self.alive = False
                self.sick = False
                self.image = pygame.image.load("green square.png")
            elif change < recovery:
                self.sick = False
                self.image = pygame.image.load("white box.png")

    def contact(self, other):
        """The event that two people come in contact with each other.
        Handles the case where the infection spreads
        Also handles the change in direction as they part ways
        Isolated people dont come into contact so people pass through them"""
        if self.ps.colliderect(other.ps) and not self.isolated \
                and not other.isolated:
            self.speed[0], self.speed[1] = \
                self.speed[0] * -1, self.speed[1] * -1
            other.speed[0], other.speed[1] = \
                other.speed[0] * -1, other.speed[1] * -1
            if self.sick and not other.sick:
                other.sick = True
                other.image = pygame.image.load("red box.jpg")
            elif not self.sick and other.sick:
                self.sick = True
                self.image = pygame.image.load("red box.jpg")


def sim_continue(pop):
    """Tells the simulation if there is any point in continuing.
    End of simulation defined as the event when the whole population is either
    dead or completely recovered."""
    all_dead = all(not people.alive for people in pop)
    all_healed = all(not people.sick for people in pop)
    return not(all_dead or all_healed)


def statistics(pop):
    """Informs the user of population statistics following the extermination of
    either the population or the virus"""
    alive = 0
    dead = 0
    for people in pop:
        if people.alive:
            alive += 1
        else:
            dead += 1
    return alive, dead


screen = pygame.display.set_mode(size)
population = []

# Creating the population
for i in range(100):
    is_isolated = False
    is_infected = False
    temp = randint(1, 100)
    if temp < isolation:
        is_isolated = True
    if temp < infected:
        is_infected = True
    new_person = Person(is_isolated, is_infected)
    new_person.ps = \
        new_person.ps.move(new_person.left * 25, new_person.top * 25)
    population.append(new_person)

# Creating the Simulation
while sim_continue(population):
    count += 1
    if count == 3:
        day_counter += 1
        count = 0
    time.sleep(0.09)
    # Exit Key (right arrow)
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RIGHT:
            sys.exit()

    screen.fill(black)
    for person in population:
        person.ps = person.ps.move(person.speed)
        if person.ps.left < 0 or person.ps.right > width:
            person.speed[0] = person.speed[0] * -1
        if person.ps.top < 0 or person.ps.bottom > height:
            person.speed[1] = person.speed[1] * -1
        for friend in population:
            if person is friend:
                pass
            else:
                person.contact(friend)
        if count == 0:
            person.new_day()
        screen.blit(person.image, person.ps)

    pygame.display.flip()

print("Days til completion: ", day_counter)

stats = statistics(population)
print("Alive: ", stats[0])
print("Dead: ", stats[1])

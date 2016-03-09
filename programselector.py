"""
Program selector module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

import random

from exception import NaughtyExpression

class ProgramSelector(object):

    __slots__ = []

    """An interface class for selecting a Program from the population"""

    def select(self, population):
        pass

class RandomProgramSelector(ProgramSelector):

    """A class which selects a program randomly from a population."""

    def select(self, population):
        return population.program(random.randint(0,len(population)-1))

class FitnessProportionateProgramSelector(ProgramSelector):

    """A class which selects a program randomly from the population, biased towards
    programs with higher fitnesses."""

    __slots__ = ['_fitnessdependence']

    def __init__(self, fitnessDependence):
        self._fitnessdependence = fitnessDependence

    def select(self,population):
        done = 0
        while(done==0):
            candidate = population[random.randint(0,len(population)-1)]
            r = random.randint(0,(int(population.getAverageAdjustedFitness()*100000000))) / 100000000.0
            try:
                normalizedFitness = candidate.adjustedFitness() / population.getAdjustedFitnessSum()
            except NaughtyExpression:
                normalizedFitness = 0

            if (r <= (normalizedFitness * (1.0 - self._fitnessdependence))):
                done = 1
        return candidate

class TournamentProgramSelector(ProgramSelector):

    """A class which holds a tournament between n randomly selected individuals and selects
    the fittest of the lot."""
    
    __slots__ = ['_tournamentsize']

    def __init__(self, tournamentSize):
        if tournamentSize == None:
            self._tournamentsize = 2
        else:
            self._tournamentsize = tournamentSize

    def select(self, population):
        tournament = []
        for i in range(self._tournamentsize):
            tournament.append(population.randomProgram())
        bestFitness = -1 ; best = None
        for p in tournament:
            #try:
            fitness = p.adjustedFitness()
            #except:
            #       fitness = -1 ; tournament.append(population.randomIndividual())
            if  fitness > bestFitness:
                best = p
                bestFitness = fitness
        return p
        
class RouletteWheelSelector(ProgramSelector):

    """A class which uses a roulette wheel method for selecting individuals from a
    population.
    
    (The programs will need to be sorted by fitness for this one.)
    """
    
    # IMPLEMENTME
    pass

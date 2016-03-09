"""
population module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.

"""

import random
import sys
import os
import string
from program import Program
from program import ConsoleProgram
from exception import NaughtyExpression
from exception import GeneticOperationException
from exception import IllegalStateException
from exception import UnimplementedVirtualMethod

class Population(list):

    """Represents a population of GPs

    
    """

    __slots__ = [
            '_environment','_interpreter','_generation',
            '_totaldepth','_deepestdepth','_adjustedfitnesssum',
            '_bestindividual','_worstindividual'
            ]
            #,'_programs'

    def __init__(self, env, interpreter):
        self._generation = 0
        self._environment = env
        self._interpreter = interpreter
        
    def __setitem__(self, index, item):
        list.__setitem__(self, index, item)
        self._resetStats()        
        
    def _resetStats(self):
        self._bestindividual = None
        self._worstindividual = None
        self._adjustedfitnesssum = None
        self._deepestdepth = 0
        self._totaldepth = 0

    def _updateStats(self):
        highest, lowest = 0, 1
        naughty = []
        self._deepestdepth, self._totaldepth = 0,0
        self._adjustedfitnesssum = 0
        for p in self:
            self._environment.fitnessevaluator.evaluate(p)
            self._totaldepth = self._interpreter.depth(p.lisp) + self._totaldepth
            if (self._interpreter.depth(p.lisp) > self._deepestdepth):
                self._deepestdepth = self._interpreter.depth(p.lisp)
            else:
                if (p.adjustedFitness() > highest):
                    self._bestindividual = p
                    highest = p.adjustedFitness()
                if (p.adjustedFitness() < lowest):
                    self._worstindividual = p
                    lowest = p.adjustedFitness()
                self._adjustedfitnesssum = self._adjustedfitnesssum + p.adjustedFitness()
            self._statsUpdateOccured()
        self._statsUpdated()

    def _makeProgram(self, lisp):
        """Factory method for instantiating Programs

        Override this in subclasses to instantiate Program subclasses.
        """
        return Program(self._environment, self._interpreter, lisp)

    def _populateOccured(self):
        """Called when an individual program is populated
        
        This can be extended in subclasses to provide feedback.
        """
        pass
    
    def _statsUpdateOccured(self):
        """Called when statistics are calculated for an individual program
        
        Extended to provide console-base feedback
        """
        pass

    def _contextSensitiveCrossoverOccured(self):
        """Called when a context sensitive crossover operation has occured

        This can be extended in subclasses to provide feedback.
        """
        pass

    def _crossoverOccured(self):
        """Called when a standard crossover operation has occured

        This can be extended in subclasses to provide feedback.
        """
        pass

    def _mutateOccured(self):
        """Called when a mutate operation has occured

        This can be extended in subclasses to provide feedback.
        """
        pass

    def _replicateOccured(self):
        """Called when a replicate operation has occured

        This can be extended in subclasses to provide feedback.
        """
        pass

    def _forceBestOccured(self):
        """Called when a force best operation has occured

        This can be extended in subclasses to provide feedback.
        """
        pass

    def _statsUpdated(self):
        """Called when the statitistics have been updated

        This can be extended in subclasses to provide feedback."""
        pass
        
    def _solutionFound(self):
        """Called when the solution has been discovered
        
        This can be extended in subclasses to provide feedback.
        """
        filename = "output/" + self._environment.name + "-sol.lsp"
        file = open(filename, 'w')
        file.write(self._bestindividual.lisp + "\n")
        file.close()

    def show(self):
        """Abstract method for showing the Population
        
        Implement this in subclasses to provide custom display formats.
        """
        raise UnimplementedVirtualMethod
                
    def populate(self):
        """Populate the population"""
        depth = self._environment.initialprogramdepth
        #self._programs = []
        self.reset()
        if not self._environment.populationsize:
            raise IllegalStateException
        n = self._environment.populationsize
        for i in range(n):
            p = self._makeProgram("()")
            p.randomize(depth)
            #self._programs.append(p)
            self.append(p)
            self._populateOccured()
        self._resetStats()
        self._updateStats()
        
    #def add(self, p):
    #    """Add a program to the Population"""
    #    self._programs.append(p)
    #self._resetStats()

    def reset(self):
        """Reset the Population to its initial (empty) state"""
        #self._programs = []
        while len(self) > 0:
            self.remove(self[0])
        self._resetStats()

    def next(self):
        """Breed the programs to create the next generation"""
        def crossover_(newpop):
            parent1 = self._environment.programselector.select(self)
            parent2 = self._environment.programselector.select(self)
            try:
                children = parent1.crossover(parent2)
                if len(newpop) < self._environment.getPopulationSize():
                    newpop.append(children[0])
                    self._crossoverOccured()
                if len(newpop) < self._environment.getPopulationSize():
                    newpop.append(children[1])
                    self._crossoverOccured()
            except NaughtyExpression:
                pass
            return newpop
        def csCrossover_(newpop):
            parent1 = self._environment.programselector.select(self)
            parent2 = self._environment.programselector.select(self)
            try:
                children = parent1.contextSensitiveCrossover(parent2)
                if len(newpop) < self._environment.getPopulationSize():
                    newpop.append(children[0])
                    self._contextSensitiveCrossoverOccured()
                if len(newpop) < self._environment.getPopulationSize():
                    newpop.append(children[1])
                    self._contextSensitiveCrossoverOccured()
            except NaughtyExpression:
                pass
            return newpop
        def mutate_(newpop):
            if len(newpop) < self._environment.getPopulationSize():
                try:
                    newpop.append(self._environment.programselector.select(self).mutant())
                    self._mutateOccured()
                except NaughtyExpression:
                    pass
            return newpop
        def replicate_(newpop):
            if len(newpop) < self._environment.getPopulationSize():
                try:
                    newpop.append(self._environment.programselector.select(self).replica())
                    self._replicateOccured()
                except NaughtyExpression:
                    pass
            return newpop
    
        newpop = []
        for i in range(self._environment.getForceBest()):
            newpop.append(self._bestindividual)
            self._forceBestOccured()

        size = self._environment.getPopulationSize()
        while (len(newpop) < size):
            stdCrossover = self._environment.getCrossoverP()
            csCrossover  = self._environment.getCSCrossoverP() + stdCrossover
            mutate       = self._environment.getMutateP()      + csCrossover
            replica      = self._environment.getReplicateP()   + mutate
            rnd = random.random()
            if (rnd <= stdCrossover):
                newpop = crossover_(newpop)
            elif (rnd <= csCrossover):
                newpop = csCrossover_(newpop)
            elif (rnd <= mutate):
                newpop = mutate_(newpop)
            elif (rnd <= replica):
                newpop = replicate_(newpop)
            else:
                raise GeneticOperationException

        #self._programs = newpop
        self.reset()
        self += newpop
        self._resetStats()
        #self.save()
        self._generation += 1
        self._updateStats()
        
    def breed(self):
        """Breed the programs until a solution is found"""
        done = 0
        #while (not self.isSuccessful()) and (not self._generation == self.__stopat__):
        if not os.path.exists("output"):
            os.mkdir("output")
        while (not done):
            done = (self._bestindividual.getHits() == self._environment.inputCount())
            if not done:
                self.next()
        self._solutionFound()

    def save(self):
        """Save the current population to the file provided"""
        name = self._environment.getRunName()
        genfile = open("output/" + name + "-gen.lsp",'w')
        statsfile = open("output/" + name + "-stats.csv", 'w')
        #for p in self._programs:
        for p in self:
            p.save(genfile)
            p.saveStats(statsfile)

    def load(self, path):
        """Load a population from a file"""
        file = open(path + "-gen.lsp", 'r')
        lisp = file.readline()[:-1]
        ct = 0
        while (lisp):
            ct = ct + 1
            p = self._makeProgram(lisp)
            #self._programs.append(p)
            self.append(p)
            lisp = file.readline()[:-1]

    #def randomProgram(self):
    #    """Return a random individual from the program list"""
    #    return self._programs[random.randint(0, len(self._programs) - 1)]
    
    #def getProgram(self, i):
    #    """Get a program with a specified index in the Population"""
    #    return self._programs[i-1]

    def getEnvironment(self):
        """Returns the current Environment"""
        return self._environment
        
    def getBestProgram(self):
        """The best Program in the list"""
        return self._bestindividual

    def getWorstProgram(self):
        """The worst Program in the list"""
        return self._worstindividual

    def getAdjustedFitnessSum(self):
        """The sum of the adjusted fitnesses of all Programs in list"""
        return self._adjustedfitnesssum

    def getAverageDepth(self):
        """Reports the average depth of the population"""
        return float(self._totaldepth) / float(len(self))

    def getDeepestDepth(self):
        """Reports the deepest depth in the population"""
        return self._deepestdepth

    def getAverageAdjustedFitness(self):
        """Returns the average adjusted fitness of the population"""
        return (self._adjustedfitnesssum / len(self))

    def getGeneration(self):
        """Returns the generation number of the population"""
        return self._generation
    
    #def getSize(self):
    #    """Return the current size of the population"""
    #    return len(self._programs)
        
    def help(self):
        help(type(self))

class ConsolePopulation(Population):
    """Represents a population of GPs, while providing a simple console
    based UI for interacting with a population
    
    Provides on-demand console output of population statistics.
    Provides visual progress indicators for genetic operations in
    real time.
    """
    __slots__ = ['_populated',
                 '_statscalculated',
                 '_crossovers', '_cscrossovers', '_replications', '_mutations'
                ]
                 
    def stats(self):
        """Print the stats of the current generation
        
        """
        best = self._bestindividual
        worst = self._worstindividual
        aaf = self._adjustedfitnesssum/len(self)
        sys.stdout.write("\n")
        sys.stdout.write("Generation " +\
                         string.zfill(self._generation, 5) + "\n")
        sys.stdout.write("================\n")
        sys.stdout.write(":Average Adjusted Fitness: " +\
                         str(aaf) + "\n")
        sys.stdout.write(":Deepest: " + str(self._deepestdepth) + "\n")
        sys.stdout.write("\nBest\n")
        sys.stdout.write("----\n")
        sys.stdout.write(":Lisp: " + best.lisp + "\n")
        sys.stdout.write(":Adjusted Fitness: " +\
                         str(best.adjustedFitness()) + "\n")
        sys.stdout.write(":Hits: " + str(best.getHits()) + "\n")
        sys.stdout.write("\nWorst\n")
        sys.stdout.write("-----\n")
        sys.stdout.write(":Lisp: " + worst.lisp + "\n")
        sys.stdout.write(":Adjusted Fitness: " +\
                         str(worst.adjustedFitness()) + "\n")
        sys.stdout.flush()
        
    def show(self):
        """Print the contents of the current population
        
        """
        for p in self:
            p.show()

    def _updateStats(self):
        # put this into a statsUpdateStarted event method
        self._statscalculated = 0
        sys.stdout.write("\n")
        Population._updateStats(self)
            
    def populate(self):
        # put this into a _populateStarted event method
        self._populated = 0
        sys.stdout.write("\n")
        Population.populate(self)
                
    def next(self):
        # put this into a _nextStarted event method
        self._crossovers = 0
        self._cscrossovers = 0
        self._replications = 0
        self._mutations = 0
        sys.stdout.write("\n")
        Population.next(self)

    def _populateProgress(self):
        percent = int((self._populated * 1.0 /
                       self._environment.populationsize) * 100)
        sys.stdout.write("\r(populating) " + string.zfill(percent,3) +"%")
        sys.stdout.flush()
        
    def _statsProgress(self):
        percent = int((self._statscalculated*1.0 / len(self)) * 100)
        sys.stdout.write("\r(updating stats) " + string.zfill(percent, 3) +"%")
        sys.stdout.flush()
                            
    def _nextProgress(self):
        ct = self._crossovers + self._cscrossovers +\
             self._replications + self._mutations
        percent = int((ct*1.0 / len(self)) * 100)
        sys.stdout.write("\r(breeding) " + string.zfill(percent, 3) + "% " +\
                         "c:" + string.zfill(self._crossovers, 4) + " " +\
                         "cs:" + string.zfill(self._cscrossovers, 4) + " " +\
                         "r:" + string.zfill(self._replications, 4) + " " +\
                         "m:" + string.zfill(self._mutations,4)
                        )
        sys.stdout.flush()

    def _makeProgram(self, lisp):
        """Factory method for instantiating Programs

        Overridden to create ConsolePrograms
        """
        return ConsoleProgram(self._environment, self._interpreter, lisp)

    def _populateOccured(self):
        """Called when an individual program is populated
        
        Extended to provide console-based feedback
        """
        self._populated += 1
        self._populateProgress()
        
    def _statsUpdateOccured(self):
        """Called when statistics are calculated for an individual program
        
        Extended to provide console-base feedback
        """
        self._statscalculated += 1
        self._statsProgress()
        
    def _contextSensitiveCrossoverOccured(self):
        """Called when a context sensitive crossover operation has occured

        Extended to provide console-based feedback.
        """
        #sys.stdout.write("%") ; sys.stdout.flush()
        self._cscrossovers += 1
        self._nextProgress()

    def _crossoverOccured(self):
        """Called when a standard crossover operation has occured

        Extended to provide console-based feedback.
        """
        #sys.stdout.write("x") ; sys.stdout.flush()
        self._crossovers += 1
        self._nextProgress()
        
    def _mutateOccured(self):
        """Called when a mutate operation has occured

        Extended to provide console-based feedback.
        """
        #sys.stdout.write("*") ; sys.stdout.flush()
        self._mutations += 1
        self._nextProgress()

    def _replicateOccured(self):
        """Called when a replicate operation has occured

        Extended to provide console-based feedback.
        """
        #sys.stdout.write("o") ; sys.stdout.flush()
        self._replications += 1
        self._nextProgress()

    def _forceBestOccured(self):
        """Called when a force best operation has occured

        This can be extended in subclasses to provide feedback.
        """
        #sys.stdout.write("b") ; sys.stdout.flush()
        pass

    def _statsUpdated(self):
        """Called when the statistics have been updated

        Extended to provide console-based feedback.
        """
        self.stats()

    def _solutionFound(self):
        """Called when the solution has been discovered
        
        Extended to provide console-based feedback.
        """
        Population._solutionFound(self)
        print "\nSolution found!"


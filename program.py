"""
Program module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

from pylisp import lisputil
import random
import random
import string
import math
import sys

from exception import NaughtyExpression
from exception import IllegalStateException
from exception import UnimplementedVirtualMethod

class Program(object):
    """A genetic program

    A Program has a lisp expression associated with it which dictates its
    behavior and therefore fitness.
    """

    __slots__ = [
            '_environment','_interpreter','_lisp',
            '_rawfitness','_depth','_hits'
            ]

    def __init__(self, env, interpreter, lisp="()"):
        """Create a Program

        You must provide a Charlemagne environment and optionally an initial
        lisp expression."""
        self._environment = env
        self._interpreter = interpreter
        self._lisp = lisp
        self._resetStats()

    def _resetStats(self):
        self._rawfitness = None
        self._depth = None
        self._hits = None

    def _makeProgram(self, lisp):
        """Factory method for instantiating programs

        This can be overridden in subclasses to create Program subclasses.
        """
        return Program(self._environment, self._interpreter, lisp)
        
    def show(self):
        """Abstract method for displaying the program
        
        Implement this in subclasses to provide custom display formats.
        """
        raise UnimplementedVirtualMethod

    def getLisp(self):
        """Retrieve the lisp source of the program"""
        return self._lisp

    def setLisp(self, lisp):
        """Set the lisp source of the program"""
        self._lisp = lisp
        self._resetStats()

    lisp = property(getLisp, setLisp, None, "the lisp expression")

    def getRawFitness(self):
        """Returns the raw fitness of the program

        Note the program needs to have been evaluated by a ProgramEvaluator
        for this to be set.  The Program does not evaluate its own fitness.
        """
        return self._rawfitness

    def setRawFitness(self, rawfitness):
        """Set the raw fitness of the program

        Normally a FitnessEvaluator should be doing this.
        """
        self._rawfitness = rawfitness

    rawfitness = property(getRawFitness, setRawFitness)

    def getDepth(self):
        """Returns the depth of the lisp expression

        Note the program needs to have been evaluated by a ProgramEvaluator
        for this to be set.  The Program does not evaluate its own depth.
        """
        return self._depth

    def setDepth(self, depth):
        """Set the depth of the program

        Note: this is setting the depth statistic for the program, not altering
        the lisp expression in any way.  Normally a FitnessEvaluator should be
        doing this.
        """
        self._depth = depth

    depth = property(getDepth, setDepth)

    def getHits(self):
        """Get the hits statistic

        Note the program needs to have been evaluated by a ProgramEvaluator
        for this to be set.  The Program does not evaluate its own hits.
        """
        return self._hits

    def setHits(self, hits):
        """Set the hits statistic

        Note: this is setting the hits statistic for the program, not altering
        the lisp expression in any way.  Normally a FitnessEvaluator should be 
        doing this.
        """
        self._hits = hits

    hits = property(getHits, setHits)

    def adjustedFitness(self):
        """Calculate the adjusted fitness
        
        Note the program needs to have been evaluated by a ProgramEvaluator for
        this to work.  The adjusted fitness is based on the rawfitness of the
        lisp expression.
        """
        try:
            a = (1.0 / (1.0 + abs(self._rawfitness)))
        except:
            print "IllegalStateException for " + self._lisp
            raise IllegalStateException
        return a

    def randomize(self, depth):
        """Randomize the Program's lisp expression"""
        terminals = "'" + lisputil.makeList(self._environment.vocabulary[0])
        onearg = "'" + lisputil.makeList(self._environment.vocabulary[1])
        twoarg = "'" + lisputil.makeList(self._environment.vocabulary[2])
        expr = lisputil.makeFunctionCall("random-program", [str(depth), terminals, onearg, twoarg])
        try:
            l = self._interpreter.querySolution(expr)
        except NaughtyExpression:
            # try again until it works
            self.randomize(depth)
        self.setLisp(l)
        self.replaceConstantSynthesisTokens()

    def replaceConstantSynthesisTokens(self):
        """Synthesize constants for all CONSTANT-SYNTHESIS token terminals
        
        The terminal CONSTANT-SYNTHESIS is a keyword which is replaced with a
        random constant."""
        #optimizations
        lstr = str ; randint = random.randint ; expovariate = random.expovariate ; replace = string.replace
        lisp = self._lisp ; find = string.find ; pow = math.pow
        while(find(lisp,"CONSTANT-SYNTHESIS") != -1):
            lisp = replace(lisp, "CONSTANT-SYNTHESIS", lstr(pow(-1, randint(1,2))*expovariate(1)), 1)
        self._lisp = lisp

    def save(self, file):
        """Save the program to file
        
        Saves the lisp expression as one line in the provided open file."""
        file.write(self._lisp + "\n")

    def saveStats(self, file):
        """Save the stats
         
         Saves the stats for this program to the provided open file."""
        #try:
        #       adjfitness = self.adjustedFitness(self._environment.inputSubsetSize())
        #       rawfitness = self.rawFitness(self._environment.inputSubsetSize())
        #except NaughtyExpression:
        #       sys.stdout.write("@")
        #       sys.stdout.flush()
        #       # JUST DONT WRITE THIS ONE FOR NOW
        #       #worst = self._environment.population().worstIndividual()
        #       #adjfitness = worst.adjustedFitness()
        #       #rawfitness = worst.rawFitness()
        #else:
        #       file.write(str(adjfitness) +","+ str(rawfitness) + "\n")
        file.write(str(self.adjustedFitness()) +","+ str(self._rawfitness) + "\n")

    def flatCount(self):
        """Return the number of possible program branches in the lisp expression"""
        expr = "(flat-count '%s)" % self._lisp
        flatCount = self._interpreter.querySolution(expr)
        return int(flatCount)

    def crossoverAt(self, mate, branch1, branch2):
        """Perform a crossover operation with another program at specified points on 
        the program trees
        """
        interpreter = self._interpreter
        expr = "(crossover-at '%s '%s %s %s)" % (self._lisp, mate.lisp, branch1, branch2)
        # note: this can raise NaughtyExpression, it should be dealt with in the caller
        children = interpreter.querySolution(expr)
        q1 = "(car '%s)" % (children)
        q2 = "(cadr '%s)" % (children)
        child1 = self._makeProgram(interpreter.querySolution(q1))
        child2 = self._makeProgram(interpreter.querySolution(q2))
        if self._interpreter.depth(child1.lisp) > self._environment.maxprogramdepth:
            child1 = self
        if self._interpreter.depth(child2.lisp) > self._environment.maxprogramdepth:
            child2 = mate
        return [child1] + [child2]

    def crossover(self, mate):
        """Perform a crossover operation with another program"""
        branch1 = random.randint(0, self.flatCount() - 1)
        branch2 = random.randint(0, mate.flatCount() - 1)
        c = self.crossoverAt(mate, branch1, branch2)
        return c

    def contextSensitiveCrossoverAt(self, mate, branch):
        """Perform a context sensitive crossover
        
        Perform a crossover operation with another program at specified points
        on the program trees."""
        interpreter = self._interpreter
        #print "Getting a tree path for " + str(self._lisp) +" "+ str(branch)
        expr = "(tree-path %s '%s)" % (branch,self._lisp)
        path = interpreter.querySolution(expr)
        if path=="NIL":
            path="()"
        #print "Does the path exist in the mate?" + str(mate.getLisp()) +" "+ path
        expr = "(path-exists '%s '%s)" % (mate.getLisp(), path)
        if interpreter.querySolution(expr)=='T':
            #print "Looks good.  Going ahead with the cscrossover.."
            expr = "(context-sensitive-crossover-at '%s '%s '%s)" % \
                            (self._lisp, mate.getLisp(), path)
            #print expr
            children = interpreter.querySolution(expr)
            ok = 1
            #print "OK: " + children
        else:
            #replicate for now
            #print "Mate is incompatible."
            return self.crossover(mate)
            #children = "(%s %s)" % (self._lisp, mate.getLisp())
            #print children
        if ok:
            q1 = "(car '%s)" % (children)
            q2 = "(cadr '%s)" % (children)
            child1 = self._makeProgram(interpreter.querySolution(q1))
            child2 = self._makeProgram(interpreter.querySolution(q2))
            if child1.getLisp()[-4:] == "NIL)":
                print self._lisp
                print mate.getLisp()
                print branch
                print child1.getLisp()
                print child2.getLisp()
                sys.exit()
            if self._interpreter.depth(child1.lisp) > self._environment.maxprogramdepth:
                child1 = self
            if self._interpreter.depth(child2.lisp) > self._environment.maxprogramdepth:
                child2 = mate
            return [child1] + [child2]
        else:
            return []

    def contextSensitiveCrossover(self, mate):
        """Perform a crossover operation with another program
        """
        branch = random.randint(0, self.flatCount() - 1)
        try:
            c = self.contextSensitiveCrossoverAt(mate, branch)
        except NaughtyExpression:
            # keep trying until we get a crossover that works.
            return self.crossover(mate)
        return c

    def mutant(self):
        """Perform a mutation on the program"""
        terminals = "'" + lisputil.makeList(self._environment.vocabulary[0])
        onearg = "'" + lisputil.makeList(self._environment.vocabulary[1])
        twoarg = "'" + lisputil.makeList(self._environment.vocabulary[2])
        mutant = self._makeProgram(self._interpreter.querySolution(lisputil.makeFunctionCall("mutate", ["'" + self._lisp] + [str(self._environment.maxprogramdepth), terminals, onearg, twoarg])))
        mutant.replaceConstantSynthesisTokens()
        return mutant

    def replica(self):
        """Replicate the program"""
        return self._makeProgram(self._lisp)

class ConsoleProgram(Program):
    """A genetic program - extended to provide console output

    A Program has a lisp expression associated with it which dictates its
    behavior and therefore fitness.
    """

    def _makeProgram(self, lisp):
        """Factory method for instantiating programs

        This can be overridden in subclasses to create Program subclasses.
        """
        return ConsoleProgram(self._environment, self._interpreter, lisp)
        
    def show(self):
        """Display the program in text format"""
        print self._lisp

    #def deviance(self, n):
    #       """The deviance of the output of p on input n from the output of fitnessExpression on input x"""
    #       return self._environment.deviancecalculator.calculate(this, n)
    #       #devianceExpression = self._environment.devianceExpression()
    #       #if devianceExpression==None:
    #       #       y = self.evaluate(self._environment.inputSubset(n))
    #       #       d = abs(self._environment.output(n) - float(y))
    #       #else:
    #       #       interpreter = self._environment.interpreter()
    #       #       setInputVector(interpreter, self._environment.inputSubset(n))
    #       #       # note, this can raise NaughtyExpression -- it should be dealt with in the caller
    #       #       q = "(%s %s)" % (devianceExpression, self.lisp())
    #       #       d = float(interpreter.querySolution(q))
    #       #return d

    #def hits(self):
    #       """The number of test cases the program got correct"""
    #       hits = 0
    #       precision = self._environment.precision.getValue()
    #       deviance = self.deviance
    #
    #       if self._environment.inputsubsetsize.isSet():
    #               n = self._environment.inputsubsetsize.getValue()
    #       else:
    #               n = len(self._environment.input)
    #
    #       for i in range(n):
    #               if (deviance(i) <= precision):
    #                       hits = hits + 1
    #       return hits

    #def rawFitness(self, inputSubsetSize):
    #       """The raw fitness of the Program over a set of test cases.
    #
    #       The raw fitness is the sum of the deviances of a test case set."""
    #
    #       if (self._rawfitness == None):
    #               rawfitness = 0.0
    #               deviance = self.deviance
    #               #inputSubsetSize = self._environment.inputSubsetSize()
    #               if self._environment.inputsubsetsize.isSet():
    #                       n = self._environment.inputsubsetsize.getValue()
    #               else:
    #                       n = len(self._environment.input)
    #
    #               for i in range(n):
    #                       d = deviance(i)
    #                       rawfitness = rawfitness + abs(d)
    #               self._rawfitness = rawfitness
    #       return self._rawfitness

    #def standardFitness(self):
    #       """Return the standard fitness - simply the raw fitness.
    #
    #       Why do we keep this?"""
    #       #print "standard fitness: " + str(self.rawFitness())
    #       return self.rawFitness()

    #def normalizedFitness(self, adjusted_fitness_sum, inputSubsetSize):
    #       """The normalized fitness of the Program"""
    #       return self.adjustedFitness(inputSubsetSize) / adjusted_fitness_sum

    #def best(self, p):
    #       """Compares this Program to another, returning the most fit"""
    #       if self.rawFitness(self._environment.inputSubsetSize()) <= p.rawFitness(self._environment.inputSubsetSize()):
    #               return self
    #       else:
    #               return p

    #def worst(self, p):
    #       """Compares this Program to another, return the least fit"""
    #       if self.rawFitness(self._environment.inputSubsetSize()) >= p.rawFitness(self._environment.inputSubsetSize()):
    #               return self
    #       else:
    #               return p

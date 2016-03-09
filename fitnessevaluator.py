"""
Fitness evaluator module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

from exception import NaughtyExpression

class FitnessEvaluator(object):
    """A class which calculates the fitness of a Program in a particular Environment.

    Use a FitnessEvalulator to set all fitness-related instance variables on a Program
    instance.
    """

    __slots__ = ['_interpreter', '_deviancecalculator', '_input', '_output']

    def __init__(self, input, output, interpreter, deviancecalculator):
        self._input = input
        self._output = output
        self._interpreter = interpreter
        self._deviancecalculator = deviancecalculator

    def setInput(self, input):
        self._input = input
        
    def setOutput(self, output):
        self._output = output

    def evaluate(self, p):
        """Evaluate and update specified program with its basic fitness information

        The deviance of the Program is calculated using the DevianceCalculator instance.
        The basic fitness properties of the Program are set (rawfitness and hits).
        """
        try:
            rawfitness = 0 ; hits = 0
            precision = 0.01
            inputct = len(self._input)
            for i in range(inputct):
                d = self._deviancecalculator.calculate(p, i)
                rawfitness = rawfitness + d
                hits = hits + (d <= precision)
            p.setRawFitness(rawfitness)
            p.setHits(hits)
        except NaughtyExpression:
            self.punish(p)

    def punish(self, p):
        """Severely punish this program

        Only use this when a program has been most inappropriate.
        This sets its fitness to be very bad.
        """
        # FIXME: this is arbitrary and therefore very bad
        # in some contexts, this rawfitness could be excellent!
        p.setRawFitness(999999)
        p.setHits(0)

    def best(self, p1, p2):
        """Compares one program to another, returning the most fit
        
        Programs are compared based on their rawfitness.
        """
        if p1.rawfitness <= p2.rawfitness:
            best = p1
        else:
            best = p2
        return best

    def worst(self, p1, p2):
        """Compares one program to another, returning the least fit
        
        Programs are compared based on their rawfitness.
        """
        if p1.rawfitness > p2.rawfitness:
            worst = p1
        else:
            worst = p2
        return worst


    #def hits(self, p):
    #       """The number of test cases the program got correct"""
    #       hits = 0
    #       #precision = self.__environment__.precision.getValue()
    #       precision = 0.01
    #       for i in range(len(self._input)):
    #               print " input:" + str(i)
    #               if (self._deviancecalculator.calculate(p, i) <= precision):
    #                       hits = hits + 1
    #       return hits

#class OutputListFitnessEvaluator(FitnessEvaluator):
#
#    """A FitnessCalculator which is a straight forward measurement of the
#    distance between the correct output and the actual output"""
#
#    def __calculateDeviance__(self, p, n):
#
#        """Calculate the deviance i.e. the distance between the actual output and the
#        correct output"""
#
#        y = self.__evaluate__(p, self.__env__.input[n])
#        return abs(self.__env__.output[n] - float(y))

#class DefaultFitnessEvaluator(OutputListFitnessEvaluator):
#    pass
#       def __init__(self):
#               pass

#       def evaluate(self, p):
#               p.setRawFitness(random.randint(0,99))

#class LispExpressionFitnessCalculator(FitnessCalculator):
#
#       """A FitnessCalculator that calculates deviance using a lisp expression"""
#
#       def __init__(self, env, interpreter, expr):
#               self.__env__ = env
#               self._interpreter = interpreter
#               self.__expr__ = expr
#
#       def __calculateDeviance__(self, p, n):
#
#               """Calculate the deviance based on the lisp expression"""
#
#               setInputVector(self._interpreter, self.__env__.input[n])
#               # note, this can raise NaughtyExpression -- it should be dealt with in the caller
#               q = "(%s %s)" % (self.__expr__, p.lisp)
#               d = float(self._interpreter.querySolution(q))

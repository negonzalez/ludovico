"""
Genetic programming environment module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

import string

from  deviancecalculator import  OutputDevianceCalculator
from  deviancecalculator import  LispFunctionDevianceCalculator
from  outputgenerator    import  LispExpressionOutputGenerator
from  fitnessevaluator   import  FitnessEvaluator
from  programselector    import  FitnessProportionateProgramSelector
from  programselector    import  TournamentProgramSelector

class Environment(object):
    """An environment in which genetic programming occurs

    This highly configurable class represents an environment in which
    the genetic programming takes place."""

    __slots__ = [
            '_name','_populationsize','_initialprogramdepth','_maxprogramdepth',
            '_crossoverp','_cscrossoverp','_replicatep','_mutatep',
            '_fitnessenvironment','_fitnessevaluator','_programselector',
            '_deviancecalculator','_outputgenerator',
            '_forcebest','_precision',
            '_input','_output',
            '_terminals','_oneargs','_twoargs',
            '_interpreter'
            ]

    def __init__(self):
        self._name                      = None
        self._populationsize            = None
        self._initialprogramdepth       = None
        self._maxprogramdepth           = None
        self._crossoverp                = 0
        self._cscrossoverp              = 0
        self._replicatep                = 0
        self._mutatep                   = 0
        self._programselector           = None
        self._fitnessenvironment        = None
        self._fitnessevaluator          = None
        self._deviancecalculator        = None
        self._outputgenerator           = None
        self._forcebest                 = None
        self._precision                 = None
        self._input                     = None
        self._output                    = None
        self._terminals                 = []
        self._oneargs                   = []
        self._twoargs                   = []
        self._interpreter               = None
        
    def initialize(self, interpreter):
        """Initialize any remaining properties.

        This should be called after command-line parameter application
        """
        self._interpreter = interpreter
        self._deviancecalculator.setInterpreter(interpreter)
        if self._outputgenerator <> None:
            if self._outputgenerator.__class__ == LispExpressionOutputGenerator:
                self._outputgenerator.setInterpreter(interpreter)
            self._output = self._outputgenerator.generate()
            self._deviancecalculator.setOutput(self._output)
        self._fitnessevaluator = FitnessEvaluator(self._input,
                                                  self._output,
                                                  self._interpreter,
                                                  self._deviancecalculator)

    def _readPutsFromFile(self, putsfile):
        put = []
        file = open(putsfile, 'r')
        for line in file.readlines():
            if len(line[:-1]) > 0:
                vector = string.split(line[:-1],',')
                for i in range(len(vector)):
                    vector[i] = float(vector[i])
                put.append(vector)
        return put

    #def _calculateOutputsFromExpression(self):
    #    interpreter = CLISPInterpreter(self._fitnessenvironment)
    #    output = []
    #    for i in self._input:
    #        output.append(
    #                float(interpreter.evaluate("(" + self._fitnessexpression + ")", i))
    #                )
    #    return output

    def getFitnessEvaluator(self):
        """Return the fitness evaluator

        This is an instance of FitnessEvaluator which is used to evaluate
        Program fitness.
        """
        return self._fitnessevaluator

    fitnessevaluator = property(getFitnessEvaluator)
    
    def getProgramSelector(self):
        """Return the program selector
        
        This is an instance of ProgramSelector which is used to select
        programs from the Population.
        """
        return self._programselector
        
    programselector = property(getProgramSelector)

    def getName(self):
        """Return the name of this run

        This can be used to log, save, load, and resume runs.
        """
        return self._name

    def setName(self, name):
        """Set the name of this run

        This can be used to log, save, load, and resume runs.
        """
        self._name = name

    name = property(getName, setName, None, 
                    "The name of this environment.  This can be used to " +\
                    "log, save, load, and resume runs.")

    def getPopulationSize(self):
        """Return the population size

        This is the size the population is initialize to and
        will remain throughout a run.
        """
        return self._populationsize

    def setPopulationSize(self, s):
        """Set the size of the population to use

        This is the size the population is initialize to and
        will remain throughout a run.
        """
        self._populationsize = s

    populationsize = property(getPopulationSize, setPopulationSize)

    def getInitialProgramDepth(self):
        """Return the initial program depth

        This is maximum initial program depth a Population will have.
        """
        return self._initialprogramdepth

    def setInitialProgramDepth(self, d):
        """Set the initial program depth

        This is maximum initial program depth a Population will have.
        """
        self._initialprogramdepth = d

    initialprogramdepth = property(getInitialProgramDepth, setInitialProgramDepth)

    def getMaxProgramDepth(self):
        """Return the maximum program depth allowed

        This is maximum program depth a Population can develop.
        """
        return self._maxprogramdepth

    def setMaxProgramDepth(self, d):
        """Set the maximum program depth to allow

        This is maximum program depth a Population can develop.
        """
        self._maxprogramdepth = d

    maxprogramdepth = property(getMaxProgramDepth,setMaxProgramDepth)

    def getCrossoverP(self):
        """Return the probability of a standard crossover operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        return self._crossoverp

    def setCrossoverP(self, P):
        """Set the probability of a standard crossover operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        self._crossoverp = P

    crossoverP = property(getCrossoverP, setCrossoverP)

    def getCSCrossoverP(self):
        """Return the probability of a context sensitive crossover operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        return self._cscrossoverp

    def setCSCrossoverP(self, P):
        """Set the probability of a context sensitive crossover operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        self._cscrossoverp = P

    def getReplicateP(self):
        """Return the probability of a replication operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        return self._replicatep

    def setReplicateP(self, P):
        """Set the probability of a replication operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        self._replicatep = P

    replicateP = property(getReplicateP, setReplicateP)

    def getMutateP(self):
        """Return the probability of a mutation operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        return self._mutatep

    def setMutateP(self, P):
        """Set the probability of a mutation operation occuring each turn during breeding

        This should be a number from 0 to 1.  The sum of all the genetic
        operation probability parameters must be exactly 1.
        """
        self._mutatep = P

    mutateP = property(getMutateP, setMutateP)

    def getInput(self):
        """Get the input list

        The input list is a list of vectors represented as lists.  There is no
        limit to the dimensionality of the vectors.
        """
        return self._input
        
    def setInput(self, input):
        """Set the input list
        
        The input list is a list of vectors represented as lists.  There is no
        limit to the dimensionality of the vectors.
        """
        self._input = input

    input = property(getInput, setInput)
        
    def getOutput(self):
        """Get the output list

        The output list is a list of single outputs.
        """
        return self._output

    def setOutput(self, output):
        """Set the output list

        The output list is a list of single outputs.
        """
        self._output = output

    output = property(getOutput, setOutput)

    def getVocabulary(self):
        """Returns the vocabulary

        The vocabulary is represented as a list containing three sublists in
        the following format:
        [ terminals-list, one-argument-function-list, two-argument-function-list ]
        """
        return [self._terminals, self._oneargs, self._twoargs]
        #return self._vocabulary

    def setVocabulary(self, vocabulary):
        """Set the vocabulary

        The vocabulary is represented as a list containing three sublists in
        the following format:
        [ terminals-list, one-argument-function-list, two-argument-function-list ]
        """
        self._terminals = vocabulary[0]
        self._oneargs = vocabulary[1]
        self._twoargs = vocabulary[2]
        #self._vocabulary = vocabulary

    vocabulary = property(getVocabulary, setVocabulary)

    def getTerminals(self):
        return self._terminals
        
    def setTerminals(self, terminals):
        self._terminals = terminals
        
    terminals = property(getTerminals, setTerminals)
        
    def getOneArgs(self):
        return self._oneargs
        
    def setOneArgs(self, oneargs):
        self._oneargs = oneargs
        
    oneargs = property(getOneArgs, setOneArgs)
        
    def getTwoArgs(self):
        return self._twoargs
        
    def setTwoArgs(self, twoargs):
        self._twoargs = twoargs
    
    twoargs = property(getTwoArgs, setTwoArgs)
    
    def useLispEnvironmentFile(self, filename):
        self._interpreter.evaluate('(load "' + filename + '")')
        
#     def getFitnessEnvironment(self):
#         """Return the fitness environment file filename
# 
#         ...
#         """
#         return self._fitnessenvironment
# 
#     def setFitnessEnvironment(self, fitnessenvironment):
#         """Set the fitness environment filename
# 
#         ...
#         """
#         self._fitnessenvironment = fitnessenvironment
# 
#     fitnessenvironment = property(getFitnessEnvironment, setFitnessEnvironment)

    # TODO fitness-dependence should be a value on --selection FITNESS-PROPORTIONATE
    #def getFitnessDependence(self):
    #    """Get the fitness dependence value
    #    """
    #    return self._fitnessdependence
    #
    #fitnessdependence = property(getFitnessDependence)

    def getForceBest(self):
        """Returns the number of instance of the best program per generation that will be forced to replicate

        If its zero, the feature is effectively disabled
        """
        return self._forcebest

    def setForceBest(self, forcebest):
        """Set the number of instance of the best program per generation that will be forced to replicate

        If its zero, the feature is effectively disabled
        """
        self._forcebest = forcebest

    forcebest = property(getForceBest)

    def getPrecision(self):
        """Returns the numeric value of how close a Program answer must be to be considered a hit
        """
        return self._precision

    def setPrecision(self, precision):
        """Sets the numeric value of how close a Program answer must be to be considered a hit
        """
        self._precision = precision

    precision = property(getPrecision, setPrecision)
    
    def useVocabularyFile(self, filename):
        """Set the vocabulary to the contents of the specified file

        The file must be an ASCII file with three lines.  The first line
        should be a comma seperated list of TERMINAL values.  The second
        line should be a comma seperated list of ONE-ARGUMENT lisp
        functions.  The third line should be a comma seperated list of
        TWO-ARGUMENT functions.
        """
        def readVocabularyFile(filename):
            file = open(filename, 'r')
            vocab = []
            vocab.append(string.split(file.readline()[:-1],','))
            vocab.append(string.split(file.readline()[:-1],','))
            vocab.append(string.split(file.readline()[:-1],','))
            return vocab
        
        self.vocabulary = readVocabularyFile(filename)

    def useInputsFromFile(self, inputsfile):
        """Use the input set contained in the specified file

        The file must be in ASCII comma delimited (CSV) format.  One input vector
        per line, with each dimension seperated by commas.
        """
        self._input = self._readPutsFromFile(inputsfile)

    def useOutputsFromFile(self, outputsfile):
        """Use the output set contained in the specified file

        The file must be an ASCII file with one line per output.  The can
        only be one output per line.
        """
        outputvectors = self._readPutsFromFile(outputsfile)
        self._output = []
        for vector in outputvectors:
            self._output.append(vector[0])

    def useFitnessProportionateSelection(self, fitnessDependence):
        """Use a fitness proportionate selection method

        Program selection for genetic operations will be biased
        towards more fit individuals.
        """
        self._programselector = FitnessProportionateProgramSelector(fitnessDependence)

    def useTournamentSelection(self, size):
        """Use a tourament selection method
        
        Program selection for genetic operations will be based on
        the winner of a tournament of the specified size.
        """
        self._programselector = TournamentProgramSelector(size)

    def useLispExpressionOutputGeneration(self, expr):
        """Use the specified lisp expression to generate outputs

        The specified expression should be a valid lisp expression
        accessible to the interpreter.  The expression must expect
        the input vector values as lisp variables in the form
        INPUT1,INPUT2,...INPUTn for an n dimensional input space.
        """
        self._outputgenerator = \
            LispExpressionOutputGenerator(expr, self._input, self._interpreter)

    def usePythonClassOutputGeneration(self, module, classname):
        """Use the specied OutputGenerator subclass to generate outputs

        The name of a OutputGenerator subclass must be specified along with the
        name of the module that contains it.  When activated, this class should
        generate the output list based on the values in the input list.
        """
        self._outputgenerator = getattr(__import__(module), classname)(self._input)

    def useOutputDevianceCalculation(self):
        """Use the output list for deviance calculation

        The output list is compared directly with the actual results of the Program
        being tested.
        """
        self._deviancecalculator = \
            OutputDevianceCalculator(self._input, self._output, self._interpreter)

    def useLispFunctionDevianceCalculation(self, name):
        """Use the specified lisp function for deviance calculation

        Sets the deviance calculation method to be based on a lisp function call
        with the specified name.
        """
        self._deviancecalculator = \
            LispFunctionDevianceCalculator(self._input, name, self._interpreter)

    def usePythonClassDevianceCalculation(self, module, classname):
        """Use the specified DevianceCalculator subclass for deviance calculation

        The name of a DevianceCalculator subclass must be specified along with the
        name of the module that contains it.
        """
        self._deviancecalculator = \
            getattr(__import__(module), classname)(self._input, self._interpreter)

    def inputCount(self):
        """Returns the number of inputs in the input list
        
        ...
        """
        return len(self._input)
        
    def help(self):
        help(type(self))



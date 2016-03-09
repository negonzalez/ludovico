# -*- coding: utf-8 -*-
"""
Charlemagne Application

Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.

"Just by chance you crossed a diamond with a pearl.
You turned it on the world.  That's when you turned
the world around.'"
                                      -- Steely Dan
"""
import sys
from environment     import Environment
from population      import Population
from population      import ConsolePopulation
from interpreter     import CLISPInterpreter
from configurator    import TextConfigurator
from parameter       import *
from exception       import UnimplementedVirtualMethod

#class Client(object)?????????
#class Session(object)????????
class Application(object):

    """The application class
    """

    __slots__ = [
        '_parameters','_execname',
        "_appname","_version","_date","_copyright","_url",
        '_environment','_configurator','_interpreter', '_population',
        ]

    def __init__(self, args):
        """Initialize the application with command-line style arguments"""

        self._appname   = "Charlemagne"
        self._execname  = "charlemagne"
        self._version   = "2.0.0"
        self._date      = "June 10, 2003"
        self._copyright = "Copyright © 2003 Robert Green.\nLicensed under "+\
                          "the GNU General Public License (GPL)."
        self._url       = "http://charlemagne.sourceforge.net"        
        self.printTag()
        self._parameters = self._makeParameters()    
        self._environment = Environment()
        self._interpreter = CLISPInterpreter()
        self._population = self._makePopulation()
        self._configurator = self._makeConfigurator()
        self._acceptArguments(args)
        #print "i should be initializing the interpreter with the fitness env"
        #self._interpreter.initialize(self._environment.getFitnessEnvironment()) 
           
    def _makeEnvironment(self):
           
        """Factory method for instantiating Environment
        
        ...
        """
        return Environment()
        
    def _makeInterpreter(self):
        """Factory method for instantiating interpreter
        
        Override this to instantiate different Interpreter subclasses.
        """
        return CLISPInterpreter()
        
    def _makeParameters(self):
        """Factory method for instantiating parameter list
        
        Extend this in subclasses to customize parameters
        """
        return [RunNameParameter(),
                InputParameter(),
                OutputParameter(),
                TerminalsParameter(),
                OneArgsParameter(),
                TwoArgsParameter(),
                InputsFileParameter(), 
                OutputsFileParameter(), 
                VocabularyFileParameter(), 
                PopulationSizeParameter(), 
                InitialDepthParameter(),
                MaxDepthParameter(),
                CrossoverProbabilityParameter(),
                CSCrossoverProbabilityParameter(),
                ReplicateProbabilityParameter(),
                MutateProbabilityParameter(),
                SelectionMethodParameter(),
                PrecisionParameter(),
                ForceBestParameter(),
                FitnessEnvironmentFileParameter(),
                GenerateOutputsParameter(),
                DevianceCalculationParameter()
               ]
        
    def _makePopulation(self):
        """Factory method for instantianting Populations

        Override this in subclasses to instantiate Population subclasses.
        """
        return Population(self._environment, self._interpreter)
        
    def _makeConfigurator(self):
        """Factory method for instantiating Configurator
        
        Override this in subclasses to instantiate Configurator subclasses.
        """
        return TextConfigurator(self._environment, self._parameters, self._interpreter)
        
    def _acceptArguments(self, args):
        for parameter in self._parameters:
            args = parameter.extractArg(args)
        if len(args) > 0:
            print "Unhandled command line input: " + str(args)
            print "Use -h or --help for usage information."
            sys.exit()
            
    def getParameters(self):
        return self._parameters
        
    parameters = property(getParameters)
    
    def printTag(self):
        """Output "tag" for application with name, version information, copyright, etc.
        
        ...
        """
        print self._appname + "-" + self._version + " (" + self._date + ")"
        print self._url
        print self._copyright

    def help(self, arg=None):
        if arg==None:
                self.printUsage()
        else:
                for param in self._parameters:
                        if param.getName()==arg:
                                print param.printUsage()

#     def config(self, args=[]):
#         for parameter in self._parameters:
#             args = parameter.extractArg(args)
#         if len(args) > 0:
#             print "Unhandled command line input: " + str(args)
#             print "Use -h or --help for usage information."
#             sys.exit()
#         for parameter in self._parameters:
#             if parameter.isSet():
#                 parameter.apply(self._environment)
#         for parameter in self._parameters:
#             parameter.cooperate(self._parameters)
#         for parameter in self._parameters:
#             if parameter.isSet():
#                 parameter.printValue()
#             else:
#                 if parameter.isMandatory():
#                     if parameter.extrapolateValue(self._environment):
#                         parameter.printValue()
#                     else:
#                         parameter.getInput()
#             if parameter.isSet():
#                 parameter.apply(self._environment)
#         #self._interpreter = CLISPInterpreter(self._environment.getFitnessEnvironment())
#         self._interpreter.initialize(self._environment.getFitnessEnvironment())
#         self._environment.initialize(self._interpreter)
#         print "Vocabulary: " + str(self._environment.getVocabulary())
#         print "Input: " + str(self._environment.getInput())
#         print "Output: " + str(self._environment.getOutput())
#         
#         self._population = self._makePopulation()
        
    def getPopulation(self):
        return self._population
    
    def getEnvironment(self):
        return self._environment
        
    def getInterpreter(self):
        return self._interpreter
        
    def getConfigurator(self):
        return self._configurator
        
    def help(self):
        help(type(self))

        
    #def run(self):
    #    """The main method of the application.
    #    
    #    Starts the Population breeding.
    #    """
    #    
    #    self._population.breed()
    
class ConsoleApplication(Application):

    """A Charlemagne application with console based feedback

    Subclasses Charlemagne to use console output based version of the
    core classes.
    """

    def _makePopulation(self):
        """Factory method for instantiating Populations

        Overridden to create ConsolePopulations.
        """
        return ConsolePopulation(self._environment, self._interpreter)

    
# 20021212 save this for generation logging inspiration

#       def _logGeneration(self):
#               generationFileName = self._runName +"-"+ str(self._generation)
#               self._population.save(generationFileName)
#               file = open(self._runName + ".gen", 'w')
#               file.write(str(self._generation))
#               file.close()
#               file = open(self._runName + "-best.lsp", 'w')
#               self._population.bestIndividual().save(file)
#               file.close()
#               self._avgFile.write(str(self._generation) +"," + str(self._population.avgAdjustedFitness()) +"\n")
#               self._avgFile.flush()
#               self._bestFile.write(str(self._generation) +","+ str(self._population.bestIndividual().adjustedFitness(self._environment.inputSubsetSize())) +"\n")
#               self._bestFile.flush()
#       def _initGeneration(self):
#               if self._continue:
#                       file = open(self._runName + ".gen",'r')
#                       self._generation = int(file.readline())
#                       self._populationFile = self._runName + "-" + str(self._generation)
#               else:
#                       self._generation = 0
#       def _go(self):
#               self._avgFile = open(self._runName + "-avg.csv", 'a')
#               self._bestFile = open(self._runName + "-best.csv", 'a')
#               while (not self._population.successful()) and (not self.generation() == self.stopAt()):
#                       self._environment.refreshInputSubset()
#                       self._logGeneration()
#                       self._population.breed()
#                       self._generation = self._generation + 1
#               self._logGeneration()
#               self._avgFile.close()
#               self._bestFile.close()


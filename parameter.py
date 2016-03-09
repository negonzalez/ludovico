"""
Parameter module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

import os
import sys
from exception import BadParameterException

class Command(object):
    
    __slots__ = ['_set', '_cmd', '_desc']
    
    def __init__(self, command, description):
        self._set = 0
        self._cmd = command
        self._desc = description
        
    def extract(self, args):
        if args[0] == self._cmd:
            self._set = 1
            args.remove(self._cmd)

    def set(self):
        self._set = 1
            
    def isSet(self):
        return self._set
        
    def printUsage(self):
        line = " " + self._cmd
        for i in range(22-(len(self._cmd))):
            line += " "
        line += self._desc
        print line

class Parameter(object):

    def __init__(self, name, description, mandatory, longswitch, 
                 shortswitch=None, value=None):
        self.__name__ = name
        self.__description__ = description
        self.__mandatory__ = mandatory
        self.__longswitch__ = longswitch
        self.__shortswitch__ = shortswitch
        self.__value__ = value

    def getName(self):
        return self.__name__

    def setName(self, name):
        self.__name__ = name

    name = property(getName, setName)

    def getDescription(self):
        return self.__description__

    def getValue(self):
        return self.__value__

    def setValue(self, value):
        self.__value__ = value

    value = property(getValue, setValue)

    def getLongSwitch(self):
        return self.__longswitch__
    
    def extrapolateValue(self, env):
        return 0

    def isSet(self):
        return (self.__value__ <> None)

    def setMandatory(self, mandatory):
        self.__mandatory__ = mandatory

    def isMandatory(self):
        return self.__mandatory__

    def show(self):
        print self.__name__ + ": " + str(self.__value__)

    def _prompt(self):
        return self.__name__ + " ["+ str(self.__value__) +"]: "
        
    def getInput(self):
        valid = 0
        while not valid:
            input = raw_input(self._prompt())
            if input=="":
                break
            else:
                valid = self.validate(input)
                if not valid:
                    print "[ invalid keyword ]"
        if valid:
            self.setValue(input)

    def apply(self, target):
        """Apply this parameter to the target object"""

    def cooperate(self, params):
        for param in params:
            self._cooperateWith(param)

    def _cooperateWith(self, param):
        pass
        
    def validate(self):
        pass

    def printUsage(self):
        line = " "
        if self.__shortswitch__ <> None:
            line += "-" + self.__shortswitch__ + ", "
            slen = len(self.__shortswitch__) + 3
        else:
            slen = 0
        line += "--" + self.__longswitch__
        if self.__longswitch__ <> None:
            llen = len(self.__longswitch__)
        else:
            llen = 0
        for i in range(22-(llen+slen)):
            line += " "
        line += self.__description__

        print line

class ValueParameter(Parameter):

    def extractArg(self, args):
        switch=None
        if ("--" + self.__longswitch__ in args):
            switch = "--" + self.__longswitch__
        else:
            if self.__shortswitch__:
                if ("-" + self.__shortswitch__ in args):
                    switch = "-" + self.__shortswitch__
        if switch:
            handled = []
            for i in range(len(args)):
                if args[i]==switch:
                    val = args[i+1]
                    if self.validate(val):
                        self.setValue(val)
                    else:
                        print "*** Ignoring invalid value: "+ val +" ***"
                    handled += args[i:i+2]
            for arg in handled:
                args.remove(arg)
        return args

class BooleanParameter(Parameter):

    def extractArg(self, args):
        switch=None
        if ("--" + self.__longswitch__ in args):
            switch = "--" + self.__longswitch__
        else:
            if self.__shortswitch__:
                if ("-" + self.__shortswitch__ in args):
                    switch = "-" + self.__shortswitch__
        if switch:
            self.__value__ = 1
            args.remove(switch)
        return args
        
    def validate(self, input):
        return input==0 or input==1

class IntParameter(ValueParameter):

    def setValue(self, value):
        self.__value__ = int(value)
        
    def validate(self, input):
        try:
            int(input)
            valid = 1
        except ValueError:
            valid = 0
        return valid

class FloatParameter(ValueParameter):

    def setValue(self, value):
        self.__value__ = float(value)

    def validate(self, input):
        try:
            float(input)
            valid = 1
        except ValueError:
            valid = 0
        return valid

class ListParameter(ValueParameter):

    def setValue(self, value):
        self.__value__ = value
        
    def validate(self, input):
        try:
            list(input)
            valid = 1
        except ValueError:
            valid = 0
        return valid

class StringParameter(ValueParameter):

    def setValue(self, value):
        self.__value__ = str(value)
    
    def validate(self, input):
        if input=="":
            valid = 0
        else:
            try:
                str(input)
                valid = 1
            except ValueError:
                valid = 0
        return valid

class Keyword(object):
    """Represents a keyword, possibly with an associated value"""
    
    __slots__ = ['_word', '_prop']
    
    def __init__(self, word, prop=None):
        self._word = word
        self._prop = prop
    
    def toString(self):
        s = self._word
        if self._prop:
            s += "=" + self._prop.__name__
        return s
                
    def match(self, input):
        match = 1
        if len(input) > 0:
            input = input.split('=')
            if len(input) > 1:
                if self._prop:
                    try:
                        self._prop(input[1])
                        match = 1
                    except ValueError:
                        match = 0
                else:
                    match = 0
            else:
                match = self._prop==None
            match = match and input[0]==self._word
        return match
        
class KeywordParameter(StringParameter):
    """A parameter with a finite list of valid string values"""
    
    __slots__ = ['_keywords']
    
    def __init__(self, name, description, mandatory, longswitch, 
                 shortswitch=None, value=None, keywords=None):
                 
        StringParameter.__init__(self, name, description, mandatory, longswitch,
                                 shortswitch, value)
        self._keywords = keywords
        
    def _prompt(self):
        options = ""
        for keyword in self._keywords:
            options += keyword._word + "=*, "
        options = "("+ options[:-2] +")"
        prompt = self.__name__ + " " + options + " ["+ str(self.__value__) +"]: "
        return prompt

    def validate(self, input):
        valid = 0
        for keyword in self._keywords:
            if keyword.match(input):
                valid = 1
                break
        return valid
        
    def printUsage(self):
        line = " "
        if self.__shortswitch__ <> None:
            line += "-" + self.__shortswitch__ + ", "
            slen = len(self.__shortswitch__) + 3
        else:
            slen = 0
        line += "--" + self.__longswitch__
        if self.__longswitch__ <> None:
            llen = len(self.__longswitch__)
        else:
            llen = 0
        for i in range(22-(llen+slen)):
            line += " "
        line += self.__description__

        line += " {"
        for keyword in self._keywords:
            line += keyword.toString() + ","
        line = line[:-1] + "}"
        print line

class FileParameter(StringParameter):
    """A StringParameter whose value must be the path (relative or absolute) to
    that of an existing file"""
    
    def validate(self, input):
        return os.path.exists(input)
                
class HelpParameter(BooleanParameter):
    def __init__(self):
        Parameter.__init__(self,
                           "Help",
                           "Display this help, then exit",
                           0, "help", "h")

class RunNameParameter(StringParameter):
    def __init__(self):
        Parameter.__init__(self, 
                          "Name", 
                          "Use the specified name for the session",
                          1, "name", "n")

    def apply(self, env):
        if self.__value__ <> None:
            env.name = self.__value__

class PopulationSizeParameter(IntParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Population Size", 
                           "Use the specified population size",
                           1, "population-size", "S", 500)

    def apply(self, env):
        if self.__value__ <> None:
            env.setPopulationSize(self.__value__)

class InitialDepthParameter(IntParameter):
    def __init__(self):
        Parameter.__init__(self,
                           "Maximum Initial Program Depth", 
                           "Restrain initial programs to the specified depth",
                           1, "initial-depth", "d", 10)

    def apply(self, env):
        if self.__value__ <> None:
            env.setInitialProgramDepth(self.__value__)

class MaxDepthParameter(IntParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Maximum Program Depth", 
                           "Restrain programs to the specified maximum depth",
                           1, "maximum-depth", "D", 100)

    def apply(self, env):
        if self.__value__ <> None:
            env.setMaxProgramDepth(self.__value__)

class CrossoverProbabilityParameter(FloatParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Traditional Crossover Probability", 
                           "Perform crossovers with the specified probability",
                           1, "crossover", "C", 0.85)

    def apply(self, env):
        if self.__value__ <> None:
            env.setCrossoverP(self.__value__)

    def extrapolateValue(self, env):
        extrapolated = 0
        csCrossoverP = env.getCSCrossoverP()
        replicateP = env.getReplicateP()
        mutateP = env.getMutateP()
        if (csCrossoverP <> None) and (replicateP <> None) and (mutateP <> None):
            self.__value__ = 1.0 - (csCrossoverP + replicateP + mutateP)
            extrapolated = 1
        return extrapolated

class CSCrossoverProbabilityParameter(FloatParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Context Sensitive Crossover Probability", 
                           "Perform context sensitive crossovers with the "
                           "specified probability",
                           1, "cs-crossover", "P", 0)

    def apply(self, env):
        if self.__value__ <> None:
            env.setCSCrossoverP(self.__value__)

    def extrapolateValue(self, env):
        extrapolated = 0
        crossoverP = env.getCrossoverP()
        replicateP = env.getReplicateP()
        mutateP = env.getMutateP()
        if (crossoverP <> None) and (replicateP <> None) and (mutateP <> None):
            self.__value__ = 1.0 - (crossoverP + replicateP + mutateP)
            extrapolated = 1
        return extrapolated

class ReplicateProbabilityParameter(FloatParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Replicate Probability", 
                           "Perform replications with specified probability",
                           1, "replicate", "R", 0.1)

    def apply(self, env):
        if self.__value__ <> None:
            env.setReplicateP(self.__value__)

    def extrapolateValue(self, env):
        extrapolated = 0
        crossoverP = env.getCrossoverP()
        csCrossoverP = env.getCSCrossoverP()
        mutateP = env.getMutateP()
        if (crossoverP <> None) and (csCrossoverP <> None) and (mutateP <> None):
            self.__value__ = 1.0 - (crossoverP + csCrossoverP + mutateP)
            extrapolated = 1
        return extrapolated

class MutateProbabilityParameter(FloatParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Mutate Probability", 
                           "Perform mutations with specified probability",
                            1, "mutate", "M", 0.05)

    def apply(self, env):
        if self.__value__ <> None:
            env.setMutateP(self.__value__)

    def extrapolateValue(self, env):
        extrapolated = 0
        crossoverP = env.getCrossoverP()
        csCrossoverP = env.getCSCrossoverP()
        replicateP = env.getReplicateP()
        if (replicateP <> None) and (crossoverP <> None) and (csCrossoverP <> None):
            self.__value__ = 1.0 - (replicateP + crossoverP + csCrossoverP)
            extrapolated = 1
        return extrapolated
        
class InputParameter(ListParameter):
    def __init__(self):
        ListParameter.__init__(self, "Input",
                               "Use specified input",
                               0, "input", None)

    def apply(self, env):
        if self.__value__ <> None:
            env.input = self.__value__

class OutputParameter(ListParameter):
    def __init__(self):
        ListParameter.__init__(self, "Output",
                               "Use specified output",
                               0, "output", None)

    def apply(self, env):
        if self.__value__ <> None:
            env.output = self.__value__
            
# class VocabularyParameter(ListParameter):
#     def __init__(self):
#         ListParameter.__init__(self, "Vocabulary",
#                                "Use specified vocabulary",
#                                0, "vocabulary", None)
# 
#     def apply(self, env):
#         if self.__value__ <> None:
#             env.vocabulary = self.__value__
            
class TerminalsParameter(ListParameter):
    def __init__(self):
        ListParameter.__init__(self, "Terminals",
                              "Use specified terminals in vocabulary",
                               0, "terminals", None)
                           
    def apply(self, env):
        if self.__value__ <> None:
            env.terminals = self.__value__.split(",")
            
class OneArgsParameter(ListParameter):
    def __init__(self):
        ListParameter.__init__(self, "One Argument Functions",
                              "Use specified one argument functions in vocabulary",
                               0, "one-args", None)
                           
    def apply(self, env):
        if self.__value__ <> None:
            env.oneargs = self.__value__.split(",")
            
class TwoArgsParameter(ListParameter):
    def __init__(self):
        ListParameter.__init__(self, "Two Argument Functions",
                              "Use specified two argument functions in vocabulary",
                               0, "two-args", None)
                           
    def apply(self, env):
        if self.__value__ <> None:
            env.twoargs = self.__value__.split(",")
            
class InputsFileParameter(FileParameter):
    def __init__(self):
        FileParameter.__init__(self, "Inputs File", 
                           "Use data from specified file as input data",
                           1, "inputs-file", "I")

    def apply(self, env):
        if self.__value__ <> None:
            env.useInputsFromFile(self.__value__)
            
class OutputsFileParameter(FileParameter):
    def __init__(self):
        FileParameter.__init__(self, "Outputs File", 
                           "Use data from specified file as output data",
                           1, "outputs-file", "O")

    def apply(self, env):
        if self.__value__ <> None:
            env.useOutputsFromFile(self.__value__)

class VocabularyFileParameter(FileParameter):
    def __init__(self):
        FileParameter.__init__(self, "Vocabulary File", 
                           "Use vocabulary defined in specified file",
                           1, "vocabulary-file", "V")

    def apply(self, env):
        env.useVocabularyFile(self.__value__)

class SelectionMethodParameter(KeywordParameter):
    def __init__(self):
        keywords = [ Keyword("FITNESS-PROPORTIONATE",float),
                     Keyword("TOURNAMENT",int) ]
        KeywordParameter.__init__(self, "Selection Method",
                                  "Use specified selection method",
                                  1, "selection", None, "FITNESS-PROPORTIONATE=0.9",
                                  keywords)

    def apply(self, env):
        tmp = self.__value__.split('=')
        if tmp[0] == "FITNESS-PROPORTIONATE":
            env.useFitnessProportionateSelection(float(tmp[1]))
        elif tmp[0] == "TOURNAMENT":
            env.useTournamentSelection(int(tmp[1]))
        else:
            raise BadParameterException

class InputSubsetSizeParameter(IntParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Input Subset", 
                           "Evaluate fitness based on a random subset of the inputs of the specified size",
                           0, "input-subset")

class FitnessEnvironmentFileParameter(FileParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Lisp Environment File", 
                           "Initialize lisp interpreter with specified file",
                           0, "lisp-environment-file")

    def apply(self, interpreter):
        interpreter.evaluate('(load "' + self.__value__  + '")')

#class FitnessExpressionParameter(StringParameter):
#    def __init__(self):
#        Parameter.__init__(self, "Fitness Expression", "Base fitness evaluation on the lisp expression <expr>",
#                                           0, "fitness-expression")
#
#    def _cooperateWith(self, param):
#        if self.__value__ <> None:
#            if param.getName() == "Outputs File":
#                param.setMandatory(0)
#
#    def apply(self, env):
#        env.setFitnessExpression(self.__value__)

class ForceBestParameter(IntParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Force Best", 
                           "Force the specified number of best program to carry over",
                           1, "force-best", None, 0)

    def apply(self, env):
        env.setForceBest(self.__value__)

class PrecisionParameter(FloatParameter):
    def __init__(self):
        Parameter.__init__(self, 
                           "Precision", 
                           "Use the specified precision in determining hits",
                           1, "precision", None, 0.0001)

    def apply(self, env):
        env.setPrecision(self.__value__)

class GenerateOutputsParameter(KeywordParameter):
    def __init__(self):
        keywords = [ Keyword("LISP-EXPRESSION", str),
                     Keyword("PYTHON-CLASS", str)
                   ]
        KeywordParameter.__init__(self, 
                                  "Generate Outputs",
                                  "Generate outputs using specified method",
                                  0, "generate-outputs", None, None,
                                  keywords)

    def _cooperateWith(self, param):
        if self.__value__ <> None:
            if param.getName() == "Outputs File":
                param.setMandatory(0)

    def apply(self, env):
        tmp = self.__value__.split('=')
        method = tmp[0] ; value = tmp[1]
        if method=="PYTHON-CLASS":
            tmp = value.split('.')
            module = tmp[0] ; classname = tmp[1]
            env.usePythonClassOutputGeneration(module, classname)
        elif method=="LISP-EXPRESSION":
            env.useLispExpressionOutputGeneration(value)
        else:
            raise BadParameterException

class DevianceCalculationParameter(KeywordParameter):
    def __init__(self):
    
        keywords = [ Keyword("OUTPUT"),
                     Keyword("LISP-FUNCTION", str),
                     Keyword("PYTHON-CLASS", str)
                   ]
        KeywordParameter.__init__(self, 
                           "Deviance Calculation",
                           "Calculate deviance using the specified method",
                           1, "deviance-calculation", None, "OUTPUT",
                           keywords)

    def _cooperateWith(self, param):
        if self.__value__ <> "OUTPUT":
            if param.getName() == "Outputs File":
                param.setMandatory(0)

    def apply(self, env):
        tmp = self.__value__.split('=')
        method = tmp[0]
        if method=="OUTPUT":
            env.useOutputDevianceCalculation()
        elif method=="LISP-FUNCTION":
            env.useLispFunctionDevianceCalculation(tmp[1])
        elif method=="PYTHON-CLASS":
            tmp = tmp[1].split('.')
            env.usePythonClassDevianceCalculation(tmp[0],tmp[1])
        else:
            raise BadParameterException

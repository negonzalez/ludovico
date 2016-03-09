"""
Deviance calculator module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

from exception import NaughtyExpression
from exception import UnimplementedVirtualMethod

class DevianceCalculator(object):
    """An abstract class which is responsible for calculating deviance

    The calculate method should be implemented in subclasses.
    """
    __slots__ = ['_interpreter']

    def setInterpreter(self, interpreter):
        """Set the lisp interpreter to use when calculating deviances
        
        ...
        """
        self._interpreter = interpreter

    def getInterpreter(self):
        """Return the interpreter used for calculating deviances
        
        ...
        """
        return self._interpreter

    def calculate(self, p):
        """Calculate the deviance of a program
        
        ...
        """
        raise UnimplementedVirtualMethod

class InputDevianceCalculator(DevianceCalculator):
    """An abstract class which is responsible for calculating deviance on an input set.

    The calculate method should be implemented in subclasses.
    """
    __slots__ = ['_input']

    def getInput(self):
        """Return the input set
        
        ...
        """
        return self._input

    def calculate(self, p, i):
        """Calculate the deviance of a program on a given input
        
        ...
        """
        raise UnimplementedVirtualMethod

class OutputDevianceCalculator(InputDevianceCalculator):
    """A DevianceCalculator which calculates deviance based on the input and output set.

    Deviance is calculated based on the difference between the
    expected output from an output list and the actual output.
    """
    __slots__ = ['_output']

    def __init__(self, input, output, interpreter=None):
        self._interpreter = interpreter
        self._input = input
        self._output = output

    def setOutput(self,output):
        """Set the output set

        ...
        """
        self._output = output

    def getOutput(self):
        """Return the output set
        
        ...
        """
        return self._output

    def calculate(self, p, i):
        """Calculate the deviance the specified program on the specified input/output index.

        WARNING: This can raise NaughtyException which should be
        dealt with in the caller.
        """
        y = self._interpreter.evaluate(p.lisp, self._input[i])
        return abs(self._output[i] - float(y))

class LispFunctionDevianceCalculator(InputDevianceCalculator):
    """A DevianceCalculator which calculates deviance by evaluating a lisp expression.

    Deviance is calculated by evaluating a specified expression on
    with the interpreter specified.
    """

    __slots__ = ['_expression']

    def __init__(self, input, expression, interpreter=None):
        self._interpreter = interpreter
        self._input = input
        self._expression = expression

    def calculate(self, p, i):
        """Calculate the deviance the specified program on the specified input index.

        WARNING: This can raise NaughtyException which should be
        dealt with in the caller.
        """
        expr = "(" + self._expression + " " + p.lisp + ")"
        deviance = abs(float(self._interpreter.evaluate(expr, self._input[i])))

        return deviance

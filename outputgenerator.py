"""
Output generator module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

from exception import UnimplementedVirtualMethod

class OutputGenerator(object):
    """An abstract class which is responsible for generating outputs.

    The generate method must be implemented in subclasses."""

    __slots__ = ['_input']

    def __init__(self, input):
        self._input = input

    def generate(self):
        """Generate outputs based on inputs
        
        ...
        """
        raise UnimplementedVirtualMethod

class LispExpressionOutputGenerator(OutputGenerator):
    """An OutputGenerator which uses a lisp expression to generate each output
    
    This class must be supplied with a working LispInterpreter instance.
    """
    __slots__ = ['_expression','_interpreter']

    def __init__(self, expression, input, interpreter=None):
        self._expression = expression
        self._input = input
        self._interpreter = interpreter

    def setInterpreter(self, interpreter):
        """Set the interpreter to use in output generation

        ...
        """
        self._interpreter = interpreter

    def generate(self):
        """Generate outputs based on inputs using lisp expression
        
        ...
        """
        output = []
        for i in self._input:
            output.append(float(self._interpreter.evaluate(self._expression, i)))
        return output

"""
Interpreter module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

import pylisp
import os
import sys
from exception import NaughtyExpression
from pylisp.client import PyLisp

class Interpreter(object):
    """An abstract class which represents an interpreter of some kind

    ...
    """
    
    def evaluate(self, expr):
        """Evaluate an expression
        
        ...
        """
        
    def getHelp(self):
        help(type(self))
        
    help = property(getHelp)

class LispInterpreter(Interpreter):
    """An abstract class which represents a lisp interpreter of some kind

    ...
    """

    def evaluate(self, expr):
        """Evaluate a lisp expression
        
        ...
        """


class CLISPInterpreter(PyLisp, LispInterpreter):
    """A LispInterpreter implementation specific to CLISP

    ...
    """
    
    def __init__(self):
        lisp_path = sys.prefix + "/share/charlemagne/lisp"
        PyLisp.__init__(self, 
                        "clisp", 
                        ("clisp", 
                        "-i",
                        lisp_path+"/charlemagne.lsp",
                        lisp_path+"/pylisp_server.lsp"
                        )
                       )
                                                      
    def eval(self, p):
        """Evaluate the lisp expression
        """
        self.query(p)
        return self.getSolution()

    def query(self,q):
        """Send a query to the interpreter

        ...
        """
        safeQuery = "(handler-case (without-floating-point-underflow "+ q +") ((or floating-point-overflow floating-point-underflow) () 'NAUGHTY))"
        PyLisp.query(self, safeQuery)

    def getSolution(self, timeout=None):
        """Get a solution from the interpreter

        ...
        """
        sol = PyLisp.getSolution(self, timeout)
        if (sol == "NAUGHTY"):
            raise NaughtyExpression
        return sol

    def setInputVector(self, vector):
        """Set the input vector to evaluate on
        
        ...
        """
        lstr = str
        for i in range(len(vector)):
            l = "(setq INPUT%s %s)" % (lstr(i+1), lstr(vector[i]))
            self.edibleQuery(l)

    def evaluate(self, expr, vector=None):
        """Evaluate a CLISP compatible expression

        ...
        """
        if vector <> None:
            self.setInputVector(vector)
        return self.querySolution(expr)

    def depth(self, expr):
        """Calculate the depth of a lisp expression

        ...
        """
        q = "(depth '%s)" % (expr)
        return int(self.querySolution(q))

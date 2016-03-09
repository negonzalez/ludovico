"""
Configurator module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

from exception import UnimplementedVirtualMethod

class Configurator(object):
    """Class for configuring parameters
    """
    __slots__ = ['_environment','_parameters','_interpreter']
    
    def __init__(self, env, params, interpreter):
        self._environment = env
        self._parameters = params
        self._interpreter = interpreter
        
    def help(self):
        help(type(self))

    def configure(self):
        """Abstract method to configure the environment parameters
        
        Override this in subclasses
        """
        raise UnimplementedVirtualMethod
        
    def apply(self):
        """Abstract method to configure the environment parameters
        
        Override this in subclasses
        """
        raise UnimplementedVirtualMethod
        
    def show(self):
        """Abstract method for showing the contents of the configurator
        
        Override this in subclasses
        """
        raise UnimplementedVirtualMethod
        
class TextConfigurator(Configurator):
    """A Configurator that provide a text UI"""
    
    def configure(self, name=None, value=None):
            for param in self._parameters:
                if name==None:
                    param.getInput()
                else:
                    if param.getName()==name or param.getLongSwitch()==name:
                        if value==None:
                            param.getInput()
                        else:
                            if param.validate(value):
                                param.setValue(value)
                        break

    def apply(self):
        for param in self._parameters:
            #kludge: we need to distinguish between environment params and
            #        interpreter params
            if param.getName() == "Lisp Environment File":
                if param.isSet():
                    param.apply(self._interpreter)
            else:
                if param.isSet():
                    param.apply(self._environment)
        for param in self._parameters:
            param.cooperate(self._parameters)
#         for param in self._parameters:
#             if param.isSet():
#                 param.show()
#             else:
#                 if param.isMandatory():
#                     if param.extrapolateValue(self._environment):
#                         param.show()
#                     else:
#                         param.getInput()
#             if param.isSet():
#                 param.apply(self._environment)

        self._environment.initialize(self._interpreter)

    def show(self, name=None):
        for param in self._parameters:
            if name==None:
                param.show()
            else:
                if param.getName()==name or param.getLongSwitch()==name:
                    param.show()
                    break
            

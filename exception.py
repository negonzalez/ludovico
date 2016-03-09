"""
Exception module

This module is part of Charlemagne
Copyright (c) Robert Green 2002, 2003

Charlemagne is distributed under the GNU General Public License.  See
the file LICENSE.txt in the distribution for details.
"""

class NaughtyExpression(Exception):
    pass

class GeneticOperationException(Exception):
    pass

class IllegalStateException(Exception):
    pass

class UnimplementedVirtualMethod(Exception):
    pass
    
class BadParameterException(Exception):
    pass

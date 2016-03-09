from wxPython.wx import *
from population import Population

class PopulationMonitor(object):

        __slots__ = ['_population', '_frame']

        def __init__(self, population):
                self._population = population
                self._frame = wxFrame(NULL, -1, "Population Monitor")

        def show(self):
                print "showing frame"
                self._frame.Show()
        
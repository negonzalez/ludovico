"""

===============================
Charlemagne Development Roadmap
===============================

:Web site: http://charlemagne.sourceforge.net/
:Project page: http://sourceforge.net/projects/charlemagne/
:Author: Bob Green
:Email: bob underscore green at speakeasy dot net


This is the tentative schedule for major functionality that will be added 
to major releases categorized by release number.  The miscellaneous 
category contains items for which it has not been decided when or if 
they will be implemented.  This schedule is loose, so if anyone wants to 
contribute, feel free to work on these out of order.


---
1.x
---

* Initial release

---
2.x
---

* Distutils distribution, install
* Interactive session support
* Interactive help system integrated with docstrings in code.
* Much improved documentation

---
3.x
---

* Cross-platform support (Windows, OS X, etc.)
* wxPython interface.
* Threaded processes.

---
4.x
---

* Migration/Immegration - Migration will pave the way for parallel 
  processing.  Libevocosm has a nice API for this that I would like to 
  emulate.  It consists of an abstract Migrator class and an abstract 
  Immegrator class.  Implematations of these could use different methods of 
  achieving this, but presumably concrete Migrators and Immegrators would 
  operate in functional pairs.

* Parallel processing support (directory-based?, xml-rpc based?)

-------------
Miscellaneous
-------------

* Inline C++ w/ weave or similar for massive performance gains.

* Scipy support/integration/dependance?

* Roulette wheel selection -I've never felt totally comfortable with my 
  selection method.  Libevocosm implements a RouletteWheel for selection.  
  This probably dictates that the programs must be sorted which is 
  something that so far I've managed to not do, but this method would   
  certainly instill some more confidence in me that the selection process   
  wasn't fatally flawed.
  
* Genetic operators for terminals - Libevocosm uses a real number 
  evolver which allows crossover and mutation on real number terminals.  
  Currently in charlemagne there is only spontaneous creation of real 
  numbers through general mutation through the special terminal 
  CONSTANT-SYNTHESIS.

* Interactive help mode

* Interactive lisp mode

* Clean error checking, Ctrl-C stopping

"""

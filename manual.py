# -*- coding: utf-8 -*-
"""

=======================
Charlemagne User Manual
=======================

:Web site: http://charlemagne.sourceforge.net/
:Project page: http://sourceforge.net/projects/charlemagne/
:Author: Bob Green
:Email: bob underscore green at speakeasy dot net

I realize this documentation is somewhat less than complete.  Feel free to 
email me with questions, requests, etc.

Overview
========

Charlemagne is a genetic programming application which aims to be highly 
configurable and applicable to a broad range of problems.   It is written 
in Python and Lisp and to some degree is extensible in both languages.  It 
features built-in input-output mapping support, but also provides the 
ability to define complex fitness calculators in Lisp or Python.

This document in no way tries to cover genetic programming itself.  
However, you can explore this application by following the instructions 
below even without knowing alot about genetic programming. 

License
=======

Charlemagne is distributed under the GNU General Public License (GPL).  
Please see the file LICENSE.txt included with the distribution, point your 
browser to http://www.gnu.org/copyleft/gpl.html, type "charlemagne LICENSE" 
from the command line, or from an interactive charlemagne 
session type help(license).

Requirements
============

* Linux / Unix?
* Python 2.x (http://python.org)
* CLISP (http://clisp.cons.org)

Currently, support is limited to Unix-like operating systems, and only 
Linux has been tested.  There is one technical issue preventing Windows 
support right now, but hopefully this will be corrected in the future.

Installation
============

See the file README.txt included with the distribution.  But briefly, as 
root type::

    $ python setup.py install
    
Quick Start
===========

For the impatient, you can try running some of the examples.  Many are 
trivial.  First, make a working copy of the examples directory tree.  From 
your working directory::

    $ cp -r /usr/local/share/charlemagne/examples .

Change into the example0 directory::

    $ cd examples/example0
    
And run the example::

    $ ./example0
    
Then you could try::

    $ cd ../example1
    $ ./example1
    
There are some more difficult problems in example2::

    $ cd ../example2
    
You can run any of::
    
    $ ./cos2x
    $ ./sin2x-easy
    $ ./sin2x-hard
    $ ./tan2x    
        
The problems sin2x-hard and tan2x are non-trivial.  

If you look at the scripts you'll notice all of the examples are just calls 
to charlemagne with command line parameters.  You can try tweaking these if 
you want.  For a description of available command-line options, try::    

    $ charlemagne --help


Interactive Session
===================

Getting Started
---------------

Starting charlemagne in the simplest way possible results in an interactive 
session::

    $ charlemagne
    Charlemagne-2.0.0 (June 10, 2003)
    http://charlemagne.sourceforge.net
    Copyright © 2003 Robert Green.
    Licensed under the GNU General Public License (GPL).
    >>>

This is actually a Python session with some additional user references 
available for controlling the charlemagne application.  The core objects 
are automatically instantiated for you.  The important user reference 
variables are:

    cfg - charlemagne.configurator.TextConfigurator object
    pop - charlemagne.population.ConsolePopulation object 
    lsp - charlemagne.interpreter.CLISPInterpreter object
    
All public methods of these classes are available for interactive 
manipulation.  These instructions cover the most important functionality.


cfg - The Configurator
----------------------

In any interactive session, we are provided a reference to a Configurator 
object through the variable cfg. 

To see the current contents of the configurator::

    >>> cfg.show()
    
You'll see that some of the parameters are configured and others are set to 
None.  The configurator comes initialized with some default values, but 
there are some parameters which must be set before we can move on.  Let's 
configure a few parameters::

    >>> cfg.configure("name")
    Run Name [None]: tutorial

Once again, let's look at the contents of the configurator::

    >>> cfg.show()
    
We can see the name parameter has been modified.  We could have performed 
the same task without resorting to the interactive parameter prompt::

    >>> cfg.configure("name", "tutorial")
        
The remaining mandatory parameters that are not yet set are input, output, 
and vocabulary.  We'll do that now::

    >>> cfg.configure("input", map(lambda x: [x*1.0], range(10)))

If you are familiar with the Python map function and the lambda construct, 
the above will look familiar to you.  If not, this was just a handy way for 
defining the input set as shown below::

    >>> cfg.show("input")
    [[0.0], [1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0], [9.0]]

This is a set of one dimensional input vectors.  In general, the input 
vectors can be of any dimensionality.

We define the output set in similar fashion::

    >>> import math
    >>> cfg.configure("output", map(lambda x: math.sin(2*x), range(10)))
    
This sets the output set to be a list of values corresponding to the input 
set, specifically each output is the sin of its corresponding input::

    >>> cfg.show("output")
    [0.0, 0.8414709848078965, 0.90929742682568171, 0.14112000805986721, 
    -0.7568024953079282, -0.95892427466313845, -0.27941549819892586, 
    0.65698659871878906, 0.98935824662338179, 0.41211848524175659]

The final property which we will set is the vocabulary.  This is the list 
of building blocks the programs can be constructed from.  The vocabulary is 
divided into three parameters: "terminals" - elements which take no 
parameters, "one-args" function which take exactly one argument, and 
"two-args" functions which take exactly two arguments.  We will set the 
vocabulary parameters as follows::

    >>> cfg.configure("terminals")
    Terminals [None]: INPUT1,2.0
    >>>cfg.configure("one-args")
    One Argument Functions [None]: cos,tan
    >>>cfg.configure("two-args")
    Two Argument Functions [None]: +,*,-,%
            
Above, INPUT1 refers to 1st element of the input vector (in this case there 
is only one element of each vector, but in the case of a higher 
dimensionality input set, you enter additional terminals in the form 
INPUT2, INPUT3, etc.)  We also provide the additional terminal element 2.0, 
because it seems likely that having a 2.0 readily available may help in 
this case.

We also provide the one argument functions sin and cos, as well as 
providing the four standard arithmetic operators as the two argument 
functions.  (% is a safe division here, not modulo.  Using the real  
operator will result in divide by zero errors.)  

Currently there is no mechanism for allowing functions which take more 
than two arguments or functions which take an arbitrary number of 
arguments, although this is a planned enhancement.

Note: Although you don't need to do this now, to be prompted for all 
available parameters, we can run configure with no parameters::

    >>> cfg.configure()
    
Pressing enter at any parameter prompt leaves the value of that parameter 
unchanged.  (The current value is display in square brackets to the left of 
the colon in the prompt.)

We are almost done with the configurator, but we still need to *apply* the 
parameters to the environment.  This is done with the command::
    
    >>> cfg.apply()
    
That's all we need to do with the configurator for now, but to see full 
class documentation for the instantiated Configurator, you can type::

    >>> cfg.help()
    
Typing 'q' gets you out of the help system and back to the session prompt.  

    
pop - The Population
--------------------

With all the necessary environment parameters set, we can create the 
initial generation using the pop reference variable::

    >>> pop.populate()
    
After a moment, you should see some statistics printed out.  These are the 
statistics for your generation 0 population.

You can look at the lisp source of all the programs in the 
population by executing::

    >>> pop.show()
    
This is kind of silly, but it shows that there really is a population of 
random programs.  Also for kicks, note::

    >>> len(pop)
    500
    
This shows you the number of programs in the population.  Also try::

    >>> pop[0].show()
    
This shows you the lisp of the first program in the population.
    
Now, let's try getting to the next generation::
    
    >>> pop.next()
        
Here, you'll see a progress bar work across the screen as the population 
is bred.  When complete, the stats for the new generation will be 
calculated and printed.  The variable pop now contains the next generation 
of programs.  Calling pop.next() repeatedly will step the population along 
from generation to generation.  If you want this process to continue until 
a solution is found::

    >>> pop.breed()
    
Since the problem we've defined is non-trivial, the truth is that the 
parameters might take some more tweaking and perhaps a long time before we 
find a solution.  If you do take the time to step through a few 
generations, you should notice the Average Adjusted Fitness of the 
population creeping upwards in the statistics report.

Once you get impatient, type CTRL-C to stop execution.  You exit 
the session the same way as any python session, CTRL-D. 


lsp - The Interpreter
---------------------

When you enter interactive mode, a CLISP session is started in the 
background.  While its possible to use the system without ever explicitly 
referencing this session, there are some cases where it is useful.  

First, its interesting to note that we have a full lisp interpreter at our 
fingertips even if the syntax is a bit more awkward than at a real lisp 
prompt::

    >>> lsp.evaluate("(+ 2 2)")
    '4'

Also notice that this is a persistent lisp session.  We can define 
variables that will remain defined for the remainder of the session::

    >>> lsp.evaluate("(defvar test-var (+ 2 2))")
    'TEST-VAR'
    >>> lsp.evaluate("test-var")
    '4'
    
We can also define functions in this way::

    >>> lsp.evaluate("(defun sin2x (x) (sin (* 2 x)))")
    'SIN2X'
    >>> lsp.evaluate("(sin2x 0.25)")
    '0.47942555'

The utility in this is based on the fact that this is the same lisp 
session that the programs from the population are evaluated in.  For 
instance, we can define functions in this way and then add them to the 
vocabulary::

    >>> cfg.configure("one-args")
    One Argument Functions [None]: cos,tan,sin2x
    >>> cfg.apply()
    
We could also define terminals in this fashion::

    >>> lsp.evaluate("(defvar EARTHS-GRAVITY 9.7982)")
    'EARTHS-GRAVITY'
    
And make them available as part of the terminal vocabulary::

    >>> cfg.configure("terminals")
    Terminals [None]: INPUT1,EARTHS-GRAVITY
    >>> cfg.apply()
        

Command-Line
============

When you're repeatedly setting up the environment for a particulate problem 
it may seem tedious to have to type in commands in interactive mode. For 
this reason, we support scriptable command-line parameters.  Any parameter 
which is available in the configurator can also be initialized via a 
corresponding command-line switch.  We can start an interactive session in 
such a way that some parameters are already set::

    $ charlemagne --name test --crossover 0.9 --replicate 0.1 --mutate 0

The application starts as normal.  To confirm that the specified 
parameters have been set, try::

    >>> cfg.show()

Press CTRL-D at the prompt to exit.

Typing the parameters out on the command-line each time is no easier than 
typing them out in the configurator.  The power of the command-line 
switches is in scripting them.  To illustrate, let's copy the examples that 
are distributed with the package to our working directory::

    $ cp -r /usr/local/share/charlemagne/examples .
    
Change into the example0 directory::    
    
    $ cd examples/example0
        
Now we have some data and vocabulary files available for a trivial problem. 
Create a file 'tutorial' in your working directory as follows::    
    
    #!/bin/bash    
    charlemagne --name tutorial-example --inputs-file inputs.asc 
    --outputs-file outputs.asc --vocabulary-file vocab.asc

Here we are using predefined data files to specify the inputs, outputs and 
vocabulary.       
                    
Make the script executable and run it::
    
    $ chmod +x tutorial
    $ ./tutorial
    
And apply the contents of the configurator to the environment::

    >>> cfg.apply()
    
If we want to enter the application with the configurator having already 
been applied, we can use the APPLY scripting command.

Modify the tutorial script as follows::    

    #!/bin/bash
    charlemagne APPLY --name tutorial-example --inputs-file 
    inputs.asc --outputs-file outputs.asc --vocabulary-file vocab.asc 

This command effectively causes cfg.apply() to be called automatically 
on start up.  The complete list of scripting commands is as follows:

    * MANUAL - activate the online manual, exit when done
    * CONFIGURE - interactive configure, all parameters
    * APPLY - apply
    * POPULATE - apply, populate
    * BREED - apply, populate, breed
    * BATCH - apply, populate, breed, exit

At most, one of these commands should be specified, and it must be the 
first parameter on the command line.  For POPULATE, BREED, and BATCH to 
work, you must also specify all the mandatory, non-defaulted parameters on 
the command-line i.e. the name, input, output, and vocabulary.


Parameters
==========

To get a brief rundown of all available parameters::
 
    $ charlemagne --help

Below is some additional detail on the paramters.


Name (-n, --name)
-----------------
The name of the run.  This is used for logging runs by name.  This 
parameter is mandatory.


Input (--input)
---------------
The list of input vectors, specified Python in the style of Python 
list.  The vectors can be of any dimensionality, but they must be 
consistently so.

Example::

    --input [[1.0,1.0],[1.0,-1.0],[-1.0,1.0],[-1.0,-1.0]]


Terminals (--terminals)
-----------------------
The terminal (atomic) elements of the vocabulary.  The special keywords 
INPUT1, INPUT2, INPUT3, etc. are used to represent the elements of the 
input vector begin evaluated.  The keyword CONSTANT-SYNTHESIS evaluates to 
a random constant in each place it is used.

Example::

    --terminals INPUT1,0,1.0,CONSTANT-SYNTHESIS


One Argument Functions (--one-args)
-----------------------------------
The functional elements of the vocabulary which take exactly one argument.

Example::

    --one-args sin,cos,tan


Two Argument Functions (--two-args)
-----------------------------------
The functional elements of the vocabulary which take exactly two arguments.

Example::

    --two-args +,-,*,%

Note % is a special safe divide function which does not generate divide by 
zero errors.
    

Inputs File (-I, --inputs-file)
-------------------------------
Use data from specified file as the test inputs.  The specified inputs file 
must be an ASCII file with one input vector per line, with each term 
sepeated by commas.  Example inputs file::    
    
    1,1
    -1,1
    1,-1
    -1,-1
    
Use this instead of specifying inputs directly with the Input parameter.


Output (--output)
-----------------
The list of output values, specified in the style of a Python list.  
Each output corresponds to the input vector in the same position in the 
input list

Example::

    --output [2.0,0,0,-2.0]

The Output parameter is for use with the (default) OUTPUT 
deviance-calculation method.

    
Outputs File (-O, --outputs-file)
---------------------------------
Use data from specified file correct test output.  The outputs file should 
be an ASCII file with one output per line.  The Outputs File parameter is 
mandatory unless you use --generate-outputs to generate the correct output 
values, or you use a --deviance-calculation method other than the default 
OUTPUT method.  Example outputs file::

    2
    0
    0
    -2
    
Use this instead of specifying the outputs directly with the Output 
parameter.


Generate Outputs (--generate-outputs)
-------------------------------------
Generate output values from the input values using the specified method.  
If you generate outputs with this option using either method, neither 
--outputs or --outputs-file should be specified. 

Available methods are:

* LISP-EXPRESSION=<expr>
* PYTHON-CLASS=<module>.<classname>
  
LISP-EXPRESSION output generation requires that you specify a full lisp 
expression which uses lisp variables of the form INPUT1 INPUT2, etc. to 
operate on the input data.  

PYTHON-CLASS output generation requires that you create an 
charlemagne.outputgenerator.OutputGenerator subclass which implements the 
generate() method to return an output list.  


Vocabulary File (-V, --vocabulary-file)
---------------------------------------   
Use vocabulary defined in specified file.  The vocabulary file must be an 
ASCII file of the following form:  It should be exactly three lines long 
with the first line being a command seperated list of available terminals 
values.  The second line should be a comma seperated list of available 
functions which take exactly one argument.  The third and final line should 
be a comma seperated list of available functions which take exactly two 
arguments.  Example vocabulary file::

    INPUT1,1.0,PI
    sin,cos,tan
    -,+


Population Size (-S, --population-size)
---------------------------------------
Use a population of the specified size.


Maximum Initial Depth (-d, --initial-depth)
-------------------------------------------
Start with random programs no deeper than the specified depth.


Maximum Depth (-D, --maximum-depth)
-----------------------------------
Restrain programs to the maximum depth specified.  This prevent crossovers 
and mutations from endless growing the average depth of the population.  


Standard Crossover Probability (-C, --crossover)
------------------------------------------------
Perform the standard crossover operation with the specified probability.  


Context Sensitive Crossover Probability (-P, --cs-crossover)
------------------------------------------------------------
Perform the context sensitive crossover operation with the specified 
probability.


Replicate Probability (-R, --replicate)
---------------------------------------
Perform the replicate operation with the specified probability.


Mutate Probability (-M, --mutate)
---------------------------------
Perform the mutate operation with the specified probability.


Selection Method (--selection)
------------------------------
Use the specified selection method. 

Available methods are:

* FITNESS-PROPORTIONATE=<degree>
* TOURNAMENT=<size>.  

FITNESS-PROPORTIONATE selection prefers fit to unfit programs and degree is 
a measure of how tightly bound this selection is.  A degree of 1.0 is very 
greedy toward fit programs, numbers less than 1 are proportionately less 
greedy.

TOURNAMENT selection randomly selects programs from the population 
and holds a tournament of the specified size.  The best program in the 
tournament is selected.


Precision (--precision)
-----------------------
Use the specified precision in determining hits.


Force Best (--force-best)
-------------------------
Force the best program to replicate into the new generation the specified 
number of times.
  

Fitness Environment File (--fitness-environment)
------------------------------------------------
Evaluate fitness-function in the lisp environment created by the specified 
lisp file.  


Deviance Calculation (--deviance-calculation)
---------------------------------------------
Calculate deviance using the specified method.  

Available methods are:

* OUTPUT
* LISP-FUNCTION=<name>
* PYTHON-CLASS=<module>.<classname>
  
The OUTPUT method uses the difference between the actual output and the 
output list to directly calculate the deviance.  This is the default method 
and is useful if you are searching for a mapping or approximation function 
which maps a set of inputs to a set of outputs.

The LISP-FUNCTION method uses the output of the specified lisp function as 
the deviance.  The function should take exactly one argument which is the 
lisp expression of the program to be calculated for.

The PYTHON-CLASS method requires that you must create a
charlemagne.deviancecalculator.InputDevianceCalculator subclass which 
implements calculate() to return the deviance a program.

Both the LISP-FUNCTION and PYTHON-CLASS methods are suitable for complex 
domains where the fitness of an indivual is a more involved measure than 
just its ability to map input to output.  With these methods it is possible 
to measure deviance in terms of complex multi-step simulations.  If you're 
using either of these two methods, you do not specify --output or 
--outputs-file, as the output of the program being tested could be 
something much more intangible.  For example, if you were searching the 
space of checkers playing programs, you could write a lisp function 
checkers-deviance, or define a Python class CheckersDevianceCalculator, 
which interfaced with a checkers simulation and returns some measure of how 
well a particular program played the game.  When defining deviance 
calculators, a deviance of zero is the perfect program with the higher the 
deviance is, the worse that program is.

"""

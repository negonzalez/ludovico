"""

==================
Charlemagne README
==================

:Web site: http://charlemagne.sourceforge.net/
:Project page: http://sourceforge.net/projects/charlemagne/
:Author: Bob Green
:Email: bob underscore green at speakeasy dot net

-------
License
-------

Charlemagne is distributed under the GNU General Public License (GPL). 
Please see the file LICENSE.txt or http://www.gnu.org/copyleft/gpl.html for 
more information.
    
------------
Installation
------------
    
Linux
-----
To install from source tarball to the default place, execute::

    $ python setup.py install

See the Distutils documentation for many command-line options as to 
installation locations, etc.

Windows (or lack thereof)
-------------------------
It turns out there's a little more to getting it running on Windows then I 
initially realized.  I am using W. Michael Petullo's PipeDream module for 
low-level pipe communications with the lisp interpreter relies on os.fork() 
which is not available on Windows.  It's on the TODO come up with an 
alternate implementation of this.  Once this is corrected, there will 
be a .exe installer for Windows.        

-------------
Documentation
-------------

To browse documentation from the command-line::

    $ charlemagne MANUAL

To browse the documentation from an interactive session::

    >>> help(manual)

Incidently, you can few this readme at any time with::

    $ charlemagne README
    
Or, from within an interactive charlemagne session::

    >>> help(readme)
        
"""

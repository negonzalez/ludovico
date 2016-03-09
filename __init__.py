"""
Charlemagne package

Web site: http://charlemagne.sourceforge.net
Project page: http://sourceforge.net/projects/charlemagne
Email: bob underscore green at speakeasy dot net

To view the manual from a command prompt:

    $ charlemagne MANUAL

To get help for command-line options:

    $ charlemagne --help
    
To start an interactive session:

    $ charlemagne
    
To view the manual from an interactive session:

    >>> help(manual)
    
To get help on a specific module from this package:

    >>> help(<module name>)
    
"""

def Help(topic=None):

    if topic==None:
        import charlemagne
        help(charlemagne)
    else:
        if type(topic)==str:
            pass
        else:
            help(topic)
        

#S = topic.split('.')
#classname = S[-1]
#module = ""
#for s in S[:-1]:
#    module += s
#if module=="":
#    target = getattr(__import__("charlemagne"), classname)
#else:
#    module = "charlemagne." + module
#    target = getattr(__import__(module), classname)
#help(target)



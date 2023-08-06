# -*- coding: utf-8 -*-
"""
Handy Functions and variables/constants for use at iPython prompt
   call mine() for full list of functions and variables.

Created on Sat Feb  1 15:05:51 2020
     ------ Time-stamp: <2020-09-01T13:58:54.955110-04:00 cws2> ------
     
@author: Carl Schmiedekamp

2020-04-14 /CS/ adding 'mine()' to list what has been setup by handies.py
                adding atan2P(y,x) to return positive angle.
2020-04-17 /CS/ adding astropy.units as 'u'
2020-07-13 /CS/ removing cdpy1d(), and cdWD()
2020-07-22 /CS/ making astropy and func_timeout optional.
2020-07-25 /CS/ added timeStampStr()
                changed from file date/time to timestamp file as mod. time
                for this module, also added the version from __init__.py.
                Added variable "__version__" which holds the version.
2020-07-29 /CS/ added isInstalled()
2020-08-13 /CS/ added condaEnvName() as a helper function.
2020-08-25 /CS/ added 'line magic' cls to fill screen with 23 blank lines.
                the 'Loading' message is not output if not in interpreter,
                i.e. if IsInteractive flag is False.
2020-09-02 /CS/ Now sets ipython number precision to 5 digits.
                  (Note: only for expression evaluation output.)

"""


## Shortcuts etc. functions.
import math
import codecs
from math import pi, sqrt, cos, sin, tan
from math import acos, asin, atan, atan2, degrees, radians
from math import log, log10, exp

from random import randint

def randomLetter():
    '''
    Generate a single random uppercase ASCII letter

    Returns
    -------
    TYPE
        char.
    '''
    import random
    import string    
    return random.choice(string.ascii_uppercase)

def randomElement( List=(1,2,3,4,5,6,7, 'oops')):
    '''
    return random element of list

    '''
    index = randint(0, len( List))
    return List[ index]


def timeStampStr():
    '''Returns a string with the current time in ISO format.'''
    import datetime
    import time
    
    dt = datetime.datetime.now()
    epoch = dt.timestamp() # Get POSIX timestamp of the specified datetime.
    st_time = time.localtime(epoch) #  Get struct_time for the timestamp. This will be created using the system's locale and it's time zone information.
    tz = datetime.timezone(datetime.timedelta(seconds = st_time.tm_gmtoff)) # Create a timezone object with the computed offset in the struct_time.
    return dt.astimezone(tz).isoformat()

import math
## math.comb is in Python 3.8 
if hasattr( math, "comb" ):
    from math import comb
    from math import comb as nCr
else:
    def nCr(n,r):
        ''' calculate number of combinations of r from n items.'''
        f = math.factorial
        return f(n) // f(r) // f(n-r)
    comb = nCr    

from platform import python_version
import sys, os.path, time, os


def hostname():
    '''Returns 'fully qualified domain name' '''
    import socket
    return socket.getfqdn()


def getTS( rel_path):
    '''Reads first line of specified file, which is expected to be a time-date
    string.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as tsf:
        lines = tsf.read()
    linelist = lines.splitlines()
    return linelist[0]


def read(rel_path):
    '''Reads text file.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    '''Reads version from specified file. The file path is relative
    to this file. It looks for line that starts with "__version__"'''
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


## set IsInteractive flag and define cls as line magic
IsInteractive = False
try:
    from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)
    ## Ref: https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
    ## Ref: https://ipython.readthedocs.io/en/stable/config/custommagics.html
    
    try:
        if sys.ps1:
            IsInteractive = True
        
    except AttributeError:
        interpreter = False
        if sys.flags.interactive: IsInteractive = True
        
        
    if IsInteractive:
        ### set default float precision
        ### Ref: https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
        from IPython import get_ipython
        ipython = get_ipython()
        ipython.magic( 'precision "%0.5g"')
        
        ### define clear screen magic (%cls generates 23 blank lines)
        @register_line_magic 
        def cls(line): 
            '''Defines a 'clear screen' line magic'''
            print( 23*'\n') 
            return
            
except ( ModuleNotFoundError, ImportError):
    IsInteractive = False
else:
    del cls ## must delete function to make magic visible.

    

######  'Welcome Message' on loading  ######

def condaEnvName():
    '''Gets environment name from python's path.
    Ref:
        https://stackoverflow.com/questions/36539623/how-do-i-find-the-name-of-the-conda-environment-in-which-my-code-is-running'''

    # return Path(sys.executable).as_posix().split('/')[-3]
    return sys.exec_prefix.split(os.sep)[-1]

timestamp = getTS( 'timestamp.txt') ##
date  = timestamp[0:10]
# print('DBug: date: {} TS:\n{}'.format( date, timestamp))

__version__=get_version("__init__.py")

if IsInteractive:
    print( "Loading Carl's handies.py ver: {} {}; Python:{}; ENV:{}".format( 
        __version__, date, python_version(), condaEnvName())) 

def call( cmd):
    import subprocess
    '''Modeled after call function in NANOGrav Sprinng 2020 workshop.
    call() just executes the command in the shell and displays output,
    while runCatch( cmd) tries to catch all errors and output and only returns
    True or False to indicate success or failure.
    Could have security issues. See subprocess documentation.'''
    subprocess.call( cmd, shell=True)

def isInstalled( pkgname):
    ''' Imports pkgname and returns package if installed.
        pkgname is a string with name of package as used in import stmt.
        If not installed, returns None.
        Typical Usage:
            astropy = isInstalled( 'astropy') 
            if astropy == None:
                ... 
            else:
                from astropy import units as u
        '''
    try:
        pkg = __import__( pkgname)
        return pkg
    except Exception:
    	return None


def mine():

    '''List the functions and variables defined in handies.py'''
    print('\n handies.py ver: {}, modified {}, python {}'.format(
        __version__, date, python_version()))
    if isInstalled( 'astropy'):
        print('Defining:\n     nowMJD(); mjd2date(), date2mjd(),')
        print('     astropy.units as "u", i.e. u.cm or u.GHz')
    print('     cdbn(), osname(), hostname(), call(),')
    if isInstalled( 'PyQt5'):
        print('     select_file(), select_file_timeout( timeout={}),'.format( sfTimeOut))
    print('     rad(), deg(), sinD(), cosD(), tanD(), asinD(),\n     acosD(), atanD(), atan2D(), atan2P()')
    print("       'D' and 'P' functions work with degrees.")
    print("       'P' inverse functions return only positive angles.")
    print("Defines nCr AKA comb or imports from math if available.")
    print('     greeks  ➞ a string with greek alphabet.')
    print('     pltsize( w, h) ➞ resizes plots in matplotlib, units are inches')
    print('     timeStampStr() ➞ returns a readable timestamp string.')
    print('     isInstalled( pkgNameStr) ➞ returns package or None if not installed.')
    print('     randomLetter() ➞ a random uppercase ASCII letter.')
    print('     randomElement( List) ➞ returns random element from list.')

    print('From random imports randint( min, max)')
    
    print('From math imports:\n     pi, sqrt, degrees, radians,\n     cos, sin, tan, atan2, asin, acos, atan, and\n' + 
      '     log, log10, exp')

    print( '\n     mine() ➞ lists what handies.py defines.')

    print( '\nIf astropy package is not available, "u" and the mjd functions are not defined.')
    print( 'If PyQt5 package is not available, the select_file functions are not defined.')
    print( 'If func_timeout package is not availabe, the select_file_timeout ignores the'+\
           ' timeout value.')
    
##Ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-precision
    prhints = ('Hint:\n' + 
          '     "%precision %g" or %.6g for better number formats.')
    print(prhints)


def cosD( ang):
    '''Return cosine of angle in degrees.'''
    import math as m
    return m.cos( m.radians( ang))

def sinD( ang):
    '''Return sine of angle in degrees.'''
    import math as m
    return m.sin( m.radians( ang))

def tanD( ang):
    '''Return tangent of angle in degrees.'''
    import math as m
    return m.tan( m.radians( ang))

def asinD( val):
    '''Return inverse sine, in degrees, of val.'''
    import math as m
    return  m.degrees( m.asin( val))

def acosD( val):
    '''Return inverse consine, in degrees, of val.'''
    import math as m
    return m.degrees( m.acos( val))


def atanD( val):
    '''Return inverse tangent, in degrees, of val.'''
    import math as m
    return m.degrees( m.atan( val))


def atan2D( y, x):
    '''Return inverse tangent, in degrees, of y/x. (-180 ... 180)'''
    import math as m
    return m.degrees( m.atan2( y, x))

def atan2P( y, x):
    '''Return inverse tangent, in degrees, of y/x. (0 .. 360)'''
    ang = atan2D( y, x)
    if ang <0:
        ang = ang + 360
    return ang

rad = radians  ## alias the conversion functions
deg = degrees

greeks = ' Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω  α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω '

def cdbn( dirname, sub=None):
    '''cd to directory (or subdirectory) who's path is in Env.Var. who's name is passed as
       first argument.  2nd argument specifies a subdirectory relative to
       that named directory.'''
    import os
    """ Does cd to directory named in specified environment
        variable.
        Returns True if no error.
        If Error, returns False and prints msg.
        --
        If sub is specified, tries to cd to that subdirectory
        after the cd to the contents of env. var.
    """
    try:
        dir = os.environ[ dirname]
    except KeyError:
        print( dirname, ': not an env. var.')
        return False
    else:
        if os.access( dir, os.R_OK):
            os.chdir( dir)
            if sub==None:
                return True
            else:
                if os.access( sub, os.R_OK):
                    os.chdir( sub)
                    return True
                else:
                    print( '{}: No access!'.format( 
                            os.path.join(dir,sub), dir))
            return False

        else:
            print('[{}] --> {} : No access!'.format( dirname, dir))
            return False


# def cdpy1d():
#     '''cd to Pythonista dir. in OneDrive'''
#     return cdbn('MYonedrivepsu', 'Pythonista')
#
# def cdWD():
#     '''cd to SinglePulse/WorkingDir.'''
# # #     ##os.chdir( r'C:\Users\hedfp\OneDrive - The Pennsylvania State University\InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir')
#     return cdbn('MYonedrivepsu', 'InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir' )
#

try:
    import astropy
    from astropy import units as u
    
    def nowMJD():
        '''Convert current time to MJD'''
        from astropy.time import Time
        return Time.now().to_value( 'mjd')
    
    def mjd2date( mjd):
        '''Convert MJD to a civil date/time'''
        
        from astropy.time import Time
        time = Time( mjd, format='mjd')
        return time.to_datetime()
    
    def date2mjd_( civildate):
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778'''
        
        from astropy.time import Time
        return Time( civildate).to_value( 'mjd', 'long')
        
    def date2mjd( civildate):
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
        As a special case, if the date/time is followed by UTC offset
        then that is used to shift the date/time to UTC.
        Example: 2019-09-30 20:54:54-04:00 corresponds to 
        UTC of 2019-10-01 00:54:54
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778
            or
            date2mjd( '2020-05-16T14:10-04:00') returns 58985.756944444444446
            '''
        
        cd = civildate
        offset = 0
        ## check for special case:
        if cd[-3]==':' and ( cd[-6]=='-' or cd[-6]=='+') :
            offset = (int( cd[-5:-3]) + int( cd[-2:])/60 )/24
            if cd[-6]=='+':
                offset = -offset
            cd = cd[:-6]
        
        from astropy.time import Time
        return Time( cd).to_value( 'mjd', 'long')+offset
except ImportError:
    print( 'mjd functions not defined because astropy is not available.')


def pltsize( w, h, dpi=150):
    '''set plot size (matplotlib), size in notebook depends on resolution ond
    browser settings. However, doubling the values should double the size.
    dpi is dots-per-inch which also changes plot size in notebooks.'''
    import matplotlib
    matplotlib.rc('figure', figsize=[w,h], dpi=dpi)

def osname():
    '''Returns name of operating system that Python is running on.'''
    import os
    return os.uname().sysname

try:
    import PyQt5  ## used in fdtest module, skip these definitions if Qt5 not available.
    
    ## default timeout (in s) for select_file():
    sfTimeOut = 95

    def select_file( ):
        ''' Uses fdtest.py to browse for file and return its path.
        WARNING: This function will 'hang' until a file is selected.'''
        
        from classroom_gizmos.fdtest import gui_fname        
        return gui_fname()

    def select_file_timeout( timeout=sfTimeOut):
        ''' Uses fdtest.py to browse for file and return its path.
        If the fdtest call takes longer than 'timeout' seconds,
        the attempt is cancelled and None is returned.
        The argument, timeout, sets the number of seconds before time out.
        Note: if func_timeout package is not available, the no timeout
        is used (select_file() is called.)
        '''
        ## trying to do auto-install of func_timeout
        try:
            from func_timeout import func_timeout, FunctionTimedOut
        except ImportError:
            from classroom_gizmos.import_install import ii
            func_timeout = ii( 'func_timeout')
            try:
                from func_timeout import func_timeout, FunctionTimedOut
            except Exception:
                print( 'Timeout is not available.')
                return select_file()
            
        from classroom_gizmos.fdtest import gui_fname
        
        try:
            filename = func_timeout( timeout, gui_fname, args=()).decode("utf-8")
        except FunctionTimedOut:
            outstr = 'select_file cound not complete within '
            outstr += '{} seconds.\n'.format( timeout)
            print( outstr)
            #raise e
            filename = None
            
        return filename
except ImportError:
    print( 'select_file functions not defined because PyQt5 is not available.')


if __name__ == "__main__":
    mine()
    
    
    

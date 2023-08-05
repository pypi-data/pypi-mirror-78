#! /usr/bin/env python3
""" ### *** This is not the original python source code ***
    This is a variation on the python3 timeit function from python 3.8.5 and
    is covered by the PSF license. A copy is included at the end of this file
    or it can be found here: https://docs.python.org/3/license.html


    ####* Original (modified) docstring starts here:
    Tool for measuring execution time of small code snippets.

    This module avoids a number of common traps for measuring execution
    times.  See also Tim Peters' introduction to the Algorithms chapter in
    the Python Cookbook, published by O'Reilly.

    Library usage: see the Timer class.

    Command line usage:
        python timeit.py [-n N] [-r N] [-s S] [-p] [-h] [--] [statement]

    Options:
    -n/--number N: how many times to execute 'statement' (default: see below)
    -r/--repeat N: how many times to repeat the timer (default 5)
    -s/--setup S: statement to be executed once initially (default 'pass').
                    Execution time of this setup statement is NOT timed.
    -p/--process: use time.process_time() (default is time.perf_counter())
    -v/--verbose: print raw timing results; repeat for more digits precision
    -u/--unit: set the output time unit (nsec, usec, msec, or sec)
    -h/--help: print this usage message and exit
    --: separate options from statement, use when statement starts with -
    statement: statement to be timed (default 'pass')

    A multi-line statement may be given by specifying each line as a
    separate argument; indented lines are possible by enclosing an
    argument in quotes and using leading spaces.  Multiple -s options are
    treated similarly.

    If -n is not given, a suitable number of loops is calculated by trying
    increasing numbers from the sequence 1, 2, 5, 10, 20, 50, ... until the
    total time is at least 0.2 seconds.

    Note: there is a certain baseline overhead associated with executing a
    pass statement.  It differs between versions.  The code here doesn't try
    to hide it, but you should be aware of it.  The baseline overhead can be
    measured by invoking the program without arguments.

    Classes:

        Timer

    Functions:

        timeit(string, string) -> float
        repeat(string, string) -> list
        default_timer() -> float

    """

import sys
from .timeit import *

if __name__ == "__main__":
    from ._cli import main
    sys.exit(main())

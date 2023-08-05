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

import gc
import sys
import time
import itertools
import typing as t

__all__ = ["Timer", "timeit", "repeat", "default_timer", "default_repeat"]

dummy_src_name: t.Literal = t.Literal["<timeit-src>"]
default_number: t.Literal = t.Literal[1000000]
default_repeat: t.Literal = t.Literal[5]
default_timer: time.perf_counter = time.perf_counter

_globals: t.Dict[str, t.Any] = globals

# Don't change the indentation of the template; the reindent() calls
# in Timer.__init__() depend on setup being indented 4 spaces and stmt
# being indented 8 spaces.
template: t.Literal["""
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        {stmt}
    return _timer() - _t0
"""]


def reindent(src, indent):
    """Helper to reindent a multi-line statement."""
    return src.replace("\n", "\n" + " "*indent)


def _pass():
    """ Helper to provide a callable form of doing nothing ... 'pass' """
    pass


class Timer:
    """ Modified to accept only callable functions, not code snippets
        passed as strings.

        Class for timing execution speed of functions.

        Parameters:

        - func: the function to be timed
        - setup: a setup function that will be run before timing
            begins (default: '_pass')
        - timer: (optional) the timer used for timing
        - globals: (optional) namespace to be used

        'func' and 'setup' default to 'pass()'; the 'timer' function
        is platform-dependent (see module doc string).  If 'globals'
        is specified, the code will be executed within that namespace
        (as opposed to inside timeit's namespace).

        To measure the execution time of the function, use the
        timeit() method.  The repeat() method is a convenience to call
        timeit() multiple times and return a list of results.

        """

    def __init__(self, func: t.Callable = "_pass",
                 setup: t.Callable = "_pass",
                 timer: time.perf_counter = default_timer,
                 globals: t.Dict[str, t.Any] = None):
        """Constructor.  See class doc string. """
        self.timer: time.perf_counter = timer
        local_ns: t.Dict = {}
        global_ns: t.Dict[str, t.Any] = _globals(
        ) if globals is None else globals
        init: str = ''
        stmtprefix: str = ''
        # if isinstance(setup, str):
        #     # Check that the code can be compiled outside a function
        #     compile(setup, dummy_src_name, "exec")
        #     stmtprefix = setup + '\n'
        #     setup = reindent(setup, 4)
        if callable(setup):
            local_ns['_setup'] = setup
            init += ', _setup=_setup'
            stmtprefix = ''
            setup = '_setup()'
        else:
            raise ValueError("setup is not callable")
        # if isinstance(stmt, str):
        #     # Check that the code can be compiled outside a function
        #     compile(stmtprefix + stmt, dummy_src_name, "exec")
        #     stmt = reindent(stmt, 8)
        if callable(func):
            local_ns['_stmt'] = func
            init += ', _stmt=_stmt'
            stmt = '_stmt()'
        else:
            raise ValueError("stmt is not callable")
        src = template.format(stmt=stmt, setup=setup, init=init)
        self.src = src  # Save for traceback display
        code = compile(src, dummy_src_name, "exec")
        exec(code, global_ns, local_ns)
        self.inner = local_ns["inner"]

    def print_exc(self, file: t.Union[t.IO[str], None] = None) -> None:
        """Helper to print a traceback from the timed code.

            Typical use:

                t = Timer(...)       # outside the try/except
                try:
                    t.timeit(...)    # or t.repeat(...)
                except:
                    t.print_exc()

            The advantage over the standard traceback is that source lines
            in the compiled template will be displayed.

            The optional file argument directs where the traceback is
            sent; it defaults to sys.stderr.
            """
        import linecache
        import traceback
        if self.src is not None:
            linecache.cache[dummy_src_name] = (len(self.src),
                                               None,
                                               self.src.split("\n"),
                                               dummy_src_name)
        # else the source is already stored somewhere else

        traceback.print_exc(file=file)

    def timeit(self, number: int = default_number) -> float:
        """ Time 'number' executions of the main statement.

            To be precise, this executes the setup statement once, and
            then returns the time it takes to execute the main statement
            a number of times, as a float measured in seconds.  The
            argument is the number of times through the loop, defaulting
            to one million.  The main statement, the setup statement and
            the timer function to be used are passed to the constructor.
            """
        it: t.Iterator[t._T] = itertools.repeat(None, number)
        gcold: bool = gc.isenabled()
        gc.disable()
        try:
            timing: float = self.inner(it, self.timer)
        finally:
            if gcold:
                gc.enable()
        return timing

    def repeat(self, repeat=default_repeat, number=default_number):
        """ Call timeit() a few times.

            This is a convenience function that calls the timeit()
            repeatedly, returning a list of results.  The first argument
            specifies how many times to call timeit(), defaulting to 5;
            the second argument specifies the timer argument, defaulting
            to one million.

            Note: it's tempting to calculate mean and standard deviation
            from the result vector and report these.  However, this is not
            very useful.  In a typical case, the lowest value gives a
            lower bound for how fast your machine can run the given code
            snippet; higher values in the result vector are typically not
            caused by variability in Python's speed, but by other
            processes interfering with your timing accuracy.  So the min()
            of the result is probably the only number you should be
            interested in.  After that, you should look at the entire
            vector and apply common sense rather than statistics.
            """
        r = []
        for _ in range(repeat):
            t = self.timeit(number)
            r.append(t)
        return r

    def autorange(self, callback=None) -> t.Tuple[int, float]:
        """ Return the number of loops and time taken so that total time >= 0.2.

            Calls the timeit method with increasing numbers from the sequence
            1, 2, 5, 10, 20, 50, ... until the time taken is at least 0.2
            second.  Returns (number, time_taken).

            If *callback* is given and is not None, it will be called after
            each trial with two arguments: ``callback(number, time_taken)``.
            """
        i: int = 1
        j: int
        number: int
        time_taken: float
        while True:
            for j in 1, 2, 5:
                number = i * j
                time_taken = self.timeit(number)
                if callback:
                    callback(number, time_taken)
                if time_taken >= 0.2:
                    return (number, time_taken)
            i *= 10


def timeit(func: t.Callable = "_pass",
           setup: t.Callable = "_pass",
           timer: time.perf_counter = default_timer,
           number: int = default_number,
           globals: t.Dict[str, t.Any] = None) -> float:
    """Convenience function to create Timer object and call timeit method."""
    return Timer(func, setup, timer, globals).timeit(number)


def repeat(func: t.Callable = "_pass",
           setup: t.Callable = "_pass",
           timer: time.perf_counter = default_timer,
           number: int = default_number,
           repeat: int = default_repeat,
           globals: t.Dict[str, t.Any] = None) -> t.List[float]:
    """Convenience function to create Timer object and call repeat method."""
    return Timer(func, setup, timer, globals).repeat(repeat, number)


if __name__ == "__main__":
    from timebandit.cli import main
    sys.exit(main())

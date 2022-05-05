# cython: language_level=3
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string
from libcpp.complex cimport complex
import os
import sys
from contextlib import contextmanager

cdef extern from "FitResults.h":
    cdef cppclass FitResults:
        FitResults(const string& inFile)
        double likelihood()
        pair[double, double] intensity(vector[string]& amplitudes, bint accCorrected)
        pair[double, double] total_intensity "intensity"(bint accCorrected)
        pair[double, double] phaseDiff(string& amp1, string& amp2)
        complex[double] productionParameter(string& ampName)
        vector[string] ampList()

cdef class CyFitResults:
    cdef FitResults *cobj

    def __init__(self, string inFileStr):
        self.cobj = new FitResults(inFileStr)
        if self.cobj == NULL:
            raise MemoryError('Not enough memory.')

    def __del__(self):
        del self.cobj

    def likelihood(self) -> double:
        return self.cobj.likelihood()

    def intensity(self, amps, acc):
        return self.cobj.intensity(amps, acc)

    def total_intensity(self, acc):
        return self.cobj.total_intensity(acc)

    def phaseDiff(self, amp1, amp2):
        return self.cobj.phaseDiff(amp1, amp2)

    def productionParameter(self, amp):
        return self.cobj.productionParameter(amp)

    def ampList(self):
        return self.cobj.ampList()


@contextmanager
def stdout_redirected(to=os.devnull):
    '''
    solution by jfs at https://stackoverflow.com/questions/5081657/how-do-i-prevent-a-c-shared-library-to-print-on-stdout-in-python
    import os

    with stdout_redirected(to=filename):
        print("from Python")
        os.system("echo non-Python applications are also supported")
    '''
    fd = sys.stdout.fileno()

    ##### assert that Python and C stdio write using the same file descriptor
    ####assert libc.fileno(ctypes.c_void_p.in_dll(libc, "stdout")) == fd == 1

    def _redirect_stdout(to):
        sys.stdout.close() # + implicit flush()
        os.dup2(to.fileno(), fd) # fd writes to 'to' file
        sys.stdout = os.fdopen(fd, 'w') # Python writes to fd

    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open(to, 'w') as f:
            _redirect_stdout(f)
        try:
            yield # allow code to be run with the redirected stdout
        finally:
            _redirect_stdout(old_stdout) # restore stdout.
                                            # buffering and flags such as
                                            # CLOEXEC may be different


# might be redundant
class FitResultsWrapper:
    def __init__(self, inFileStr):
        self.fitobj = CyFitResults(inFileStr.encode('utf-8'))

    def likelihood(self):
        with stdout_redirected():
            return self.fitobj.likelihood()

    def intensity(self, amps, acc):
        with stdout_redirected():
            return self.fitobj.intensity([amp.encode('utf-8') for amp in amps], acc)

    def total_intensity(self, acc):
        with stdout_redirected():
            return self.fitobj.total_intensity(acc)

    def phaseDiff(self, amp1, amp2):
        with stdout_redirected():
            return self.fitobj.phaseDiff(amp1.encode('utf-8'), amp2.encode('utf-8'))

    def productionParameter(self, amp):
        with stdout_redirected():
            return self.fitobj.productionParameter(amp.encode('utf-8'))

    def ampList(self):
        with stdout_redirected():
            return self.fitobj.ampList()

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
A set of exceptions for pandeia to raise

The web interface will recognize any of these exceptions and produce a
pretty and user-friendly (to the extent that you gave good text) error
message.

"""
from __future__ import division, absolute_import
import re


class PandeiaException(Exception):

    """superclass of all custom pandeia exceptions

    This exception contains these fields of interest:

        message - the message provided by the code that raised the exception

        results - the results dict that the engine was working on at the
            time of the exception (this may be an empty dictionary if the
            engine code cannot provide it)

    """

    def __init__(self, value='Unspecified Error', results=None):
        Exception.__init__(self, value)
        self.results = results
        self.name = "Unspecified Pandeia exception"

    def addinfo(self, more_info):
        """ A convenience method so a calling function can add additional
        information to a raised exception before reraising.
        """
        args = list(self.args)
        args[0] = str(args[0]) + " " + str(more_info)
        self.args = tuple(args)

        # self.message is deprecated as of python 2.6, but we must set it
        # now in order to get the desired behavior.
        self.message = self.args[0]

# Errors resulting not from user inputs, but coding or connection problems.

class EngineOutputError(PandeiaException):

    """
    an engine error that is probably related to engine output

    raise engine.exceptions.OutputError( 'descriptive text', result_dict )

    The result dict is the partially completed result dictionary that the
    engine would have returned if it could finish the calculation.

    This error should include the etcid that issued it

    As used, these are problems with bad data in $pandeia_refdata and engine coding.

    """

    def __init__(self, value="Output Error", results=None):
        PandeiaException.__init__(self, value)
        self.name = "Output Error"

class InternalError(PandeiaException):

    """
    an error that should not have happened and is probably a bug
    We should include the etcid in the error information?
    """

    def __init__(self, value="Internal Error", results=None):
        PandeiaException.__init__(self, value)
        self.name = "Internal Error"

class UnsupportedError(PandeiaException):

    """ Certain cases are 'available' but 'unsupported'.
    Raise this exception for those cases.
    """

    def __init__(self, value, results=None):
        PandeiaException.__init__(self, value, results)
        self.name = "Unsupported Option Selected"

class DataConfigurationError(PandeiaException):

    """
    an engine error that is probably related to configuration data

    raise engine.exceptions.DataConfigurationError( 'descriptive text', result_dict )

    The result dict is the partially completed result dictionary that the
    engine would have returned if it could finish the calculation.

    This error should include the etcid that issued it

    """

    def __init__(self, value="Data Configuration Error", results=None):
        PandeiaException.__init__(self, value)
        self.name = "Data Configuration Error"


class DataError(PandeiaException):

    """'
    Some data entity which should exist cannot be found
    """

    def __init__(self, value="Data Error", results=None):
        PandeiaException.__init__(self, value)
        self.name = "Data Error"

# ### USER INPUT ERRORS ### #

class UserInputError(PandeiaException):
    """
    Parent class for all pandeia exceptions that arise from improper input data.
    These are errors that simply retrying a calculation will not fix.
    """

    def __init__(self, value="User Input Error", results=None):
        PandeiaException.__init__(self, value)
        self.name = value


class EngineInputError(UserInputError):

    """
    an engine error that is probably related to user input

    raise engine.exceptions.EngineInputError( 'descriptive text', result_dict )

    The result dict is the partially completed result dictionary that the
    engine would have returned if it could finish the calculation.

    This error should include the etcid that issued it

    """

    def __init__(self, value="Input Error", results=None):
        UserInputError.__init__(self, value)
        self.name = "Input Error"


class SynphotError(UserInputError):

    """ Any problem that arises from synphot should raise
    this exception
    """

    def __init__(self, value, results=None):
        # Inspired by https://stackoverflow.com/questions/50618116/regex-for-finding-file-paths
        # this will only work for file paths on UNIX systems - not Windows
        # It will also attempt to remove (and therefore mangle) URLs, however
        # at the moment there are no known Synphot errors containing URLs.
        fixvalue = re.sub(r"(\/.*/)", "", value)
        UserInputError.__init__(self, fixvalue, results)
        self.name = "Synphot Error"

class RangeError(UserInputError):

    """ Any problem caused by some value (usually a wavelength) falling
    outside a valid range should raise this exception.
    """

    def __init__(self, value, results=None):
        UserInputError.__init__(self, value, results)
        self.name = "Value Out of Range"


class WavesetMismatch(UserInputError):

    """ Raised when attempting to combine spectra of different
    wavelength sets
    """

    def __init__(self, value, results=None):
        UserInputError.__init__(self, value, results)
        self.name = "Inconsistent wavelength arrays"

# ### UNUSED PYETC EXCEPTIONS ### #

#class BadEnumeration(PandeiaException):
#
#    """
#    use this when an input field is expected to be one of a list of
#    known values, but it is not.
#    """
#
#    def __init__(self, value=None, results=None, field=None):
#        PandeiaException.__init__(self, value, results)
#        self.name = "Unrecognized Option"

# Make new exceptions here, if necessary.  Subclasses of InputError
# and InternalError require nothing special.  New subclasses of
# PandeiaException require new code in etc_web/etc/views.py

#class CalculationError(PandeiaException):
#
#    """ A catch-all exception for otherwise nonspecific exceptions
#    that are raised by the engine.
#    """
#
#    def __init__(self, value=None, results=None):
#        PandeiaException.__init__(self, value, results)
#        self.name = "Calculation Error"

# ### BACKGROUND ERRORS ### #

class BackgroundError(PandeiaException):

    """
    Raised when the Background Butler runs into errors.

    These errors could include:
        - invalid (position, date) combination
        - no stray light data available

    Usage:
        raise engine.custom_exceptions.BackgroundError('descriptive text')
    """

    def __init__(self, value='Background Error', debug=None):
        PandeiaException.__init__(self, value)
        self.name = value
        if debug:
            print('Background Error:')
            print(debug)


class StraylightPositionError(BackgroundError, UserInputError):

    """
    Raised when the specified position (ra, dec) is not observable on the
    specified date.

    Usage:
        raise engine.custom_exceptions.StraylightPositionError('descriptive text')
    """

    def __init__(self, value='User Input Related Background Error', debug=None):
        BackgroundError.__init__(self, value, debug)
        UserInputError.__init__(self, value)
        self.name = value


class StraylightDataError(BackgroundError):

    """
    Raised when needed stray light data is missing.

    Usage:
        raise engine.custom_exceptions.StraylightDataError('descriptive text')
    """

    def __init__(self, value='Background Error', debug=None):
        BackgroundError.__init__(self, value, debug)
        self.name = value


class DatelessBGError(BackgroundError):

    def __init__(self, value='Dateless Background Error', debug=None):
        BackgroundError.__init__(self, value, debug)
        self.name = value


class BMGError(BackgroundError):

    """
    Raised when the BMG returns an unhappy status code.

    Usage:
        raise engine.custom_exceptions.BMGError('status code')
    """

    def __init__(self, status, ra_dec_str, date_str):

        # these are the codes we can share with the user
        public_codes = {
            '500': 'BMG server error.',
            '501': 'Date (%s) out of range.' % date_str,
            '502': 'Ra/Dec (%s) out of range.' % ra_dec_str,
            '503': 'Wavelength out of range.'
        }

        # these are codes that we will log but won't share with the user
        private_codes = {
            '400': 'Empty bmg block (e.g. nothing after bmg keyword)',
            '401': 'No bmg block (e.g. no bmg keyword)',
            '402': 'Bad query block (e.g. badly formatted block)',
            '403': 'Bad query_type value (e.g. miss-spelled or un-supported)',
            '404': 'Empty query_type value (e.g. missing query_type value)',
            '405': 'No query_type keyword in query block (e.g. miss-spelled)',
            '504': 'Kernel list is inaccessible',
            '505': 'File wainscoat.txt is inaccessible',
            '506': 'Schlegel interstellar dust map fits file not found or inaccessible',
            '507': 'Schlegel interstellar dust map file name too long',
            '508': 'Error reading the std_spectrum_wavelengths.txt file',
            '509': 'Wavelength outside (0.1, 1200) micros for CIB',
            '510': 'Cib_spec_mode returns -1, wl outside (0.1, 1200)',
            '511': 'Error in opening file starcount.txt (when environment variable OUTPUT_STARCOUNT is set)'
        }

        if status in public_codes:
            # pass the error message to the user
            BackgroundError.__init__(self, public_codes[status])
        elif status in private_codes:
            # log the actual error, but just show the user something generic
            msg = 'The background model server encountered an unexpected error. TODO: insert generic error message text here.'
            BackgroundError.__init__(self, msg, private_codes[status])
        else:
            # Unexpected/unhandled error, but pass it on
            BackgroundError.__init__(self, "BG error with unknown status of: "+str(status))

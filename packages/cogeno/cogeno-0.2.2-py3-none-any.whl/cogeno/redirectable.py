# Copyright 2004-2016, Ned Batchelder.
# Copyright (c) 2018..2020 Bobby Noelte.
#
# SPDX-License-Identifier: MIT

import sys

class RedirectableMixin(object):
    __slots__ = []

    ##
    # @brief Redirect status and error reporting.
    #
    # Assign new files for standard out and/or standard error.
    #
    # @param stdout
    # @param stderr
    def set_standard_streams(self, stdout=None, stderr=None):
        if stdout:
            self._stdout = stdout
        if stderr:
            self._stderr = stderr


class Redirectable(RedirectableMixin):
    """ An object with its own stdout and stderr files.
    """
    def __init__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr

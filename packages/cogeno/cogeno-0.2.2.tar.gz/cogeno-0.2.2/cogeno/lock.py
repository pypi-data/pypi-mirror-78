# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from filelock import Timeout, FileLock
else:
    # use current package visibility
    from .filelock import Timeout, FileLock

class LockMixin(object):
    __slots__ = []

    ##
    # @brief Global cogeno lock
    _lock = None

    ##
    # @brief Lock file used for the current context.
    #
    # @return lock file name
    def lock_file(self):
        if self._context._lock_file is None:
            # No file for locking specified
            self.error("No path defined for lock file.", frame_index = 2)
        return self._context._lock_file

    ##
    # @brief Get the global cogeno lock
    #
    # @code
    # try:
    #      with cogeno.lock().acquire(timeout = 10):
    #          ...
    # except cogeno.lock_timeout():
    #     cogeno.error(...)
    # except:
    #     raise
    # @endcode
    #
    # @return Lock object
    def lock(self):
        if self._lock is None:
            self._lock = FileLock(self.lock_file())
        return self._lock

    ##
    # @brief Lock timeout
    #
    # @return Lock timeout object
    def lock_timeout(self):
        return Timeout


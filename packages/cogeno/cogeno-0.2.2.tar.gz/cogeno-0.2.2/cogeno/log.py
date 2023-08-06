# Copyright (c) 2018..2020 Bobby Noelte.
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

class LogMixin(object):
    __slots__ = []

    _log_file = None

    ##
    # @brief Print message and write to log file.
    #
    # @param message Message
    # @param message_type If given will be prepended to the message
    # @param end Character to put at the end of the message. '\\n' by default.
    # @param logonly Only write to logfile. True by default.
    def log(self, message, message_type=None, end="\n", logonly=True):
        if message_type is None:
            message_type = ''
            stdfile = self._stdout
        elif message_type == 'error':
            message_type = message_type+': '
            stdfile = self._stderr
        else:
            message_type = message_type+': '
            stdfile = self._stdout
        if not logonly:
            print(message_type+message, file=stdfile, end=end)
        if self._log_file is None:
            if self._context._log_file is None:
                # No file logging specified
                pass
            elif self._context._log_file == '-':
                # log to stdout
                pass
            else:
                log_file = Path(self._context._log_file)
                try:
                    with self.lock().acquire(timeout = 10):
                        if not log_file.is_file():
                            # log file will be created
                            # add preamble
                            preamble = "My preamble\n{}".format(message)
                            with log_file.open(mode = 'a', encoding = 'utf-8') as log_fd:
                                log_fd.write(preamble)
                    self._log_file = log_file
                except self.lock_timeout():
                    # Something went really wrong - we did not get the lock
                    self.error(
                        "Log file '{}' no access."
                        .format(log_file), frame_index = 2)
                except:
                    raise
        if not self._log_file is None:
            # Write message to log file
            try:
                with self.lock().acquire(timeout = 10):
                    with self._log_file.open(mode = 'a', encoding = 'utf-8') as log_fd:
                        for line in message.splitlines():
                            log_fd.write("{}{}{}".format(message_type, line, end))
                        log_fd.flush()
            except Timeout:
                # Something went really wrong - we did not get the lock
                self.error(
                    "Log file '{}' no access."
                    .format(log_file), frame_index = 2)
            except:
                raise

    ##
    # @brief Print message to stdout and log with a “message: ” prefix.
    #
    # @param message Message
    #
    # @see LogMixin::log()
    def msg(self, message):
        self.log(message, message_type='message', logonly=False)

    ##
    # @brief Print message to stdout and log with a "warning: ” prefix.
    #
    # @param message Message
    #
    # @see LogMixin::log()
    def warning(self, message):
        self.log(message, message_type='warning', logonly=False)

    ##
    # @brief Print message to stdout and log.
    #
    # @param message Message
    # @param end Character to put at the end of the message. '\\n' by default.
    #
    # @see LogMixin::log()
    def prout(self, message, end="\n"):
        self.log(message, message_type=None, end=end, logonly=False)

    ##
    # @brief Print message to stderr and log with a "error: ” prefix.
    #
    # @param message Message
    # @param end Character to put at the end of the message. '\\n' by default.
    #
    # @see LogMixin::log()
    def prerr(self, message, end="\n"):
        self.log(message, message_type='error', end=end, logonly=False)

# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from generator import CodeGenerator
    from redirectable import Redirectable
    from options import Options
    from context import Context
else:
    # use current package visibility
    from .generator import CodeGenerator
    from .redirectable import Redirectable
    from .options import Options
    from .context import Context


##
# @brief The code generation processor
class Cogeno(Redirectable):

    def __init__(self):
        Redirectable.__init__(self)

    ##
    # @brief Is this a trailing line after an end spec marker.
    #
    # @todo Make trailing end spec line detection dependent on
    #       type of text or file type.
    #
    # @param s line
    def _is_end_spec_trailer(self, s):
        return '*/' in s

    ##
    # @brief All of command-line cogeno, but in a callable form.
    #
    # This is used by main.
    #
    # @param argv equivalent of sys.argv.
    def callable_main(self, argv):
        if '--base' in argv:
            # maybe used to find the installation path of cogeno
            print(Path(__file__).resolve().parent.parent)
            return 0
        options = Options(argv)
        generator = CodeGenerator()
        generator.set_standard_streams(self._stdout, self._stderr)
        context = Context(generator, options = options)
        ret = generator._evaluate_context(context)
        return ret


def main():
    ret = Cogeno().callable_main(sys.argv)
    sys.exit(ret)


if __name__ == '__main__':
    main()

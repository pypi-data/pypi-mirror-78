# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import io

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from error import Error
    from context import Context
else:
    # use current package visibility
    from .error import Error
    from .context import Context

class IncludeMixin(object):
    __slots__ = []

    ##
    # @brief Write the text from include_file to the output.
    #
    # The ``include_file`` is processed by cogeno. Inline code generation in
    # ``include_file`` can access the globals defined in the
    # ``including source file`` before inclusion. The ``including source file``
    # can access the globals defined in the ``include_file`` (after inclusion).
    #
    # @param include_file Path of include file, either absolute path or relative
    #                     to current directory or relative to templates directory
    #                     (e.g. 'templates/drivers/simple_tmpl.c')
    def out_include(self, include_file):
        self.log('s{}: out_include {}'
                 .format(len(self.cogeno_module_states), include_file))
        # collect pathes to search (script directory, template directories)
        paths = []
        paths.append(self.template_path())
        paths.extend(self.templates_paths())
        # find the include file
        input_file = self.find_file_path(include_file, paths)
        if input_file is None:
            raise self._get_error_exception(
                "Include file '{}' does not exist or is no file.\n".
                format(include_file) + "Searched in {}".format(paths), 1)
        if str(input_file) in self._context._globals['_guard_include']:
            self.log('------- include guarded {} - multiple inclusion of include file.'.
                     format(str(input_file)))
            return ''
        else:
            include_context = Context(self,
                parent_context = self.context(),
                template_file = str(input_file),
                template_source_type = 'file',
                delete_code = True,
                )
            # delete inline code in included files
            self.log('------- include start {}'.format(input_file))
            # let the devils work - evaluate context
            # inserts the context output into the current context
            self._evaluate_context(include_context)
            self.log('------- include   end {}'.format(input_file))
            return include_context._outstring

    ##
    # @brief Prevent the current file to be included by ``cogeno.out_include()``
    #        when called the next time.
    def guard_include(self):
        if self._context._template_file in self._context._globals['_guard_include']:
            # This should never happen
            raise self._get_error_exception(
                "Multiple inclusion of guarded include file '{}'.".
                format(self._context._template_file), 1)
        self.log('------- include guard {}'.format(self._context._template_file))
        self._context._globals['_guard_include'].append(self._context._template_file)


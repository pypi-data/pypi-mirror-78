# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

import sys
import re
import hashlib
import string

class OutputMixin(object):
    __slots__ = []

    class OutputFilter():
        ##
        # @brief Apply filter
        #
        # @param line line to apply filter to
        # @param lineno line number - starts at 1
        # @param lines all lines
        # @return line with filter applied. Maybe None in case the line is deleted
        def __call__(self, line, lineno=None, lines=None):
            return line

        ##
        # @brief Parse a line number spec.
        #
        # @param spec Line number spec (such as "1,2,4-6")
        # @param total Total number of lines
        # @return A list of  wanted line numbers (line numbers start at 1).
        def parselinenos(self, spec, total):
            # Adapted from
            # https://github.com/sphinx-doc/sphinx/blob/3.x/sphinx/directives/code.py
            linenos = list()
            parts = spec.split(',')
            for part in parts:
                try:
                    begend = part.strip().split('-')
                    if ['', ''] == begend:
                        raise ValueError
                    elif len(begend) == 1:
                        linenos.append(int(begend[0]))
                    elif len(begend) == 2:
                        start = int(begend[0] or 1)  # left half open (cf. -10)
                        end = int(begend[1] or max(start, total))  # right half open (cf. 10-)
                        if start > end:  # invalid range (cf. 10-1)
                            raise ValueError
                        linenos.extend(range(start, end + 1))
                    else:
                        raise ValueError
                except Exception:
                    raise ValueError('invalid line number spec: %r' % spec)

            return linenos

    ##
    # @brief Remove initial and trailing blank lines from the block of lines.
    class OutputFilterTrimBlankLines(OutputFilter):
        def __init__(self):
            self.trim_inital_lines = True
            self.trim_trailing_lines_start = None

        ##
        # @brief Apply filter
        #
        # @param line line to apply filter to
        # @param lineno line number - starts at 1
        # @param lines all lines
        # return line with filter applied. Maybe None in case the line is deleted
        def __call__(self, line, lineno=None, lines=None):
            if self.trim_inital_lines:
                if line.strip() == '':
                    return None
                self.trim_inital_lines = False
            if line.strip() == '':
                self.trim_trailing_lines_start = lineno - 1
            if lineno >= len(lines) and self.trim_trailing_lines_start:
                # We are at the last line
                for i, line in enumerate(lines):
                    if line is None or i < self.trim_trailing_lines_start:
                        continue
                    lines[i] = None
            return line

    ##
    # @brief Remove common initial white space from the lines.
    #
    # @param new_indent Optional new indentation (after dedent)
    class OutputFilterDedent(OutputFilter):
        def __init__(self, new_indent=''):
            self.white_prefix = None
            self.new_indent = new_indent

        ##
        # @brief Apply filter
        #
        # @param line line to apply filter to
        # @param lineno line number - starts at 1
        # @param lines all lines
        # @return line with filter applied. Maybe None in case the line is deleted
        def __call__(self, line, lineno=None, lines=None):
            if line.strip() != '':
                # Non whitespace line
                # Find initial whitespace chunk in line.
                pat = r'\s*'
                prefix = re.match(pat, line).group(0)
                if self.white_prefix is None:
                    self.white_prefix = prefix
                else:
                    for i in range(len(self.white_prefix)):
                        if i >= len(prefix) \
                           or self.white_prefix[i] != prefix[i]:
                            self.white_prefix = self.white_prefix[:i]
                            break
            else:
                # whitespace line
                line = line.strip()
            if lineno >= len(lines):
                # We are at the last line
                for i, line in enumerate(lines):
                    if line is None:
                        continue
                    if self.white_prefix:
                        line = line.replace(self.white_prefix, '', 1)
                    if line.strip() != '' and self.new_indent:
                        line = self.new_indent + line
                    lines[i] = line
            return line

    ##
    # @brief Filter lines by line numbers.
    #
    # Filter lines that are given by line sumber specifications
    # (such as "1,2,4-6").
    #
    # @param args list of arguments denoting line number specifications
    class OutputFilterLineNumbers(OutputFilter):
        def __init__(self, *args):
            self.args = args
            self.line_numbers = None

        ##
        # @brief Apply filter
        #
        # @param line line to apply filter to
        # @param lineno line number - starts at 1
        # @param lines all lines
        # @return line with filter applied. Maybe None in case the line is deleted
        def __call__(self, line, lineno=None, lines=None):
            if self.line_numbers is None:
                self.line_numbers = []
                for spec in self.args:
                    if isinstance(spec, str):
                        linenos = self.parselinenos(spec, len(lines))
                        self.line_numbers.extend(linenos)
                    else:
                        self.line_numbers.append(int(spec))

            if not lineno in self.line_numbers:
                return None

            return line

    ##
    # @brief Start output at pattern.
    #
    # @param start_at Start pattern
    class OutputFilterStartAt(OutputFilter):
        def __init__(self, start_at):
            self.start_at = start_at
            self.started = False

        def __call__(self, line, lineno=None, lines=None):
            if self.start_at in line:
                self.started = True
            if not self.started:
                return None
            return line

    ##
    # @brief Stop output at pattern.
    #
    # @param stop_at Stop pattern
    class OutputFilterStopAt(OutputFilter):
        def __init__(self, stop_at):
            self.stop_at = stop_at
            self.stopped = False

        def __call__(self, line, lineno=None, lines=None):
            if self.stopped:
                return None
            if self.stop_at in line:
                self.stopped = True
            return line

    ##
    # @brief Replace substring.
    #
    # @param old old substring to replace
    # @param new new substring which will replace the old substring.
    #            if new is None and the resulting line is empty it
    #            is deleted.
    # @param count (optional) the number of times to replace the old
    #              substring with the new substring
    class OutputFilterReplace(OutputFilter):
        def __init__(self, old, new, count = None):
            self.old = old
            self.new = new
            self.count = count

        def __call__(self, line, lineno=None, lines=None):
            if self.new is None:
                new = ""
            else:
                new = self.new
            if self.count:
                new_line = line.replace(self.old, new, self.count)
            else:
                new_line = line.replace(self.old, new)
            if len(new_line) == 0 and self.new is None:
                return None
            else:
                return new_line

    ##
    # @brief Substitude regular expression pattern.
    #
    # Replace the leftmost non-overlapping occurrences of pattern in each line
    # by the replacement repl.
    #
    # @param pattern Pattern for replacement. Pattern is a string that will be
    #                compiled to a pattern object.
    # @param repl Replacement. Repl can be a string or a function. If repl is a
    #             function, it is called for every non-overlapping occurrence of
    #             pattern.
    # @param count (optional) maximum number of pattern occurrences to be replaced
    class OutputFilterReSub(OutputFilter):
        def __init__(self, pattern, repl, count = 0, flags = 0):
            self.pattern = re.compile(pattern)
            self.repl = repl
            self.count = count
            self.flags = flags

        def __call__(self, line, lineno=None, lines=None):
            return re.sub(self.pattern, line, self.count, self.flags)

    ##
    # @brief Substitude template placeholders.
    #
    # Template placeholder substitution supports $-based substitutions,
    # using the following rules:
    # - $$ is an escape; it is replaced with a single $.
    # - $identifier names a substitution placeholder matching a mapping key of "identifier".
    #   By default, "identifier" is restricted to any case-insensitive ASCII alphanumeric string
    #   (including underscores) that starts with an underscore or ASCII letter.
    #   The first non-identifier character after the $ character terminates this placeholder specification.
    # - ${identifier} is equivalent to $identifier. It is required when valid identifier characters
    #   follow the placeholder but are not part of the placeholder, such as "${noun}ification".
    #
    # At least up to 4 nesting levels of placeholders are substituded, e.g.:
    # - ${placeholder_level1}                : mapping = 'placeholder_level1' : 'holder'
    # - ${place${placeholder_level1}_level2} : mapping = 'placeholder_level2' : 'placeholder'
    # - ${${placeholder_level2}_level3}      : mapping = 'placeholder_level3' : 'placeholder_level'
    # - ${${placeholder_level3}4}            : mapping = 'placeholder_level4' : 'success'
    #
    # If more than one placeholder patterns are provided the substitution is done for each pattern
    # sequencing through the patterns list.
    #
    # @param mapping Mapping is any dictionary-like object with keys that match the
    #                template placeholders.
    # @param patterns (optional) Patterns is a list of regular expressions describing
    #                 the pattern for non-braced placeholders.
    class OutputFilterTemplateSubstitude(OutputFilter):
        templates_classes = {}

        def __init__(self, mapping, patterns = [r'[_a-zA-Z][_a-zA-Z0-9]*']):
            self.mapping = mapping
            self.templates = []
            for pattern in patterns:
                template_class_name = f'OutputFilterTemplate{hashlib.md5(pattern).hexdigest()}'
                if template_class_name in OutputFilterTemplateSubstitude.templates_classes:
                    template_class = OutputFilterTemplateSubstitude.templates_classes[template_class_name]
                else:
                    # Create new template class with pattern
                    template_class = type(template_class_name, string.Template, { 'idpattern' : pattern, })
                    # Remember template class for multiple use
                    OutputFilterTemplateSubstitude.templates_classes[template_class_name] = template_class
                # Add templates class to template classes to be applied
                if len(patterns) == 1:
                    # Apply at least for 4 times
                    self.templates.extend([template_class, template_class, template_class, template_class])
                else:
                    self.templates.append(template_class)

        def __call__(self, line, lineno=None, lines=None):
            substituded = line
            for template in self.templates:
                substituded = template(substituded).safe_substitude(self.mapping)
            return substituded

    ##
    # @brief Write text to the output.
    #
    # The string arguments are concenated. The filters are then applied to the
    # lines of the concenated string. The resulting string is written to the output.
    #
    # list, set and frozenset type arguments are unrolled before concenation.
    #
    # The output filters ``OutputFilterDedent`` and ``OutputFilterTrimBlankLines``
    # make it easier to use multi-line strings, and they are only are useful for multi-line strings:
    #
    # @code
    # cogeno.out("""
    #    These are lines I
    #    want to write into my source file.
    # """, cogeno.OutputFilterDedent(), cogeno.OutputFilterTrimBlankLines())
    # @endcode
    #
    # @param *args Variable length argument list of strings and output
    #              filters.
    # @return output string
    def _out(self, *args):
        output = ''
        filters = []
        for arg in args:
            if isinstance(arg, list) or isinstance(arg, set) or isinstance(arg, frozenset):
                for elem in arg:
                    if isinstance(elem, str):
                        output = output + elem
                    elif isinstance(arg, OutputMixin.OutputFilter):
                        filters.append(elem)
                    else:
                        self.error(f"Unknown element '{elem}' in argument '{arg}' for out function.", 3)
            elif isinstance(arg, str):
                output = output + arg
            elif isinstance(arg, OutputMixin.OutputFilter):
                filters.append(arg)
            else:
                self.error(f"Unknown argument '{arg}' in {args} for out function.", 3)
        if filters:
            lines = output.split('\n')
            for filt in filters:
                for i, line in enumerate(lines):
                    if line:
                        lines[i] = filt(line, i + 1, lines)
            output = ''
            for line in lines:
                if line:
                    output += line + '\n'

        if self._context.script_is_python():
            self.context_out(output)

        return output

    ##
    # @brief Write text to the output.
    #
    # The string arguments are concenated. The filters are then applied to the
    # lines of the concenated string. The resulting string is written to the output.
    #
    # ``OutputFilterDedent`` and ``OutputFilterTrimBlankLines`` make it easier to use
    # multi-line strings, and they are only are useful for multi-line strings:
    #
    # @code
    # cogeno.out("""
    #    These are lines I
    #    want to write into my source file.
    # """, cogeno.OutputFilterDedent(), cogeno.OutputFilterTrimBlankLines())
    # @endcode
    #
    # @param *args Variable length argument list of strings and output
    #              filters.
    # @return output string
    def out(self, *args):
        return self._out(*args)

    ##
    # @brief Write text to the output with newline appended.
    #
    # @see OutputMixin::out(self, *args)
    #
    # @param *args Variable length argument list of strings and output
    #              filters.
    # @return output string
    def outl(self, *args):
        self._out(*args)
        self._out('\n')

    ##
    # @brief Insert the text from the file into the output
    #
    # @see OutputMixin::out(self, *args)
    #
    # @param insert_file Path of file, either absolute path or relative
    #                    to current directory or relative to templates directory.
    # @param *args Variable length argument list of strings and output
    #              filters.
    # @return output string
    def out_insert(self, insert_file, *args):
        self.log('s{}: insert_file {}'
                 .format(len(self.cogeno_module_states), insert_file))
        # collect pathes to search (script directory, template directories)
        paths = []
        paths.append(self.template_path())
        paths.extend(self.templates_paths())
        paths.extend(self.modules_paths())
        # find the insert file
        path = self.find_file_path(insert_file, paths)
        if path is None:
            raise self._get_error_exception(
                "Insert file '{}' does not exist or is no file.\n".
                format(insert_file) + "Searched in {}".format(paths), 1)

        with path.open(mode = "r", encoding="utf-8") as fd:
            content = fd.read()

        return self._out(content, *args)

# Copyright (C) 2020, Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import cogeno

##
# @brief Section mark hirarchy for section depth.
RST_SECTION_MARKS = '#*=-'

##
# @brief Sanitize target string.
#
# Replace weired characters in the target string.
# Prevent `_` at start and end of target string.
#
# @return Sanitized target string.
def sanitize_target(target):
    target = target.strip() \
        .replace(" ", "_") \
        .replace("-", "_") \
        .replace(",", "_") \
        .replace("@", "_") \
        .replace("/", "_") \
        .replace(".", "_") \
        .replace("+", "_") \
        .strip('_')
    return target


##
# @brief Get target reference.
#
# Get the target reference for target string.
# The target string is sanitized by
# sanitize_target() before.
# 
# @return Target reference.
def link_reference(target):
    target = sanitize_target(target)
    return f':ref:`{target}`'


##
# @brief A node of a RST document
class Node(object):
    def __init__(self, text_begin = None, text_end = None):
        self.children = []
        self._text_begin = text_begin
        self._text_end = text_end

    ##
    # @brief Get the text to be issued at beginning of node output.
    #
    # Maybe overloaded by child classes to dynamically adapt the 
    # output text at out() processing.
    #
    # @return text
    def text_begin(self):
        return self._text_begin

    ##
    # @brief Get the text to be issued at end of node output.
    #
    # Maybe overloaded by child classes to dynamically adapt the 
    # output text at out() processing.
    #
    # @return text
    def text_end(self):
        return self._text_end

    ##
    # @brief Add a ``Node`` object to the current node.
    #
    # @param node Node to add as a child of this node.
    # @return ``True`` in case of success.
    def add_child(self, node):
        self.children.append(node)
        return True

    ##
    # @brief Output node content
    #
    # @param output_redirect Optional - redirect output, default is cogeno.out.
    def out(self, out_redirect = None):
        if out_redirect is None:
            out_redirect = cogeno.out
        if not self.text_begin() is None:
            out_redirect(self.text_begin())
        for child in self.children:
            child.out(out_redirect = out_redirect)
        if not self.text_end() is None:
            out_redirect(self.text_end())


##
# @brief A pure text node.
class Text(Node):
    ##
    # @brief Initialise the text node.
    #
    # @param text Multiline text
    def __init__(self, text):
        Node.__init__(self, text_begin = text)


##
# @brief A comment node.
class Comment(Node):
    ##
    # @brief Initialise the comment node.
    #
    # @param text Multiline text
    def __init__(self, text):
        comment = '..\n'
        for line in text.splitlines():
            line = line.strip()
            comment += f'    {line}\n'
        Node.__init__(self, text_begin = comment, text_end = '\n')


##
# @brief A code block node.
class CodeBlock(Node):
    ##
    # @brief Initialise the code block node.
    #
    # @param code Multiline code
    # @param code_type The type of code as understood by the code-block directive
    def __init__(self, code, code_type = 'none'):
        code_block = f'.. code-block:: {code_type}\n\n'
        for line in code.splitlines():
            line = line.expandtabs(8)
            code_block += f'    {line}\n'
        code_block += '\n'
        Node.__init__(self, text_begin = code_block)


##
# @brief A paragraph node.
class Paragraph(Node):
    ##
    # @brief Initialise the paragraph node.
    #
    # @param text Multiline text
    def __init__(self, text):
        Node.__init__(self)
        self.add_child(Text(text.strip() + '\n\n'))


##
# @brief A section node.
class Section(Node):
    ##
    # @brief Initialise the section node.
    #
    # @param title Title of the section
    # @param depth Either depth of the section, default is 1,
    #              or section mark character (e.g. '#').
    def __init__(self, title, depth=1):
        header = title.strip()
        if isinstance(depth, int):
            section_mark = RST_SECTION_MARKS[depth - 1]
        else:
            section_mark = depth
        section = header + '\n' + section_mark * len(header) + '\n\n'
        Node.__init__(self, text_begin = section)


##
# @brief A bullet list node.
class BulletList(Node):
    ##
    # @brief Initialise the bullet list node.
    def __init__(self):
        Node.__init__(self, text_end = '\n')

    ##
    # @brief Add new text block to the bullet list.
    #
    # @param text Multiline text
    def add_item(self, text):
        self.add_child(Text('    * ' + text.strip() + '\n'))


##
# @brief A ordered list node.
class OrderedList(Node):
    ##
    # @brief Initialise the ordered list node.
    def __init__(self):
        Node.__init__(self, text_end = '\n')
        self._index = 1

    ##
    # @brief Add new text block to the ordered list.
    #
    # @param text Multiline text
    def add_item(self, text):
        self.add_child(Text(f'    {self._index}. ' + text.strip() + '\n'))
        self._index += 1


##
# @brief A table node.
#
# Output will be done in csv-table style.
class Table(Node):
    ##
    # @brief Initialise the paragraph node.
    #
    # @param title the table title
    # @param headers list of header items in the table
    # @param widths list of column widths in the table
    def __init__(self, title='', headers=[], widths=[]):
        table_header = f'.. list-table:: {title}\n'
        if len(widths) > 0:
            table_header += '    :widths:'
            for width in widths:
                table_header += f' {width}'
            table_header += '\n'
        if len(headers) > 0:
            header_count = len(headers)
            table_header += '    :headers: {header_count}\n'
        table_header += '\n'
        for i, header in enumerate(headers):
            if i == 0:
                table_header += f'    * - {header}\n'
            else:
                table_header += f'      - {header}\n'
        Node.__init__(self, text_begin = table_header, text_end = '\n')

    ##
    # @brief Add new row to the table.
    #
    # @param row List of column items in the row.
    def add_row(self, row):
        text = ''
        for i, column in enumerate(row):
            if i == 0:
                text += f'    * - {column}\n'
            else:
                text += f'      - {column}\n'
        self.add_child(Text(text))


##
# @brief A link target node.
class LinkTarget(Node):
    ##
    # @brief Initialise the link target node.
    #
    # The target string will be santized 
    # using sanitize_target().
    #
    # @param target Target
    def __init__(self, target):
        target = sanitize_target(target)
        Node.__init__(self, text_begin = f'.. _{target}:\n\n')


##
# @brief A document node.
class Document(Node):
    ##
    # @brief Initialise the document node.
    #
    # @param file_path Optional, file to write the document to
    def __init__(self, file_path = None):
        Node.__init__(self)
        self._file_path = file_path
        self._file_fd = None

    def _out_file(self, text):
        self._file_fd.write(text)

    ##
    # @brief Output document content
    # 
    # If no out_redirect is provided the content is written to
    # the file_path specified on initialisation.
    # If also the file_path is not specified the output is re-directed
    # to cogeno.out().
    #
    # @param output_redirect Optional - redirect output, default is file_path.    
    def out(self, out_redirect = None):
        if self._file_path is None and out_redirect is None:
            # Output to cogeno.out
            Node.out(self)
        elif not out_redirect is None:
            # Output to specified out_direct
            Node.out(self, out_redirect = out_redirect)
        else:
            # Output document to file
            out_redirect = self._out_file
            rst_file = Path(self._file_path)
            with rst_file.open('w') as rst_file_fd:
                self._file_fd = rst_file_fd
                Node.out(self, out_redirect = out_redirect)

# Copyright (c) 2018 Open Source Foundries Limited
# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0
#
# CMakeCacheEntry and CMakeCache are taken from scripts/zephyr_run.py.


import os
import sys
import re
from collections import OrderedDict
from pathlib import Path

import cogeno


class CMakeCacheEntry:
    '''Represents a CMake cache entry.
    This class understands the type system in a CMakeCache.txt, and
    converts the following cache types to Python types:
    Cache Type    Python type
    ----------    -------------------------------------------
    FILEPATH      str
    PATH          str
    STRING        str OR list of str (if ';' is in the value)
    BOOL          bool
    INTERNAL      str OR list of str (if ';' is in the value)
    ----------    -------------------------------------------
    '''

    # Regular expression for a cache entry.
    #
    # CMake variable names can include escape characters, allowing a
    # wider set of names than is easy to match with a regular
    # expression. To be permissive here, use a non-greedy match up to
    # the first colon (':'). This breaks if the variable name has a
    # colon inside, but it's good enough.
    CACHE_ENTRY = re.compile(
        r'''(?P<name>.*?)                               # name
         :(?P<type>FILEPATH|PATH|STRING|BOOL|INTERNAL)  # type
         =(?P<value>.*)                                 # value
        ''', re.X)

    @classmethod
    def _to_bool(cls, val):
        # Convert a CMake BOOL string into a Python bool.
        #
        #   "True if the constant is 1, ON, YES, TRUE, Y, or a
        #   non-zero number. False if the constant is 0, OFF, NO,
        #   FALSE, N, IGNORE, NOTFOUND, the empty string, or ends in
        #   the suffix -NOTFOUND. Named boolean constants are
        #   case-insensitive. If the argument is not one of these
        #   constants, it is treated as a variable."
        #
        # https://cmake.org/cmake/help/v3.0/command/if.html
        val = val.upper()
        if val in ('ON', 'YES', 'TRUE', 'Y'):
            return True
        elif val in ('OFF', 'NO', 'FALSE', 'N', 'IGNORE', 'NOTFOUND', ''):
            return False
        elif val.endswith('-NOTFOUND'):
            return False
        else:
            try:
                v = int(val)
                return v != 0
            except ValueError as exc:
                raise ValueError('invalid bool {}'.format(val)) from exc

    @classmethod
    def from_line(cls, line, line_no):
        # Comments can only occur at the beginning of a line.
        # (The value of an entry could contain a comment character).
        if line.startswith('//') or line.startswith('#'):
            return None

        # Whitespace-only lines do not contain cache entries.
        if not line.strip():
            return None

        m = cls.CACHE_ENTRY.match(line)
        if not m:
            return None

        name, type_, value = (m.group(g) for g in ('name', 'type', 'value'))
        if type_ == 'BOOL':
            try:
                value = cls._to_bool(value)
            except ValueError as exc:
                args = exc.args + ('on line {}: {}'.format(line_no, line),)
                raise ValueError(args) from exc
        elif type_ == 'STRING' or type_ == 'INTERNAL':
            # If the value is a CMake list (i.e. is a string which
            # contains a ';'), convert to a Python list.
            if ';' in value:
                value = value.split(';')

        return CMakeCacheEntry(name, value)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        fmt = 'CMakeCacheEntry(name={}, value={})'
        return fmt.format(self.name, self.value)


class CMakeCache:
    '''Parses and represents a CMake cache file.'''

    def __init__(self, cache_file):
        self.load(cache_file)

    def load(self, cache_file):
        entries = []
        with open(str(cache_file), 'r') as cache:
            for line_no, line in enumerate(cache):
                entry = CMakeCacheEntry.from_line(line, line_no)
                if entry:
                    entries.append(entry)
        self._entries = OrderedDict((e.name, e) for e in entries)

    def get(self, name, default=None):
        entry = self._entries.get(name)
        if entry is not None:
            return entry.value
        else:
            return default

    def get_list(self, name, default=None):
        if default is None:
            default = []
        entry = self._entries.get(name)
        if entry is not None:
            value = entry.value
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                return [value]
            else:
                msg = 'invalid value {} type {}'
                raise RuntimeError(msg.format(value, type(value)))
        else:
            return default

    def __getitem__(self, name):
        return self._entries[name].value

    def __setitem__(self, name, entry):
        if not isinstance(entry, CMakeCacheEntry):
            msg = 'improper type {} for value {}, expecting CMakeCacheEntry'
            raise TypeError(msg.format(type(entry), entry))
        self._entries[name] = entry

    def __delitem__(self, name):
        del self._entries[name]

    def __iter__(self):
        return iter(self._entries.values())


class CMakeDB(object):

    def _extract(self, cache_file):
        cache_file = Path(cache_file)
        if not cache_file.is_file():
            raise RuntimeError(
                "CMake cache file '{}' does not exist or is no file.".
                format(cache_file))
        return CMakeCache(cache_file)

    def __init__(self, cache_file, *args, **kw):
        self._variables = dict(*args, **kw)
        self._cmake_cache = self._extract(cache_file)

    def variable(self, variable_name, default="<unset>"):
        variable_value = self._variables.get(variable_name, default)
        if variable_value == "<unset>":
            raise RuntimeError(
                "CMake variable '{}' not defined.".format(variable_name))
        return variable_value

    def cache_variable(self, variable_name, default="<unset>"):
        try:
            return self._cmake_cache.get(variable_name)
        except:
            if default == "<unset>":
                raise RuntimeError(
                    "CMake variable '{}' not defined in cache file.".
                    format(variable_name))
            return default


##
# @brief Get CMake variable database prepared for cogeno use.
# @return CMake variable database.
def cmake(force_extract = False):
    if not hasattr(cogeno, '_cmakedb'):
        # Make the CMake database a hidden attribute of the generator
        cogeno._cmakedb = None

        cogeno.options_add_argument('--cmake:cache', metavar='FILE',
            dest='cmakecache_file', action='store',
            type=lambda x: cogeno.option_is_valid_file(x),
            help='Use CMake variables from CMake cache FILE.')
        cogeno.options_add_argument('--cmake:define', nargs='+', metavar='DEFINE',
            dest='cmakedefines', action='append',
            help='Define CMake variables to your generator code.')

    if getattr(cogeno, '_cmakedb') is not None and force_extract is False:
        return cogeno._cmakedb

    # CMake cache file
    if cogeno.option('cmakecache_file'):
        cmakecache_file = cogeno.option('cmakecache_file')
    else:
        cogeno.error("No path defined for the cmake cache file.", 2)
    # --defines
    cmakedefines = {}
    if cogeno.option('cmakedefines') is not None:
        for define in cogeno.option('cmakedefines'):
            d = define[0].split('=')
            if len(d) > 1:
                value = d[1]
            else:
                value = None
            cmakedefines[d[0]] = value

    cogeno._cmakedb = CMakeDB(cogeno.option('cmakecache_file'), cmakedefines)

    return cogeno._cmakedb


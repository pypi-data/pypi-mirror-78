#!/usr/bin/env python3
#
# Copyright (c) 2018 Linaro Limited
# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import time
import argparse
import subprocess
import traceback
from pathlib import Path
from pprint import pprint

import pcpp
import cogeno

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from edtsdb.database import EDTSDb
else:
    # use current package visibility
    from .edtsdb.database import EDTSDb

##
# @brief C/C++ style preprocessor for DTS files
class EDTSPreprocessor(pcpp.Preprocessor):

    def __init__(self):
        super(EDTSPreprocessor, self).__init__()
        self.dependencies = []

    # Preprocessor customizing
    # ------------------------

    def include(self, tokens):
        if not tokens:
            return
        filename = ""
        if tokens[0].value != '<' and tokens[0].type != self.t_STRING:
            include_tokens = self.tokenstrip(self.expand_macros(tokens))
        else:
            include_tokens = tokens
        for token in include_tokens:
            filename += token.value
        # include <...>
        include_dirs = [Path(path) for path in self.path]
        # include "..."
        if include_tokens[0].type == self.t_STRING:
            include_dirs.extend([Path(path) for path in self.temp_path])
        # search the file
        include_file = cogeno.find_file_path(filename.strip('<">'), include_dirs)
        if include_file is None:
            cogeno.warning(f'edts.py: Error {filename} not found but included in DTS source file {tokens[0].source}:{tokens[0].lineno} - ignored')
        else:
            self.dependencies.append(include_file)
        return super(EDTSPreprocessor, self).include(tokens)

    # Preprocessor hooks
    # ------------------

    def on_comment(self, tok):
        # Remove comments
        return False

    def on_directive_handle(self,directive,toks,ifpassthru,precedingtoks):
        # Execute and remove from the output
        return True

    def on_directive_unknown(self,directive,toks,ifpassthru,precedingtoks):
        directive_text = ''.join(tok.value for tok in toks)
        if len(toks) >= 2 and toks[0].value == '-' and toks[1].value == 'cells':
            # #xxx-cells directive
            # pass through
            return None
        if len(toks) >= 4 and toks[0].value == '-'  and toks[2].value == '-' and toks[3].value == 'cells':
            # #xxx-xxx-cells directive
            # pass through
            return None
        if directive.value == 'error':
            cogeno.warning(f'edts.py: Error #{directive.value} {directive_text} in DTS source file {directive.source}:{directive.lineno} - ignored')
            #self.return_code += 1
        elif directive.value == 'warning':
            cogeno.warning(f'edts.py: Warning #{directive.value} {directive_text} in DTS source file {directive.source}:{directive.lineno} - ignored')
        else:
            cogeno.warning(f'edts.py: Unknown directive #{directive.value} {directive_text} in DTS source file {directive.source}:{directive.lineno} - ignored')
        # remove from output
        return True

    def on_error(self, file, line, msg):
        #self.return_code += 1
        cogeno.error(msg, 3)

    def preprocess(self):
        # --edts:dts-pp-sources
        edts_dts_pp_sources = []
        if cogeno.option('edts_dts_pp_sources'):
            paths = cogeno.option('edts_dts_pp_sources')
            if not isinstance(paths, list):
                paths = [paths]
            if isinstance(paths[0], list):
                paths = [item for sublist in paths for item in sublist]
            for path in paths:
                try:
                    path = Path(path).resolve()
                except FileNotFoundError:
                    # Python 3.4/3.5 will throw this exception
                    # Python >= 3.6 will not throw this exception
                    path = Path(path)
                if path.is_file():
                    edts_dts_pp_sources.append(path)
                else:
                    cogeno.warning(f'edts.py: Unknown DTS source file {path} - ignored')
            # remove duplicates
            edts_dts_pp_sources = list(set(edts_dts_pp_sources))

        # --edts:dts-pp-include-dirs
        edts_dts_pp_include_dirs = []
        if cogeno.option('edts_dts_pp_include_dirs'):
            paths = cogeno.option('edts_dts_pp_include_dirs')
            if not isinstance(paths, list):
                paths = [paths]
            if isinstance(paths[0], list):
                paths = [item for sublist in paths for item in sublist]
            for path in paths:
                try:
                    path = Path(path).resolve()
                except FileNotFoundError:
                    # Python 3.4/3.5 will throw this exception
                    # Python >= 3.6 will not throw this exception
                    path = Path(path)
                if path.is_dir():
                    edts_dts_pp_include_dirs.append(path)
                else:
                    cogeno.warning(f'edts.py: Unknown DTS include directory {path} - ignored')
            # remove duplicates
            edts_dts_pp_include_dirs = list(set(edts_dts_pp_include_dirs))

        # --edts:dts-pp-defines
        edts_dts_pp_defines = ['COGENO_EDTS 1']
        if cogeno.option('edts_dts_pp_defines'):
            defines = cogeno.option('edts_dts_pp_defines')
            if not isinstance(defines, list):
                defines = [defines]
            if isinstance(defines[0], list):
                defines = [item for sublist in defines for item in sublist]
            for define in defines:
                if not '=' in define:
                    define += '=1'
                edts_dts_pp_defines.append(define.replace("=", " "))

        # --edts:dts
        edts_dts = None
        if cogeno.option('edts_dts'):
            path = cogeno.option('edts_dts')
            try:
                path = Path(path).resolve()
            except FileNotFoundError:
                # Python 3.4/3.5 will throw this exception
                # Python >= 3.6 will not throw this exception
                path = Path(path)
            edts_dts = path
        else:
            cogeno.error("No path defined for the device tree specification file.", 3)

        try:
            # The file to write the DTS to
            edts_dts_file = edts_dts.open(mode="w", encoding="utf-8")

            # Parse all the source files
            for pp_include_dir in edts_dts_pp_include_dirs:
                self.add_path(str(pp_include_dir))
            for pp_define in edts_dts_pp_defines:
                self.define(pp_define)
            edts_dts_source = ''
            for pp_source in edts_dts_pp_sources:
                edts_dts_source += '#include "' + str(pp_source) + '"\n'
            self.parse(edts_dts_source)

            # Write output to file
            self.compress = 2
            self.line_directive = None
            self.write(edts_dts_file)
            # Assure file is synced to disk
            # - Important as the file is read right after to extract the database.
            #   Without sync the file may just be empty on this first read.
            edts_dts_file.flush()
            os.fsync(edts_dts_file.fileno())
        except:
            msg = traceback.print_exc(10)
            msg += "\nINTERNAL PREPROCESSOR ERROR AT AROUND %s:%d, FATALLY EXITING NOW\n" \
                    % (self.lastdirective.source, self.lastdirective.lineno)
            cogeno.error(msg, 3)
        finally:
            edts_dts_file.close()

##
# @brief Get EDTS database prepared for cogeno use.
# @return Extended device tree database.
def edts(force_extract = False):
    if not hasattr(cogeno, '_edtsdb'):
        # Make the EDTS database a hidden attribute of the generator
        cogeno._edtsdb = None

        cogeno.options_add_argument('--edts:db', metavar='FILE',
            dest='edts_db', action='store',
            help='Write or read EDTS database to/ from FILE.')
        cogeno.options_add_argument('--edts:bindings-dirs', nargs='+', metavar='DIR',
            dest='edts_bindings_dirs', action='append',
            type=lambda x: cogeno.option_is_valid_directory(x),
            help='Use bindings from bindings DIR for device tree extraction.' +
                 ' We allow multiple')
        cogeno.options_add_argument('--edts:bindings-exclude', nargs='+', metavar='FILE',
            dest='edts_bindings_exclude', action='append',
            help='Exclude bindings DIR or FILE from usage for device tree extraction.' +
                 ' We allow multiple.')
        cogeno.options_add_argument('--edts:bindings-no-default',
            dest='edts_bindings_no_default', action='store',
            help='Do not add EDTS database\'s generic bindings to bindings by default.')
        cogeno.options_add_argument('--edts:dts', metavar='FILE',
            dest='edts_dts', action='store',
            help='Write (see dts-pp) or read device tree specification to/ from this FILE.')
        cogeno.options_add_argument('--edts:dts-pp-defines', nargs='+', metavar='DEFINE',
            dest='edts_dts_pp_defines', action='append',
            help='Define variable to pre-processor. We allow multiple')
        cogeno.options_add_argument('--edts:dts-pp-include-dirs', nargs='+', metavar='DIR',
            dest='edts_dts_pp_include_dirs', action='append',
            type=lambda x: cogeno.option_is_valid_directory(x),
            help='Define include DIR to pre-processor. We allow multiple')
        cogeno.options_add_argument('--edts:dts-pp-sources', nargs='+', metavar='FILE',
            dest='edts_dts_pp_sources', action='append',
            type=lambda x: cogeno.option_is_valid_file(x),
            help='The DTS input FILE(s) to pre-process to DTS file.')

    if getattr(cogeno, '_edtsdb') is not None and force_extract is False:
        return cogeno._edtsdb

    # EDTS database file
    if cogeno.option('edts_db'):
        edts_db = cogeno.option('edts_db')
    else:
        cogeno.error(
            "No path defined for the extended device tree database file.", 2)
    edts_db = Path(edts_db)

    # DTS file
    if cogeno.option('edts_dts'):
        edts_dts = cogeno.option('edts_dts')
        edts_dts = Path(edts_dts)
    elif not edts_db.is_file():
        # EDTS DB file not available and no DTS file specified
        cogeno.error(
            "No path defined for the device tree specification file.", 2)
    else:
        edts_dts = None
    if edts_dts and not edts_dts.is_file() and not cogeno.option('edts_dts_pp_sources'):
        cogeno.error(
            "Device tree specification file '{}' not found/ no access.".
            format(edts_dts), 2)

    # Bindings Dirs
    edts_bindings_dirs = []
    if cogeno.option('edts_bindings_dirs'):
        paths = cogeno.option('edts_bindings_dirs')
        if not isinstance(paths, list):
            paths = [paths]
        if isinstance(paths[0], list):
            paths = [item for sublist in paths for item in sublist]
        for path in paths:
            try:
                path = Path(path).resolve()
            except FileNotFoundError:
                # Python 3.4/3.5 will throw this exception
                # Python >= 3.6 will not throw this exception
                path = Path(path)
            if path.is_file():
                path = path.parent # the directory
            if path.is_dir() and path not in edts_bindings_dirs:
                edts_bindings_dirs.append(path)
            else:
                cogeno.warning(f'edtsdatabase.py: Unknown bindings path {path}- ignored')
        # remove duplicates
        edts_bindings_dirs = list(set(edts_bindings_dirs))
    if edts_dts and len(edts_bindings_dirs) == 0:
        cogeno.error("No path defined for the device tree bindings.", 2)

    # Bindings exclude
    edts_bindings_exclude = []
    if cogeno.option('edts_bindings_exclude'):
        paths = cogeno.option('edts_bindings_exclude')
        if not isinstance(paths, list):
            paths = [paths]
        if isinstance(paths[0], list):
            paths = [item for sublist in paths for item in sublist]
        for path in paths:
            try:
                path = Path(path).resolve()
            except FileNotFoundError:
                # Python 3.4/3.5 will throw this exception
                # Python >= 3.6 will not throw this exception
                path = Path(path)
            if path.is_dir():
                edts_bindings_exclude.append(path)
            elif path.is_file() and path.suffix == '.yaml':
                edts_bindings_exclude.append(path)
            else:
                cogeno.warning(f'edtsdatabase.py: Unknown bindings exclude path {path} - ignored')
        # remove duplicates
        edts_bindings_exclude = list(set(edts_bindings_exclude))

    # Bindings no defaults
    edts_bindings_no_default = False
    if cogeno.option('edts_bindings_no_default'):
        edts_bindings_no_default = True

    cogeno.log('s{}: access EDTS {} with lock {}'
               .format(cogeno.cogeno_state(),
                       str(edts_db), cogeno.lock_file()))

    # Try to get a lock to access the database file
    # If we do not get the lock for 10 seconds an
    # exception is thrown.
    try:
        with cogeno.lock().acquire(timeout = 10):

            # Check whether extraction is necessary
            # All failure cases handled above
            extract = False
            if not edts_db.is_file():
                extract = True
            elif edts_dts and not edts_dts.is_file():
                extract = True
            elif edts_dts:
                # EDTS file must be newer than the DTS file
                edts_dts_date = edts_dts.stat().st_mtime
                edts_db_date = edts_db.stat().st_mtime
                if edts_dts_date > edts_db_date:
                    extract = True

            if not extract:
                # Do not log here as log also requests the global lock
                log_msg = "s{}: load EDTS database '{}'".format(cogeno.cogeno_state(),
                                 str(edts_db))
                # load database
                cogeno._edtsdb = EDTSDb()
                cogeno._edtsdb.load(edts_db)

                # check preprocessing dependencies
                dependencies = cogeno._edtsdb._edts['info'].get('edts-dts-depends', None)
                if dependencies:
                    # There are dependencies -> preprocessing has to be checked
                    if not edts_dts:
                        # Dependencies given but no DTS file
                        cogeno.error(
                            "Generated extended device tree database file '{}' has DTS dependencies without given DTS file."
                            .format(edts_db), frame_index = 2)
                    edts_dts_depends = [Path(path) for path in dependencies]
                    # DTS file which must be newer than the dependencies
                    edts_dts_date = edts_dts.stat().st_mtime
                    for dts_depend in edts_dts_depends:
                        if not dts_depend.is_file():
                            extract = True
                            break
                        dts_depend_date = dts_depend.stat().st_mtime
                        if dts_depend_date > edts_dts_date:
                            extract = True
                            break

            if extract:
                # Do not log here as log also requests the global lock
                log_msg = 's{}: extract EDTS {} from {} with bindings {} excluding {} using default {}' \
                         .format(cogeno.cogeno_state(),
                                 str(edts_db),
                                 str(edts_dts),
                                 edts_bindings_dirs,
                                 edts_bindings_exclude,
                                 edts_bindings_no_default)

                # Remove old file
                if edts_db.is_file():
                    edts_db.unlink()
                    unlink_wait_count = 0
                    while edts_db.is_file():
                        # do dummy access to wait for unlink
                        time.sleep(1)
                        unlink_wait_count += 1
                        if unlink_wait_count > 5:
                            cogeno.error(
                                "Generated extended device tree database file '{}' no unlink."
                                .format(edts_db), frame_index = 2)

                # Pre process DTS input files
                edts_dts_pp = None
                if cogeno.option('edts_dts_pp_sources'):
                    edts_dts_pp = EDTSPreprocessor()
                    edts_dts_pp.preprocess()

                # Create EDTS database by extraction
                cogeno._edtsdb = EDTSDb()
                cogeno._edtsdb.extract(edts_dts,
                    edts_bindings_dirs, edts_bindings_exclude, edts_bindings_no_default)

                # Add extra info for DTS preprocessing
                if edts_dts_pp:
                    cogeno._edtsdb._edts['info']['edts-dts-depends'] = [str(path) for path in edts_dts_pp.dependencies]

                # Store file to be reused
                cogeno._edtsdb.save(edts_db)

                # check again
                if not edts_db.is_file():
                    cogeno.error(
                        "Generated extended device tree database file '{}' not found/ no access."
                         .format(edts_db), frame_index = 2)

    except cogeno.lock_timeout():
        # Something went really wrong - we did not get the lock
        cogeno.error(
            "Generated extended device tree database file '{}' no access."
            .format(edts_db), frame_index = 2)
    except:
        raise

    cogeno.log(log_msg)

    return cogeno._edtsdb


##
# @brief Extended DTS database for standalone usage.
#
class EDTSDatabase(EDTSDb):

    @staticmethod
    def is_valid_directory(parser, arg):
        try:
            path = Path(arg).resolve()
        except:
            path = Path(arg)
        if not path.is_dir():
            parser.error('The directory {} does not exist!'.format(path))
        else:
            # File directory exists so return the directory
            return str(path)

    @staticmethod
    def is_valid_file(parser, arg):
        try:
            path = Path(arg).resolve()
        except:
            path = Path(arg)
        if not path.is_file():
            parser.error('The file {} does not exist!'.format(path))
        else:
            # File exists so return the file
            return str(path)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def callable_main(self, argv):
        self._parser = argparse.ArgumentParser(
                    description='Extended Device Tree Specification Database.')
        self._parser.add_argument('-l', '--load', metavar='FILE',
            dest='load_file', action='store',
            type=lambda x: EDTSDatabase.is_valid_file(self._parser, x),
            help='Load the input from FILE.')
        self._parser.add_argument('-s', '--save', metavar='FILE',
            dest='save_file', action='store',
            type=lambda x: EDTSDatabase.is_valid_file(self._parser, x),
            help='Save the database to Json FILE.')
        self._parser.add_argument('-e', '--extract', metavar='FILE',
            dest='extract_file', action='store',
            type=lambda x: EDTSDatabase.is_valid_file(self._parser, x),
            help='Extract the database from dts FILE.')
        self._parser.add_argument('-b', '--bindings', nargs='+', metavar='DIR',
            dest='bindings_dirs', action='store',
            type=lambda x: EDTSDatabase.is_valid_directory(self._parser, x),
            help='Use bindings from bindings DIR for extraction.' +
                 ' We allow multiple')
        self._parser.add_argument('-p', '--print',
            dest='print_it', action='store_true',
            help='Print EDTS database content.')

        args = self._parser.parse_args(argv)

        if args.load_file is not None:
            self.load(args.load_file)
        if args.extract_file is not None:
            self.extract(args.extract_file, args.ybindings_dirs)
        if args.save_file is not None:
            self.save(args.save_file)
        if args.print_it:
            pprint(self._edts)

        return 0



def main():
    EDTSDatabase().callable_main(sys.argv)

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
#
# Copyright (c) 2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import subprocess
import shutil
from pathlib import Path

from collections.abc import MutableMapping

import cogeno

##
# @brief Protocol buffers code database
#
# All generated code is cached in dictionary.
#
# Usage:
# @code
# cogeno.module_import('protobuf')
# db = protobuf.protodb("nanopb")
# db2 = protobuf.protodb("py")
# cogeno.out(db['my_message.pb.h'])
# cogeno.out(db('pb_encode.c'])
# @endcode
class ProtoCodeDb(MutableMapping):

    ##
    # @brief Initialize protocol buffer code database
    #
    # @param generator Any of 'nonopb', ...
    # @param sources *.proto sources
    # @param include_dirs Directories to search for *.proto import
    # @param dst_dir Destination directory for generated code
    def __init__(self, generator = None, sources = None, include_dirs = None, dst_dir = None):
        self._store = dict()
        self._generator = generator
        self._sources = []
        self._include_dirs = []

        self.add_sources(sources)
        self.add_include_dirs(include_dirs)

        self._dst_dir = Path(dst_dir)

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    @staticmethod
    def protoc_gen_nanopb_path():
        import nanopb
        return Path(nanopb.__file__).parent.joinpath('generator/protoc-gen-nanopb')

    @staticmethod
    ##
    # @brief Check if grpcio-tools protoc is installed.
    # @return True if installed, False otherwise
    def has_grpcio_protoc():
        # type: () -> bool

        try:
            import grpc_tools.protoc
        except ImportError:
            return False
        return True

    ##
    # @brief Add sources to the list of sources for generation
    #
    # @param sources List of source file pathes
    # @return True in case new sources were added, False otherwise.
    def add_sources(self, sources):
        new_source = False
        if sources is not None:
            for source in sources:
                source = Path(source)
                if source not in self._sources:
                    new_source = True
                    self._sources.append(source)
                    # make the parent directory of every source file an include path
                    self.add_include_dirs([source.parent])
        return new_source

    ##
    # @brief Add include directories to the list for generation
    #
    # @param include_dirs List of include dir pathes
    # @return True in case new include dirs were added, False otherwise.
    def add_include_dirs(self, include_dirs):
        new_include_dir = False
        if include_dirs is not None:
            for include_dir in include_dirs:
                include_dir = Path(include_dir)
                if include_dir not in self._include_dirs:
                    self._include_dirs.append(include_dir)
        return new_include_dir

    ##
    # @brief Load generated code into database.
    def load(self):
        if self._dst_dir.is_dir():
            # load generated code
            for (top_path, dir_pathes, file_pathes) in cogeno.path_walk(self._dst_dir, topdown = False):
                for file_path in file_pathes:
                    self.__setitem__(file_path.name, file_path.read_text())

        # load generator specific commons
        if self._generator == 'protobluff':
            protoc_gen_protobluff = shutil.which('protoc-gen-protobluff')
            protobluff_include = Path(protoc_gen_protobluff).parent.parent.joinpath('include')
            commons = [protobluff_include.joinpath('protobluff'), protobluff_include.joinpath('protobluff.h')]
        else:
            commons = [Path(__file__).parent.joinpath(f'protodb/{self._generator}')]
        for common in commons:
            if common.is_dir():
                for (top_path, dir_pathes, file_pathes) in cogeno.path_walk(common, topdown = False):
                    for file_path in file_pathes:
                        if file_path.name.startswith(('LICENSE', 'wget_')):
                            continue
                        self.__setitem__(file_path.name, file_path.read_text())
            else:
                self.__setitem__(common.name, common.read_text())

    ##
    # @brief Generate protocol buffer code
    #
    # @note This routine will use grpcio-provided protoc if it exists,
    #       and is using the system-installed protoc as a fallback.
    #
    # @return protoc invocation return value
    def generate(self):
        # type: (list) -> typing.Any

        # Select proto compiler
        if self._generator == 'pbtools':
            protoc = False
            grpc_protoc = None
            from pbtools.c_source.__init__ import generate_files as pbtools_generate_c_files
        elif ProtoCodeDb.has_grpcio_protoc() and not self._generator == 'protobluff':
            protoc = True
            import grpc_tools.protoc as grpc_protoc
            argv = ['protoc']
        else:
            protoc = shutil.which('protoc')
            grpc_protoc = None
            argv = [protoc]

        commons_dir = Path(__file__).parent.joinpath(f'protodb/{self._generator}')

        # protoc arguments
        if protoc:
            import_path_flag = '--proto_path='
            output_path_flag = f'--{self._generator}_out='

            if self._generator in ('cpp', 'python'):
                pass
            elif self._generator == 'nanopb':
                argv.append(f'--plugin=protoc-gen-nanopb={ProtoCodeDb.protoc_gen_nanopb_path()}')
                argv.append(f'--proto_path={commons_dir}')
            elif self._generator == 'protobluff':
                protoc_gen_protobluff = shutil.which('protoc-gen-protobluff')
                if not protoc_gen_protobluff:
                    cogeno.error(
                        f'protoc plugin protoc-gen-protobluff not found - {self._generator}.', 2)
                argv.append(f'--plugin=protoc-gen-protobluff={protoc_gen_protobluff}')
            else:
                cogeno.error(
                    f'Unknown protobuf generator {self._generator}.', 2)

            if grpc_protoc:
                import pkg_resources
                grpc_protoc_include = pkg_resources.resource_filename('grpc_tools', '_proto')
                # Add protoc include paths
                if grpc_protoc_include:
                    argv.append(f'{import_path_flag}{grpc_protoc_include}')

            for include_dir in self._include_dirs:
                argv.append(f'{import_path_flag}{include_dir}')

            # Add output directory
            argv.append(f'{output_path_flag}{self._dst_dir}')

            # Add protoc sources
            for source in self._sources:
                argv.append(f'{source}')

        # Assure destination directory exists
        self._dst_dir.mkdir(parents=True, exist_ok=True)

        # Execute proto compiler/ generator
        if self._generator == 'pbtools':
            # prepare pathes for pbtools - needs strings
            import_path = []
            for include_dir in self._include_dirs:
                import_path.append(str(include_dir))
            output_directory = str(self._dst_dir)
            infiles = []
            for source in self._sources:
                infiles.append(str(source))

            # generate c code
            pbtools_generate_c_files(infiles, import_path, output_directory)

        elif grpc_protoc:
            return grpc_protoc.main(argv)
        elif protoc:
            return subprocess.run(argv)
        else:
            cogeno.error(
                f'Unknown protobuf generator {self._generator}.', 2)


##
# @brief Get protocol buffer code prepared for cogeno use.
#
# @param generator The protocol buffer generator to use to generate
#                  the protocol buffer code. One of 'nanopb', 'pbtools',
#                  'protobluff', 'cpp', 'python'.
#                  Default is 'nanopb'.
# @param force_generate Force generation of the protocol buffer code, even if
#                       already generated.
#                       Default is False.
# @return Protocol buffer code database
def proto_gen(generator='nanopb', force_generate = False):
    protodb_name = f'_protodb{generator}'
    if not hasattr(cogeno, protodb_name):
        # Make the protocol buffer code database a hidden attribute of the generator
        setattr(cogeno, protodb_name, None)

        cogeno.options_add_argument('--protobuf:db-dir', metavar='DIR',
            dest='protobuf_db_dir', action='store',
            help='Write or read protocol buffer code databases to/ from DIR.')
        cogeno.options_add_argument('--protobuf:sources', nargs='+', metavar='FILE',
            dest='protobuf_sources', action='append',
            type=lambda x: cogeno.option_is_valid_file(x),
            help='The *.proto source FILE(s) to generate the protocol buffer code for.')
        cogeno.options_add_argument('--protobuf:include-dirs', nargs='+', metavar='DIR',
            dest='protobuf_include_dirs', action='append',
            type=lambda x: cogeno.option_is_valid_directory(x),
            help='Search for *.proto import files in the protocol buffer include DIR(s).')

    # Protobuf databases directory
    if cogeno.option('protobuf_db_dir'):
        protobuf_db_dir = cogeno.option('protobuf_db_dir')
    else:
        cogeno.error(
            "No path defined for the directory for protocol buffer code databases.", 2)
    # Destination directory to generate the protocol buffer code
    protobuf_dst_dir = Path(protobuf_db_dir).joinpath(generator)

    # Protocol buffers *.proto sources
    protobuf_sources = []
    if cogeno.option('protobuf_sources'):
        paths = cogeno.option('protobuf_sources')
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
            if path.is_file() and path not in protobuf_sources:
                protobuf_sources.append(path)
            else:
                cogeno.warning(f'protobuf.py: Unknown source path {path} - ignored')
    else:
        # This may be ok in case we want only get access to the common files of a generator
        cogeno.warning(
            "protobuf.py: No *.proto source file given for protocol buffer code.")

    # Protocol Buffers Include Dirs
    protobuf_include_dirs = []
    if cogeno.option('protobuf_include_dirs'):
        paths = cogeno.option('protobuf_include_dirs')
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
            if path.is_dir() and path not in protobuf_include_dirs:
                protobuf_include_dirs.append(path)
            else:
                cogeno.warning(f'protobuf.py: Unknown include directory path {path} - ignored')
        # remove duplicates
        protobuf_include_dirs = list(set(protobuf_include_dirs))
        if len(protobuf_include_dirs) == 0:
            cogeno.error("No path defined for the protobuf include directory.", 2)

    # Create database object if necessary and check whether generation is necessary
    # All failure cases handled above
    protodb = getattr(cogeno, protodb_name)
    if protodb is not None:
        # We already have a database.
        # Assure all source files are already generated
        if cogeno._protodb.add_sources(protobuf_sources):
            # We added some unknown source
            force_generate = True
        if cogeno._protodb.add_include_dirs(protobuf_include_dirs):
            # We added some unknown include directory
            force_generate = True
    else:
        # We create a new database
        protodb = ProtoCodeDb(generator = generator,
                            sources = protobuf_sources,
                            include_dirs = protobuf_include_dirs,
                            dst_dir = protobuf_dst_dir)
        setattr(cogeno, protodb_name, protodb)
        if len(protodb._sources) > 0:
            force_generate = True

    cogeno.log('s{}: access protobuf code database {} with lock {}'
               .format(cogeno.cogeno_state(),
                       protodb._dst_dir, cogeno.lock_file()))

    # Try to get a lock to access the database.
    # If we do not get the lock for 10 seconds an
    # exception is thrown.
    try:
        with cogeno.lock().acquire(timeout = 10):
            # Do not log here as log also requests the global lock
            log_msg = ""

            if force_generate is False:
                if len(protodb._sources) > 0:
                    for source in protodb._sources:
                        # modification time of destination dir must be newer than any proto file
                        if source.stat().st_mtime > protodb._dst_dir.stat().st_mtime:
                            force_generate = True
                            break
                else:
                    log_msg += '\ns{}: load protobuf code database {}'.format(cogeno.cogeno_state(),
                                        str(protodb._dst_dir))
                    # Do a dummy load to load common code files
                    protodb.load()

            if force_generate:
                log_msg += '\ns{}: generate protobuf code database in {} from {}' \
                           .format(cogeno.cogeno_state(),
                                   protodb._dst_dir,
                                   protodb._sources)

                # Assure that the directory is available
                protodb._dst_dir.mkdir(parents = True, exist_ok = True)

                # Remove generated code that will be newly generated.
                # Just to be shure protoc can write to file and missing
                # will be detected.
                sources_stem = []
                for source in protodb._sources:
                    sources_stem.append(source.stem)
                for generated in protodb._dst_dir.iterdir():
                    if generated.stem in sources_stem:
                        generated.unlink()
                        unlink_wait_count = 0
                        while generated.is_file():
                            # do dummy access to wait for unlink
                            time.sleep(1)
                            unlink_wait_count += 1
                            if unlink_wait_count > 5:
                                cogeno.error(
                                    "Generated protobuf code database file '{}' no unlink."
                                    .format(generated), frame_index = 2)

                # generate protobuf code
                protodb.generate()

                log_msg += '\ns{}: load protobuf code database {}'.format(cogeno.cogeno_state(),
                                    str(protodb._dst_dir))
                # load database
                protodb.load()

    except cogeno.lock_timeout():
        # Something went really wrong - we did not get the lock
        cogeno.error(
            "Generated protobuf code database '{}' no access."
            .format(protodb._dst_dir), frame_index = 2)
    except:
        raise

    cogeno.log(log_msg)

    return protodb

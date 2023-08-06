# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import mmap
from pathlib import Path

class PathsMixin(object):
    __slots__ = []

    _modules_paths = None
    _templates_paths = None

    ##
    # @brief Walk directory tree.
    #
    # For each directory in the tree rooted at directory top (including top itself),
    # it yields a 3-tuple (dirpath, dirnames, filenames):
    # - dirpath: the path to the directory.
    # - dirnames: list of the paths of the subdirectories in dirpath
    # - filenames: list of the paths of the non-directory files in dirpath
    #
    # See Python docs for os.walk, exact same behavior but it yields Path()
    # instances instead.
    # From: http://ominian.com/2016/03/29/os-walk-for-pathlib-path/
    #
    # @param top root of directory tree
    # @param topdown if topdown is True, the triple for a directory is generated before
    #                the triples for any of its subdirectories (directories are generated
    #                top-down). If topdown is False, the triple for a directory is
    #                generated after the triples for all of its subdirectories
    #                (directories are generated bottom-up).
    # @param followlinks
    # @return yields a 3-tuple (dirpath, dirpathes, filepathes)
    @staticmethod
    def path_walk(top, topdown = False, followlinks = False):
        names = list(top.iterdir())

        dirs = (node for node in names if node.is_dir() is True)
        nondirs = (node for node in names if node.is_dir() is False)

        if topdown:
            yield top, dirs, nondirs

        for name in dirs:
            if followlinks or name.is_symlink() is False:
                for x in PathsMixin.path_walk(name, topdown, followlinks):
                    yield x

        if topdown is not True:
            yield top, dirs, nondirs

    ##
    # @brief Delete an entire directory tree
    #
    # @param top root of directory tree
    @staticmethod
    def rmtree(top):
        top = Path(top) # allow top to be a string
        assert top.is_dir() # make sure it`s a folder

        for (top_path, dir_pathes, file_pathes) in PathsMixin.path_walk(top, topdown = False):
            for file_path in file_pathes:
                filepath.unlink()
            for dir_path in dir_pathes:
                dir_path.rmdir()

    ##
    # @brief Find template files.
    #
    # @param marker Marker as b'my-marker'
    # @param suffix
    # @return List of template file pathes
    @staticmethod
    def find_template_files(top, marker, suffix='.c'):
        sources = []
        for path, directory_names, file_names in PathsMixin.path_walk(top):
            sources.extend([x for x in file_names if x.suffix == suffix])

        templates = []
        for source_file in sources:
            if os.stat(source_file).st_size == 0:
                continue
            with open(source_file, 'rb', 0) as source_file_fd:
                s = mmap.mmap(source_file_fd.fileno(), 0, access=mmap.ACCESS_READ)
                if s.find(marker) != -1:
                    templates.append(source_file)
        return templates

    @staticmethod
    def cogeno_path():
        return Path(__file__).resolve().parent

    @staticmethod
    def find_file_path(file_name, paths):
        # Assure we have a string here
        file_name = str(file_name)
        try:
            file_path = Path(file_name).resolve()
        except FileNotFoundError:
            # Python 3.4/3.5 will throw this exception
            # Python >= 3.6 will not throw this exception
            file_path = Path(file_name)
        if file_path.is_file():
            return file_path

        # don't resolve upfront
        file_dir_parts = list(Path(file_name).parent.parts)
        for path in paths:
            file_path = None
            if len(file_dir_parts) > 0:
                path_parts = list(path.parts)
                common_start_count = path_parts.count(file_dir_parts[0])
                common_start_index = 0
                while common_start_count > 0:
                    common_start_count -= 1
                    common_start_index = path_parts.index(file_dir_parts[0], common_start_index)
                    common_length = len(path_parts) - common_start_index
                    if common_length > len(file_dir_parts):
                        # does not fit
                        continue
                    if path_parts[common_start_index:] == file_dir_parts[0:common_length]:
                        # We have a common part
                        file_path = path.parents[common_length - 1].joinpath(file_name)
                        if file_path.is_file():
                            # we got it
                            return file_path
                        else:
                            # may be there is another combination
                            file_path = None
            if file_path is None:
                # Just append file path to path
                file_path = path.joinpath(file_name)
            if file_path.is_file():
                return file_path
        return None

    def modules_paths_append(self, path):
        self._context._modules_paths.append(Path(path))
        self.cogeno_module.path.extend(str(path))
        sys.path.extend(str(path))

    def modules_paths(self):
        return self._context._modules_paths

    def templates_paths_append(self, path):
        self._context._templates_paths.append(Path(path))

    def templates_paths(self):
        return self._context._templates_paths

    def template_path(self):
        return Path(self._context._template_file).resolve().parent

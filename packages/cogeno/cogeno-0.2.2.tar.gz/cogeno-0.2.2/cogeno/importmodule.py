# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

import sys
import os
import copy
import importlib
import importlib.util
import inspect
from pathlib import Path

class ImportMixin(object):
    __slots__ = []


    ##
    # Setting scope_level=1 works for a function defined in a submodule,
    # scope_level=2 for the inner function defined in a decorator in a submodule, etc.
    #
    # https://stackoverflow.com/questions/4851463/in-python-2-how-do-i-write-to-variable-in-the-parent-scope
    @staticmethod
    def _calling_scope_globals(scope_level=0):
        return dict(inspect.getmembers(inspect.stack()[scope_level][0]))["f_globals"]

    ##
    # @brief Import a Cogeno module.
    #
    # Import a module.
    #
    # Module file is searched in current directory or modules directories.
    #
    # @param name Module to import. Specified without any path.
    def import_module(self, name):
        module_name = "{}.py".format(name)
        # collect pathes to search for module (script directory and modules dirs)
        paths = []
        paths.append(self.template_path())
        paths.extend(self.modules_paths())
        # search for module
        module_file = self.find_file_path(module_name, paths)
        if module_file is None:
            raise self._get_error_exception(
                "Module file '{}' of module '{}' does not exist or is no file.\n".
                format(module_name, name) + \
                "Searched in {}.".format(paths), 1)

        sys.path.append(os.path.dirname(str(module_file)))
        module = importlib.import_module(name)
        sys.path.pop()
        # remember in context
        self._context.generation_globals()[name] = module
        # Make it available immediatedly to the calling scope
        # in case it is not a snippet but an imported python module
        # calling cogeno.import_module.
        self._calling_scope_globals(scope_level = 2)[name] = module

    def _import_extension(self, extension_name, extension_file_path, update):
        if extension_name in self._context.generation_globals():
            if update:
                del self._context.generation_globals()[extension_name]
                del self._calling_scope_globals(scope_level = 2)[extension_name]
            else:
                return
        # https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
        spec = importlib.util.spec_from_file_location(extension_name, extension_file_path)
        module = importlib.util.module_from_spec(spec)
        # remember in context
        self._context.generation_globals()[extension_name] = module
        # Make it available immediatedly to the calling scope
        self._calling_scope_globals(scope_level = 2)[extension_name] = module

        spec.loader.exec_module(module)
        self.log(f"Extension '{extension_name!r}' imported from '{extension_file_path}'\n")
        return module

    ##
    # @brief Import extension modules.
    #
    # Extension paths are searched for extension modules.
    #
    # @param extensions_paths Directory paths for extensions
    # @param update Optional, on true the modules are reloaded if already loaded
    def import_extensions(self, extensions_paths, update=False):
        if not extensions_paths:
            return
        if not isinstance(extensions_paths, list):
            extensions_paths = [extensions_paths]
        for extension_path in extensions_paths:
            extension_path = Path(extension_path).resolve()
            extensions_dir_path = extension_path.joinpath('cogeno')
            if not extensions_dir_path.is_dir() or extensions_dir_path == Path(__file__).parent:
                # No directory at all or the cogeno directory of Cogeno
                continue
            extension_files_paths = extensions_dir_path.glob('*.py')
            if not extension_files_paths:
                continue
            for extension_file_path in extension_files_paths:
                if extension_file_path.is_file():
                    extension_name = extension_file_path.stem
                    extension_file_path.resolve()
                    extension = self._import_extension(extension_name, extension_file_path, update)

    ##
    # @brief Import extension modules given in extension:paths option.
    #
    # Extension paths are searched for extension modules. Thes modules are
    # imported. As modules may update the option in itself the import is done
    # recursively.
    #
    # @param update Optional, on true the modules are reloaded if already loaded
    def import_extensions_from_option(self, update=False):
            # Assure extensions are available
            extensions = self.option('extensions_paths')
            extensions_all = copy.copy(extensions)
            while extensions:
                self.import_extensions(extensions, update)
                # Maybe the extension added more extensions
                extensions_after = self.option('extensions_paths')
                extensions = []
                for extension in extensions_after:
                    if not extension in extensions_all:
                        extensions.append(extension)
                extensions_all.extend(extensions_after)

# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path
import json

import cogeno

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from kconfig.kconfiglib import Kconfig, TYPE_TO_STR
else:
    # use current package visibility
    from .kconfig.kconfiglib import Kconfig, TYPE_TO_STR

class ConfigDB(object):

    def _update_symbols(self):
        if self._kconfig == None:
            return

        for name, symbol in self._kconfig.syms.items():
            if symbol == None or not symbol.nodes:
                # No such Kconfig symbol or symbol is undefined
                continue

            self._configdb['symbols'][name] = {}
            self._configdb['symbols'][name]['info'] = str(symbol)

            description = None
            # Use the first help text, if available
            for node in symbol.nodes:
                if node.help is not None:
                    description = node.help
                    break
            if description is None:
                # If there's no help, use the first prompt string
                for node in symbol.nodes:
                    if node.prompt:
                        description = node.prompt[0]
                        break
            if description is None:
                description = '<unknown>'
            self._configdb['symbols'][name]['description'] = description

            self._configdb['symbols'][name]['name-and-location'] = symbol.name_and_loc
            #self._configdb['symbols'][name]['defaults'] = symbol.defaults
            #self._configdb['symbols'][name]['selects'] = symbol.selects
            #self._configdb['symbols'][name]['implies'] = symbol.implies
            self._configdb['symbols'][name]['is-constant'] = symbol.is_constant
            self._configdb['symbols'][name]['type'] = TYPE_TO_STR[symbol.type]

        return self._configdb['symbols']

    def _update_properties(self):
        if self._kconfig == None:
            return None

        config_content = self._kconfig._config_contents(header = None)
        for line in config_content.splitlines():
            if line.startswith('#') or not line.strip():
                continue
            config = line.split('=')
            key = config[0].strip()
            value = config[1].strip()
            if value in ('y'):
                value = "true"
            elif value in ('n'):
                value = "false"
            else:
                value = value.replace('"','')
            self._configdb['properties'][key] = value

        return self._configdb['properties']

    def _update_kconfig_files(self):
        if self._kconfig == None:
            return None

        kconfig_files = sorted(list(set(self._kconfig.kconfig_filenames)))
        self._configdb['kconfig-files'] = []
        # Make all file pathes absolute
        for kconfig_file in kconfig_files:
            path = Path(kconfig_file)
            if not path.is_absolute():
                path = Path(self._kconfig.srctree).joinpath(path)
            try:
                path = path.resolve()
            except FileNotFoundError:
                # Python 3.4/3.5 will throw this exception
                # Python >= 3.6 will not throw this exception
                pass
            self._configdb['kconfig-files'].append(str(path))

    ##
    # @brief Generate config database.
    #
    # @param config_kconfig_file path of top-level Kconfig file
    # @param config_kconfig_srctree path for relative lookup of files
    # @param config_kconfig_defines optional, dictionary of variables to be defined to Kconfig
    # @param config_inputs optional, list of configuration fragment file pathes
    # @param config_file optional, config file path 
    def generate(self, config_kconfig_file,
                 config_kconfig_srctree,
                 config_kconfig_defines = None,
                 config_inputs = None,
                 config_file = None):
        if config_kconfig_defines is None:
            config_kconfig_defines = {}
        if config_inputs is None:
            config_inputs = []
        if config_file:
            config_file = Path(config_file)

        # set environment needed by kconfiglib
        os.environ['KCONFIG_FUNCTIONS'] = 'kconfig.cogenofunctions'
        os.environ['srctree'] = str(config_kconfig_srctree)
        for define in config_kconfig_defines:
            env = define.split('=')
            key = env[0].strip()
            value = env[1].strip()
            os.environ[key] = value

        # We have a hen egg problem: config needs edts and edts needs config
        # 1) Create a first time configuration to get the config properties
        #    Ignore all errors/ warnings
        # 2) Update Cogeno extensions
        # 3) Redo configuration with (some) known config parameters

        # 1) create the the first time configuration
        self._kconfig = Kconfig(filename = str(config_kconfig_file), suppress_traceback=True)
        self._kconfig.warn = False
        if config_file and config_file.is_file():
            self._kconfig.load_config(str(config_file))
        for config_input in config_inputs:
            # replace=False creates a merged configuration
            self._kconfig.load_config(str(config_input), replace=False)
        #   set the first time config parameters
        self._update_properties()

        # 2) update the extensions, which may set new vars based on changed config
        cogeno.import_extensions_from_option(update=True)
        #    also update edts which may get new data
        edts = cogeno.edts(force_extract=True)

        # 2) Redo configuration with extension having done their job
        self._kconfig.unset_values()
        self._kconfig.warn = True
        if config_file and config_file.is_file():
            self._kconfig.load_config(str(config_file))
        # load fragments
        # Warn for assignments to undefined symbols, but only for handwritten
        # fragments, to avoid warnings-turned-errors when using an old
        # configuration file together with updated Kconfig files
        self._kconfig.warn_assign_undef = True
        # fragments may override settings from kconfig file, so
        # disable warnings about symbols being assigned more than once
        self._kconfig.warn_assign_override = False
        self._kconfig.warn_assign_redun = False
        for config_input in config_inputs:
            # replace=False creates a merged configuration
            self._kconfig.load_config(str(config_input), replace=False)

        # Hack: Force all symbols to be evaluated, to catch warnings generated
        # during evaluation. Wait till the end to write the actual output files, so
        # that we don't generate any output if there are warnings-turned-errors.
        #
        # Kconfiglib caches calculated symbol values internally, so this is still
        # fast.
        config_content = self._kconfig._config_contents(header = None)

        if self._kconfig.warnings:
            warnings = ""
            # Put a blank line between warnings to make them easier to read
            for warning in self._kconfig.warnings:
                warnings += "\n" + warning

            # Turn all warnings into errors, so that e.g. assignments to undefined
            # Kconfig symbols become errors.
            #
            # A warning is generated by this script whenever a symbol gets a
            # different value than the one it was assigned. Keep that one as just a
            # warning for now.
            raise RuntimeError(
                "Aborting due to Kconfig warning in '{}'.{}".
                format(config_kconfig_file, warnings))

        # set properties
        self._update_properties()
        self._update_symbols()
        self._update_kconfig_files()

    ##
    # @brief Load config database from JSON database file.
    #
    # @param file_path Path of JSON file
    def load(self, file_path):
        with Path(file_path).open(mode = "r", encoding="utf-8") as load_file:
            self._configdb = json.load(load_file)

    ##
    # @brief Save config database to JSON database file.
    #
    # @param file_path Path of JSON file
    def save(self, file_path):
        with Path(file_path).open(mode="w", encoding="utf-8") as save_file:
            json.dump(self._configdb, save_file, indent = 4, sort_keys=True)

    ##
    # @brief Extract config database from config file.
    #
    # The config file does not provide symbol information. 
    # symbols(), symbol_info() and kconfig_files() will not work
    # on a database that was extracted from a config file.
    #
    # @param config_file Path of config file
    def extract(self, config_file):
        config_file = Path(config_file)
        if not config_file.is_file():
            raise RuntimeError(
                "Config file '{}' does not exist or is no file.".
                format(config_file))
        with config_file.open(mode = 'r', encoding = 'utf-8') as config_fd:
            for line in config_fd:
                if line.startswith('#') or not line.strip():
                    continue
                config = line.split('=')
                key = config[0].strip()
                value = config[1].strip()
                if value in ('y'):
                    value = "true"
                elif value in ('n'):
                    value = "false"
                else:
                    value = value.replace('"','')
                self._configdb['properties'][key] = value
        return self._configdb['properties']

    def __init__(self, *args, **kw):
        self._kconfig = None
        self._configdb = {
            'symbols' : {},
            'properties' : dict(*args, **kw),
            'kconfig-files' : []
            }


    ##
    # @brief Get the value of a configuration property from .config.
    #
    # If property_name is not given in the database the default value is returned.
    #
    # @param property_name Name of the property (aka. symbol)
    # @param default Property value to return per default.
    # @return property value
    def property(self, property_name, default="<unset>"):
        property_value = self._configdb['properties'].get(property_name, default)
        if property_value == "<unset>":
            raise RuntimeError(
                "config property '{}' not defined.".format(property_name))
        return property_value

    ##
    # @brief Get all config properties.
    #
    # The property names are the ones that are in the database.
    #
    # @return A dictionary of config properties.
    def properties(self):
        return self._configdb['properties']

    ##
    # @brief Get all config symbols.
    #
    # @return A dictionary of config symbols.
    def symbols(self):
        return self._configdb['symbols']

    ##
    # @brief Get the info of a configuration symbol.
    #
    # If symbol_name is not available or Kconfig was not processed
    # the default value is returned.
    #
    # @param symbol_name Name of the configuration symbol
    # @param default Symbol info to return per default.
    # @return symbol info
    def symbol_info(self, symbol_name, default="<unknown>"):
        if not symbol_name in self._configdb['symbols']:
            if default == "<unknown>":
                raise RuntimeError(
                    "config symbol '{}' not defined.".format(symbol_name))
            return default

        return self._configdb['symbols'][symbol_name]['info']

    ##
    # @brief Get all Kconfig files.
    #
    # Get all Kconfig files used to generate() the database.
    #
    # @return A list of kconfig file pathes.
    def kconfig_files(self):
        return self._configdb['kconfig-files']


##
# @brief Get config properties database prepared for cogeno use.
#
# @param force_extract force extraction from Kconfig file if available
# @return config properties database.
def configs(force_extract = False):
    if not hasattr(cogeno, '_configdb'):
        # Make the config database a hidden attribute of the generator
        cogeno._configdb = None

        cogeno.options_add_argument('--config:db', metavar='FILE',
            dest='config_db', action='store',
            help='Write or read config database to/ from FILE.')

        cogeno.options_add_argument('--config:kconfig-file', metavar='FILE',
            dest='config_kconfig_file', action='store',
            default='Kconfig',
            help='Top-level Kconfig FILE (default: Kconfig).')

        cogeno.options_add_argument('--config:kconfig-srctree', metavar='DIR',
            dest='config_kconfig_srctree', action='store',
            help="""\
Kconfig files are looked up relative to the srctree DIR (unless absolute paths
are used), and .config files are looked up relative to the srctree DIR if they
are not found in the current directory.""")

        cogeno.options_add_argument('--config:kconfig-defines', nargs='+', metavar='DEFINE',
            dest='config_kconfig_defines', action='append',
            help='Define variable to Kconfig. We allow multiple.')

        cogeno.options_add_argument('--config:inputs', nargs='+', metavar='FILE',
            dest='config_inputs', action='append',
            help='Read configuration file fragment from FILE. We allow multiple.')

        cogeno.options_add_argument('--config:file', metavar='FILE',
            dest='config_file', action='store',
            help='Read configuration variables from this FILE.')

    if getattr(cogeno, '_configdb') is not None and force_extract is False:
        return cogeno._configdb

    # --config:db
    if cogeno.option('config_db'):
        path = cogeno.option('config_db')
        try:
            path = Path(path).resolve()
        except FileNotFoundError:
            # Python 3.4/3.5 will throw this exception
            # Python >= 3.6 will not throw this exception
            path = Path(path)
        config_db = path
    else:
        cogeno.error(
            "No path defined for the config database file.", 2)

    # --config:file
    if cogeno.option('config_file'):
        path = cogeno.option('config_file')
        try:
            path = Path(path).resolve()
        except FileNotFoundError:
            # Python 3.4/3.5 will throw this exception
            # Python >= 3.6 will not throw this exception
            path = Path(path)
        config_file = path
    else:
        config_file = None

    # --config:inputs
    config_inputs = []
    if cogeno.option('config_inputs'):
        paths = cogeno.option('config_inputs')
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
                config_inputs.append(path)
            else:
                cogeno.warning(f'config.py: Unknown config input file {path} - ignored')
        # remove duplicates
        config_inputs = list(set(config_inputs))

    # --config:kconfig-file
    if cogeno.option('config_kconfig_file'):
        path = cogeno.option('config_kconfig_file')
        try:
            path = Path(path).resolve()
        except FileNotFoundError:
            # Python 3.4/3.5 will throw this exception
            # Python >= 3.6 will not throw this exception
            path = Path(path)
        if not path.is_file():
            cogeno.error("Kconfig file '{}' not found/ no access.".
                          format(path), 2)
        config_kconfig_file = path
    elif config_file is None or not config_file.is_file():
        # config file not specified/ available and no Kconfig file specified
        cogeno.error("No path defined for the config file.", 2)
    else:
        config_kconfig_file = None
    if config_file and not config_file.is_file() and config_kconfig_file is None:
        cogeno.error("Config file '{}' not found/ no access.".
                     format(config_file), 2)

    if config_kconfig_file:
        # --config:kconfig-srctree
        config_kconfig_srctree = config_kconfig_file.parent
        if cogeno.option('config_kconfig_srctree'):
            path = cogeno.option('config_kconfig_srctree')
            try:
                path = Path(path).resolve()
            except FileNotFoundError:
                # Python 3.4/3.5 will throw this exception
                # Python >= 3.6 will not throw this exception
                path = Path(path)
            if path.is_dir():
                config_kconfig_srctree = path
            else:
                cogeno.warning(f'config.py: srctree path {path} - ignored')

        # --config:kconfig-defines
        config_kconfig_defines = ['COGENO_KCONFIG=1']
        if cogeno.option('config_kconfig_defines'):
            defines = cogeno.option('config_kconfig_defines')
            if not isinstance(defines, list):
                defines = [defines]
            if isinstance(defines[0], list):
                defines = [item for sublist in defines for item in sublist]
            for define in defines:
                if not '=' in define:
                    define += '='
                config_kconfig_defines.append(define)


    # Try to get a lock to access the config database
    # and also the EDTS  database for Kconfig functions.
    # The locking mechanism allows reentrant locking.
    #
    # If we do not get the lock for 10 seconds an
    # exception is thrown.
    try:
        with cogeno.lock().acquire(timeout = 10):
            generate = False
            cogeno._configdb = ConfigDB()
            if config_kconfig_file.is_file() and force_extract:
                generate = True
            elif config_db.is_file():
                # Database is available - load it to
                # retrieve further info about generation.
                cogeno._configdb.load(config_db)
                # Check whether database is uptodate
                config_date = config_db.stat().st_mtime
                for kconfig_file in cogeno._configdb.kconfig_files():
                    kconfig_file = Path(kconfig_file)
                    if not kconfig_file.is_file():
                        generate = True
                        break
                    kconfig_date = kconfig_file.stat().st_mtime
                    if kconfig_date > config_date:
                        generate = True
                        break
            elif config_kconfig_file.is_file():
                # no database but Kconfig file available
                generate = True
            elif config_file.is_file():
                # no database, no Kconfig file but config file
                # load it
                cogeno._configdb.extract(config_file)
            else:
                cogeno.error(
                    "Config database '{}' and config file '{}' is missing."
                    .format(config_db, config_file), frame_index = 2)

            if generate:
                cogeno._configdb.generate(config_kconfig_file,
                                          config_kconfig_srctree,
                                          config_kconfig_defines,
                                          config_inputs, config_file)
                cogeno._configdb.save(config_db)

    except cogeno.lock_timeout():
        # Something went really wrong - we did not get the lock
        cogeno.error(
            "Generated config database '{}' no access."
            .format(config_db), frame_index = 2)
    except:
        raise

    return cogeno._configdb


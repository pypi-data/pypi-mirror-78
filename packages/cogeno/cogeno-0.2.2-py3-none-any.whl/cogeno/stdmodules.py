# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: Apache-2.0

import sys


class StdModulesMixin(object):
    __slots__ = []

    ##
    # @brief Get the extended device tree database.
    #
    # @return Extended device tree database.
    def edts(self, force_extract=False):
        if 'edts' not in sys.modules:
            self.import_module('edts')
        return edts.edts(force_extract)

    ##
    # @brief Get the cmake variables database.
    #
    # @return CMake variables database.
    def cmake(self):
        if 'cmake' not in sys.modules:
            self.import_module('cmake')
        return cmake.cmake()

    ##
    # @brief Get the value of a CMake variable.
    #
    # If variable_name is not provided to cogeno by CMake the default value
    # is returned.
    #
    # A typical set of CMake variables that are not available in the
    # `CMakeCache.txt` file and have to be provided as defines
    # to cogeno if needed:
    #
    # - "PROJECT_NAME"
    # - "PROJECT_SOURCE_DIR"
    # - "PROJECT_BINARY_DIR"
    # - "CMAKE_SOURCE_DIR"
    # - "CMAKE_BINARY_DIR"
    # - "CMAKE_CURRENT_SOURCE_DIR"
    # - "CMAKE_CURRENT_BINARY_DIR"
    # - "CMAKE_CURRENT_LIST_DIR"
    # - "CMAKE_FILES_DIRECTORY"
    # - "CMAKE_PROJECT_NAME"
    # - "CMAKE_SYSTEM"
    # - "CMAKE_SYSTEM_NAME"
    # - "CMAKE_SYSTEM_VERSION"
    # - "CMAKE_SYSTEM_PROCESSOR"
    # - "CMAKE_C_COMPILER"
    # - "CMAKE_CXX_COMPILER"
    # - "CMAKE_COMPILER_IS_GNUCC"
    # - "CMAKE_COMPILER_IS_GNUCXX"
    #
    # @param variable_name Name of the CMake variable
    # @param default Default value
    # @return value
    def cmake_variable(self, variable_name, default="<unset>"):
        return self.cmake().variable(variable_name, default)

    ##
    # @brief Get the value of a CMake variable from CMakeCache.txt.
    #
    # If variable_name is not given in `CMakeCache.txt` the default value is
    # returned.
    #
    # @param variable_name Name of the CMake variable
    # @param default Default value
    # @return value
    def cmake_cache_variable(self, variable_name, default="<unset>"):
        return self.cmake().cache_variable(variable_name, default)

    ##
    # @brief Get the configuration variables database.
    #
    # @return Configuration variables database.
    def configs(self, force_extract=False):
        if 'config' not in sys.modules:
            self.import_module('config')
        return config.configs(force_extract)

    ##
    # @brief Get all config properties.
    #
    # The property names are the ones config file.
    #
    # @return A dictionary of config properties.
    def config_properties(self):
        return self.configs().properties()

    ##
    # @brief Get the value of a configuration property fromthe config file.
    #
    # If property_name is not given in .config the default value is returned.
    #
    # @param property_name Name of the property
    # @param default Property value to return per default.
    # @return property value
    def config_property(self, property_name, default="<unset>"):
        return self.configs().property(property_name, default)

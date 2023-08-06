..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_build:

Build with Cogeno
#################

Code generation has to be invoked as part of the build process of a project.

.. contents::
   :depth: 2
   :local:
   :backlinks: top


Build with CMake and Cogeno
***************************

Projects that use `CMake <https://cmake.org/>`_ to manage building the project
can add the :ref:`cogeno.cmake` script (:download:`cogeno.cmake <../../examples/cmake/cogeno.cmake>`).

By this a file that contains inline code generation can be added to the project
using the ``cogeno_sources`` command in the respective :file:`CMakeList.txt` file.

.. code-block:: CMake

    cogeno_sources(target [EXTERN] [DELETE_SOURCE] [source_file..]
                   [INCLUDES include_file...] [TXTFILES text_file...]
                   [SOURCE_DIR dir] [INCLUDE_DIR dir] [TXTFILE_DIR dir]
                   [COGENO_DEFINES defines..] [DEPENDS target.. file.. dir..])

* EXTERN
    ``EXTERN`` has to be given in case the target was not created in the same
    :file:`CMakeList.txt` file as the ``cogeno_sources`` command is issued.
* DELETE_SOURCE
    If ``DELETE_SOURCE`` is given the generator code is removed from the output file.
* SOURCE_DIR
    ``SOURCE_DIR`` specifies the directory to write the generated source file(s)
    to. A relative path is relative to ``${CMAKE_CURRENT_BINARY_DIR})``. It defaults
    to ``${CMAKE_CURRENT_BINARY_DIR}`` or to the Cogeno ``SOURCE_DIR`` property if
    given. Do not set ``SOURCE_DIR`` in case the
    generated file is a compilable source file (eg. *.c, *.cpp), this will trigger CMake issue
    `#14633 <https://gitlab.kitware.com/cmake/cmake/issues/14633>`_.
* INCLUDE_DIR
    ``INCLUDE_DIR`` specifies the directory to write the generated include file(s)
    to. A relative path is relative to ``${CMAKE_CURRENT_BINARY_DIR})``. It defaults
    to ``${CMAKE_CURRENT_BINARY_DIR}`` or to the Cogeno ``INCLUDE_DIR`` property if
    given.
* TXTFILE_DIR
    ``TXTFILE_DIR`` specifies the directory to write the generated text file(s)
    to. A relative path is relative to ``${CMAKE_CURRENT_BINARY_DIR})``. It defaults
    to ``${CMAKE_CURRENT_BINARY_DIR}`` or to the Cogeno ``TXTFILE_DIR`` property if
    given.
* INCLUDES
    ``INCLUDES`` marks files to be handled as include files (vs. source files).
* TXTFILES
    ``TXTFILES`` marks files to be handled as text files (vs. source files).
    Text files are added as a dependency to the target.
* COGENO_DEFINES
    The arguments given by the ``COGENO_DEFINES`` keyword have to be of
    the form ``define_name=define_value``. The arguments become globals in the python
    snippets and can be accessed by ``define_name``.
* DEPENDS
    Dependencies given by the ``DEPENDS`` keyword are added to the dependencies
    of the generated file. Adding a dependency to a directory adds all files in that directory
    as a dependency.


Use Cogeno modules with CMake
=============================

The options provided to the modules are set by Cogeno CMake properties.

+------------+-----------------------------------+----------------------------------------------+
+ Module     | Property                          | Usage                                        |
+============+===================================+==============================================+
+ ccode      | --                                | --                                           |
+------------+-----------------------------------+----------------------------------------------+
+ cmake      | :ref:`CMAKE_CACHE`                | Path to CMake cache file                     |
+            +-----------------------------------+----------------------------------------------+
+            | :ref:`CMAKE_DEFINES`              | CMake variable defines                       |
+------------+-----------------------------------+----------------------------------------------+
+ config     | :ref:`CONFIG_DB  `                | Path to config database file                 |
+            +-----------------------------------+----------------------------------------------+
+            | :ref:`CONFIG_FILE`                | Path to config file                          |
+            +-----------------------------------+----------------------------------------------+
+            | :ref:`CONFIG_KCONFIG_FILE`        | Path to Kconfig file                         |
+------------+-----------------------------------+----------------------------------------------+
+ edts       | :ref:`EDTS_ARCH`                  | `Use the Cogeno EDTS module with CMake`_     |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_ARCH_FLAVOUR`          |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DTS`                   |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DTS_ROOT`              |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DTS_PP_DEFINES`        |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`   |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DTS_PP_SOURCES`        |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_BINDINGS_DIRS`         |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_BINDINGS_EXCLUDE`      |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_BINDINGS_NO_DEFAULT`   |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`EDTS_DB`                    |                                              |
+------------+-----------------------------------+----------------------------------------------+
+ protobuf   | :ref:`PROTOBUF_DB_DIR`            | `Use the Cogeno protobuf module with CMake`_ |
+            +-----------------------------------+                                              |
+            | :ref:`PROTOBUF_SOURCES`           |                                              |
+            +-----------------------------------+                                              |
+            | :ref:`PROTOBUF_INCLUDE_DIRS`      |                                              |
+------------+-----------------------------------+----------------------------------------------+
+ zephyr     | --                                | --                                           |
+------------+-----------------------------------+----------------------------------------------+



Use the Cogeno EDTS module with CMake
-------------------------------------

The :ref:`cogeno.cmake` script searches the list of directories in the :ref:`EXTENSION_DIRS`
property and the :file:`edts` or :file:`dts` sub-directories within for device tree root pathes.
If the directories exist they are added to the :ref:`EDTS_DTS_ROOT` property.

+-------------------------------------------+------------------------------------------------+
+ :ref:`EXTENSION_DIRS` sub-directory       | Property/ usage                                |
+===========================================+================================================+
+ :file:`.`                                 | :ref:`EDTS_DTS_ROOT`                           |
+-------------------------------------------+------------------------------------------------+
+ :file:`dts`                               | :ref:`EDTS_DTS_ROOT`                           |
+-------------------------------------------+------------------------------------------------+
+ :file:`edts`                              | :ref:`EDTS_DTS_ROOT`                           |
+-------------------------------------------+------------------------------------------------+

The :ref:`EDTS_DTS_ROOT` pathes are searched for a set of standard sub-directories. If
available these sub-directories are added to the respective Cogeno EDTS properties.

+-------------------------------------------+------------------------------------------------+
+ :ref:`EDTS_DTS_ROOT` sub-directory        | Property/ usage                                |
+===========================================+================================================+
+ :file:`include`                           | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`                |
+-------------------------------------------+------------------------------------------------+
+ :file:`include` /dt-bindings              | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`                |
+-------------------------------------------+------------------------------------------------+
+ :file:`common`                            | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`                |
+-------------------------------------------+------------------------------------------------+
+ :ref:`EDTS_ARCH`                          | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`                |
+-------------------------------------------+------------------------------------------------+
+ :ref:`EDTS_ARCH`/:ref:`EDTS_ARCH_FLAVOUR` | :ref:`EDTS_DTS_PP_INCLUDE_DIRS`                |
+-------------------------------------------+------------------------------------------------+
+ :file:`bindings`                          | :ref:`EDTS_BINDINGS_DIRS`                      |
+-------------------------------------------+------------------------------------------------+

Use the Cogeno protobuf module with CMake
-----------------------------------------

The :ref:`cogeno.cmake` script searches the list of directories in the :ref:`EXTENSION_DIRS`
property for a :file:`proto` sub-directory.
If the directory exists it is added to the :ref:`PROTOBUF_INCLUDE_DIRS` property.

The protobuf sources (*.proto) shall be added to the dependencies of the source file that is
using the protobuf code database. The protobuf sources may either be given with absolute
path or with a path relative to the :file:`CMakeList.txt` directory.

The include directories that contain protobuf files to be imported by the protobuf sources,
and that are not listed in the :ref:`PROTOBUF_INCLUDE_DIRS` property, shall also be added to the
dependencies. The enclosing directories of the protobuf sources are automatically added.

:file:`CMakeList.txt`

::

    cogeno_sources('proto_user.c' DEPENDS proto/myproto.proto ../../general/proto)


Cogeno CMake properties
=======================

  - DEFINES
  - MODULES
  - TEMPLATES
  - EXTENSION_DIRS
  - CMAKE_CACHE
  - CMAKE_DEFINES
  - CONFIG_FILE
  - EDTS_ARCH
  - EDTS_ARCH_FLAVOUR
  - EDTS_DTS
  - EDTS_DTS_ROOT
  - EDTS_DTS_PP_DEFINES
  - EDTS_DTS_PP_INCLUDE_DIRS
  - EDTS_DTS_PP_SOURCES
  - EDTS_BINDINGS_DIRS
  - EDTS_BINDINGS_EXCLUDE
  - EDTS_BINDINGS_NO_DEFAULT
  - EDTS_DB
  - PROTOBUF_DB_DIR
  - PROTOBUF_SOURCES
  - PROTOBUF_INCLUDE_DIRS


Build with Zephyr and Cogeno
****************************

Zephyr uses the `CMake <https://cmake.org/>`_ build system with custom extensions.
`Build with CMake and Cogeno`_ also applies to Zephyr builds.

To use Cogeno you have to include :ref:`cogeno.cmake` in your project's :file:`CMakeList.txt` file.

The easiest way to get :ref:`cogeno.cmake` and all of Cogeno with Zephyr is to install
Cogeno as a Zephyr module.

:file:`west.yml`

::

    manifest:

      remotes:

        - name: gitlab_b0661
          url-base: https://gitlab.com/b0661

      projects:

        - name: cogeno
          remote: gitlab_b0661
          revision: master
          path: cogeno

Assure that on build the Cogeno module is processed before the modules that use it. If the sequence
created by `west --list` does not suite your needs explicitly set `ZEPHYR_MODULES` in your project.

:file:`CMakeList.txt`

::

    set(ZEPHYR_MODULES
        ${CMAKE_CURRENT_SOURCE_DIR}/../cogeno
        ...
    )

    include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)

In Zephyr the processing of source files is controlled by the `CMake <https://cmake.org/>`_
extension functions ``zephyr.._sources_cogeno..(..)`` or ``zephyr_..includes_cogeno..(..)``.
During build the source files are processed by Cogeno and the generated source files are written
to the CMake binary directory. The generated source files are added to the Zephyr sources.

A file that contains inline code generation has to be added to the project
by one of the following commands in a :file:`CMakeList.txt` file:

.. function:: zephyr_sources_cogeno(file [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_sources_cogeno_ifdef(ifguard file [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_sources_cogeno(file [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_sources_cogeno_ifdef(ifguard file [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_includes_cogeno(file.. [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_includes_cogeno_ifdef(ifguard file.. [COGENO_DEFINES defines..] [DEPENDS target.. file..])


Use Cogeno modules with Zephyr
==============================

Use the Cogeno EDTS module with Zephyr
--------------------------------------

The project device tree file is processed twice by gen_defines.py of Zephyr and cogeno.edts() of Cogeno.

Usually the both should work on the same properties - but in some rare cases
gen_defines.py of Zephyr may not understand certain properties because

  - the property is not foreseen for extraction
  - or the include directory for an include file for :ref:`device tree preprocessing <devicetree-build-flow-figure>`
    provided to the EDTS module is not provided to gen_defines.py (``edts`` vs. ``dts``)
  - or a binding file provided to the EDTS module is different from the one provided to gen_defines.py


In these cases you can use defines to exclude parts of the device tree file from processing
by gen_defines.py. ``COGENO_EDTS`` is only defined if :ref:`device tree preprocessing <devicetree-build-flow-figure>`
is done on behalf of Cogeno. If you need a more fine grained control you should add a define in the
:file:`cogeno/<extension>.py` Cogeno extension module of your project or Zephyr module
(see :ref:`Search for Cogeno extensions` and :ref:`Script Cogeno extension modules`):

::

    import cogeno
    cogeno.option_argv_append('--edts:dts-pp-defines', "MY_DTS_DEFINE=1")

In the project device tree file you can control the DTS preprocessing in the usual way:

::

    #if defined(MY_DTS_DEFINE)
    #include <dt-bindings/my_special_driver/my_special_driver.h>
    #endif

    &my_special_driver {
    #if defined(MY_DTS_DEFINE)
            clock-output-names = MY_SPECIAL_DRIVER_CLOCK_1 MY_SPECIAL_DRIVER_CLOCK_2
    #endif
    };


Build with ESP-IDF/ MDF and Cogeno
**********************************

Cogeno can be integrated as a component into
`ESP32 <https://www.espressif.com/en/products/hardware/esp32/overview>`_ projects using the
`ESP-IDF <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/>`_ or
`ESP-MDF <https://docs.espressif.com/projects/esp-mdf/en/latest/index.html>`_ framework and the
`CMake <https://cmake.org/>`_ build system. `Build with CMake and Cogeno`_ also applies to
ESP-IDF/ ESP-MDF builds.

To create the Cogeno component make Cogeno a git submodule within the project's components directory.

::

    cd <project>/components
    git submodule add https://gitlab.com/b0661/cogeno

Source files of components may use inline code generation. To generate the inline code the
component sources have to be marked using the ``cogeno_sources()`` command in the respective
:file:`CMakeList.txt` file.

``cogeno_sources()`` adds the generated source files to ``COGENO_COMPONENT_SRCS``. It also adds
include directories to ``COGENO_COMPONENT_INCLUDE_DIRS``. The ``COGENO_COMPONENT_SRCS`` and the
``COGENO_COMPONENT_INCLUDE_DIRS`` have to be registered for the component.

Components should have the Cogeno component given in their ``PRIV_REQUIRES`` property.

::

    if(NOT CMAKE_BUILD_EARLY_EXPANSION)
        cogeno_sources(${COMPONENT_NAME} inline_code_filea.c inline_code_fileb.c ...)
    endif()
    idf_component_register(
        SRCS ${COGENO_COMPONENT_SRCS} ...
        PRIV_REQUIRES cogeno ...
        INCLUDE_DIRS ${COGENO_COMPONENT_INCLUDE_DIRS} ...)


Use Cogeno modules with ESP-IDF and ESP-MDF
===========================================

Use the Cogeno EDTS module with ESP-IDF and ESP-MDF
---------------------------------------------------

To use the Cogeno Extended Device Tree Specification (EDTS) module your project has to
provide the top level device tree specification :file:`edts/project.dts`. The :file:`project.dts`
file should include device tree source files from the main component
and other components provided in their respective :file:`edts` directory.

:file:`edts/project.dts`

::

    #include <boards/esp32/esp32.dts>

A special component holds most of the generic device tree source files for inclusion:

- edts (see examples/esp_idf/edts)


cogeno.cmake
************

.. literalinclude:: ../../examples/cmake/cogeno.cmake
    :language: cmake
    :lines: 4-

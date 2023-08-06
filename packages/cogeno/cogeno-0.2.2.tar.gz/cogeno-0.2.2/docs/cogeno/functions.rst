..
    Copyright (c) 2004-2015 Ned Batchelder
    SPDX-License-Identifier: MIT
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_functions:

Code generation functions
#########################

The ``cogeno`` module provides the core functions for inline
code generation. It encapsulates all the functions to retrieve information
(options, device tree properties, CMake variables, config properties) and
to output the generated code.

The ``cogeno`` module is automatically imported by all code snippets. No
explicit import is necessary.

.. note::
    The ``cogeno`` module provides the public functions of the code generator
    ``Mixin`` classes as cogeno functions. You can simply write:

        **cogeno.func(...)**

    The mixin class function cogeno.xxx.XxxMixin.func(self, ...) is not directly
    available to code snippets.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

Output
******

**cogeno.out(*args)**
---------------------

.. doxygenfunction:: cogeno::output::OutputMixin::out()
    :project: cogeno

**cogeno.outl(*args)**
----------------------

.. doxygenfunction:: cogeno::output::OutputMixin::outl()
    :project: cogeno

**cogeno.out_insert(insert_file, *args)**
-----------------------------------------

.. doxygenfunction:: cogeno::output::OutputMixin::out_insert()
    :project: cogeno

Output filters
--------------

**cogeno.OutputFilterTrimBlankLines()**
=======================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterTrimBlankLines
    :project: cogeno

**cogeno.OutputFilterTrimDedent()**
===================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterDedent
    :project: cogeno

**cogeno.OutputFilterLineNumbers()**
====================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterLineNumbers
    :project: cogeno

**cogeno.OutputFilterStartAt()**
================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterStartAt
    :project: cogeno

**cogeno.OutputFilterStopAt()**
===============================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterStopAt
    :project: cogeno

**cogeno.OutputFilterReplace()**
================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterReplace
    :project: cogeno

**cogeno.OutputFilterReSub()**
==============================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterReSub
    :project: cogeno

**cogeno.OutputFilterTemplateSubstitude()**
===========================================

.. doxygenclass:: cogeno::output::OutputMixin::OutputFilterTemplateSubstitude
    :project: cogeno

The cogeno module also provides a set of convenience functions:


Code generator
**************

**cogeno.cogeno_state()**
------------------------------

.. doxygenfunction:: cogeno::generator::CodeGenerator::cogeno_state()
    :project: cogeno


Code generation module import
*****************************

**cogeno.import_module(name)**
------------------------------

.. doxygenfunction:: cogeno::importmodule::ImportMixin::import_module()
    :project: cogeno

See :ref:`cogeno_modules` for the available modules.


Template file inclusion
***********************

**cogeno.out_include(include_file)**
------------------------------------

.. doxygenfunction:: cogeno::include::IncludeMixin::out_include()
    :project: cogeno

**cogeno.guard_include()**
--------------------------

.. doxygenfunction:: cogeno::include::IncludeMixin::guard_include()
    :project: cogeno


Error handling
**************

**cogeno.error(msg [, frame_index=0] [, snippet_lineno=0])**
-------------------------------------------------------------

.. doxygenfunction:: cogeno::error::ErrorMixin::error()
    :project: cogeno


Log output
**********

**cogeno.log(message, message_type=None, end="\n", logonly=True)**
------------------------------------------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::log()
    :project: cogeno

**cogeno.msg(message)**
-----------------------

.. doxygenfunction:: cogeno::log::LogMixin::msg()
    :project: cogeno

**cogeno.warning(message)**
---------------------------

.. doxygenfunction:: cogeno::log::LogMixin::warning()
    :project: cogeno

**cogeno.prout(message, end="\n")**
-----------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::prout()
    :project: cogeno

**cogeno.prerr(message, end="\n")**
-----------------------------------

.. doxygenfunction:: cogeno::log::LogMixin::prerr()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` for how to provide the path to the file used for
logging.


Lock access
***********

**cogeno.lock()**
-----------------

.. doxygenfunction:: cogeno::lock::LockMixin::lock()
    :project: cogeno

**cogeno.lock_timeout()**
-------------------------

.. doxygenfunction:: cogeno::lock::LockMixin::lock_timeout()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` for how to provide the path to the file used for
locking.

Lock object
-----------

.. doxygenfunction:: cogeno::filelock::BaseFileLock::acquire()
    :project: cogeno

.. doxygenfunction:: cogeno::filelock::BaseFileLock::release()
    :project: cogeno

.. doxygenfunction:: cogeno::filelock::BaseFileLock::is_locked()
    :project: cogeno


Options
*******

**cogeno.option()**
-------------------

.. doxygenfunction:: cogeno::options::OptionsMixin::option()
    :project: cogeno

**cogeno.options_add_argument(*args, **kwargs)**
------------------------------------------------

.. doxygenfunction:: cogeno::options::OptionsMixin::options_add_argument()
    :project: cogeno


Path functions
**************

**cogeno.path_walk(top, topdown = False, followlinks = False)**
---------------------------------------------------------------

.. doxygenfunction:: cogeno::paths::PathsMixin::path_walk()
    :project: cogeno

**cogeno.rmtree(top)**
----------------------

.. doxygenfunction:: cogeno::paths::PathsMixin::rmtree()
    :project: cogeno

**cogeno.find_template_files(top, marker, suffix='.c')**
--------------------------------------------------------

.. doxygenfunction:: cogeno::paths::PathsMixin::find_template_files()
    :project: cogeno


Standard streams
****************

**cogeno.set_standard_streams(self, stdout=None, stderr=None)**
---------------------------------------------------------------

.. doxygenfunction:: cogeno::redirectable::RedirectableMixin::set_standard_streams()
    :project: cogeno


Standard Modules - CMake
************************

**cogeno.cmake_variable(variable_name [, default="<unset>"])**
--------------------------------------------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::cmake_variable()
    :project: cogeno

**cogeno.cmake_cache_variable(variable_name [, default="<unset>"])**
--------------------------------------------------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::cmake_cache_variable()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide CMake
variables to cogeno.


Standard Modules - config
*************************

**cogeno.config_properties()**
------------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::config_properties()
    :project: cogeno

**cogeno.config_property(property_name [, default="<unset>"])**
---------------------------------------------------------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::config_property()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide config
variables to cogeno.


Standard Modules - Extended Device Tree Database
************************************************

**cogeno.edts()**
-----------------

.. doxygenfunction:: cogeno::stdmodules::StdModulesMixin::edts()
    :project: cogeno

See :ref:`cogeno_invoke_cogeno` and :ref:`cogeno_build` for how to provide all
files to enable cogeno to build the extended device tree database.


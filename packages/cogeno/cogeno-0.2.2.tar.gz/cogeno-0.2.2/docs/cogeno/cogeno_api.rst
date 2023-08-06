..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_api:

Cogeno API
##########

.. module:: cogeno
    :synopsis: Inline code generator

`cogeno` is a Python module that provides access to the public functions
of the class: ``CodeGenerator`` and the sub-classes of it. See
:ref:`cogeno_functions` for a description of all ``cogeno`` module's functions.

The interfaces listed hereafter are the internal interfaces of Cogeno.
The Cogeno ``CodeGenerator`` is made of a set of ``Mixin`` classes that
bundle specific generator functionality. The ``CodeGenerator`` stores it´s
states in ``Context`` class objects.

.. contents::
    :depth: 2
    :local:
    :backlinks: top

:mod:`CodeGenerator`
====================

.. doxygenclass:: cogeno::generator::CodeGenerator
    :project: cogeno
    :members:
    :undoc-members:

The ``CodeGenerator`` class includes (sub-classes) several ``mixin`` classes:

:mod:`ContextMixin`
-------------------

.. doxygenclass:: cogeno::context::ContextMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`ErrorMixin`
-----------------

.. doxygenclass:: cogeno::error::ErrorMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`ImportMixin`
------------------

.. doxygenclass:: cogeno::importmodule::ImportMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`IncludeMixin`
-------------------

.. doxygenclass:: cogeno::include::IncludeMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`InlineGenMixin`
---------------------

.. doxygenclass:: cogeno::inlinegen::InlineGenMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`Jinja2GenMixin`
---------------------

.. doxygenclass:: cogeno::jinja2gen::Jinja2GenMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`LockMixin`
----------------

.. doxygenclass:: cogeno::lock::LockMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`LogMixin`
---------------

.. doxygenclass:: cogeno::log::LogMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`OptionsMixin`
-------------------

.. doxygenclass:: cogeno::options::OptionsMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`OutputMixin`
-------------------

.. doxygenclass:: cogeno::output::OutputMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`PathsMixin`
-------------------

.. doxygenclass:: cogeno::paths::PathsMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`PyGenMixin`
-------------------

.. doxygenclass:: cogeno::pygen::PyGenMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`RedirectableMixin`
-------------------

.. doxygenclass:: cogeno::redirectable::RedirectableMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`StdModulesMixin`
----------------------

.. doxygenclass:: cogeno::stdmodules::StdModulesMixin
    :project: cogeno
    :members:
    :undoc-members:

:mod:`Context`
==============

.. doxygenclass:: cogeno::context::Context
    :project: cogeno
    :members:
    :undoc-members:

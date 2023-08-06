..
    Copyright (c) 2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_extensions:

Cogeno extensions
#################

Search for Cogeno extensions
============================

On invocation Cogeno searches the list of directories given in the ``--extensions DIR [DIR...]``
option for Cogeno extensions.

If a :file:`cogeno/<extension_name>.py` Python module is found in an extension directory
the module is imported by Cogeno. All Python commands within the `<extension_name>` module
are executed. Scripts and script snippets can import the module by it's name `<extension_name>`.

There may be several modules within the :file:`cogeno` directory. All of them will be imported.


Script Cogeno extension modules
===============================

The :file:`cogeno/<extension_name>.py` file  is a regular Python module. All of Python can be used.

Add options to the Cogeno invocation
------------------------------------

A typical use case is to add further options to the Cogeno invocation:

::

    from pathlib import Path

    import cogeno

    component_path = Path(__file__).parent.parent

    cogeno.options_argv_append('--edts:dts-pp-defines', 'MY_EXTENSION=1')
    cogeno.options_argv_append('--edts:dts-pp-include-dirs', str(component_path.joinpath('include')))
    cogeno.options_argv_append('--edts:bindings-dirs', str(component_path.joinpath('edts/bindings')))
    cogeno.options_argv_append('--protobuf:sources', str(component_path.joinpath('proto/myproto.proto')))

Manage extensions hirarchy with Kconfig variables
-------------------------------------------------

Another use case is to have a hirarchy of extensions possibly controlled by Kconfig variables.

Toplevel <extension directory>/:file:`cogeno/<toplevel_name>.py` file:

::

    from pathlib import Path

    import cogeno

    component_path = Path(__file__).parent.parent

    if cogeno.config_property('CONFIG_MY_SUB_EXTENSION', None):
        cogeno.import_extensions(component_path.joinpath('whatever/sub-extension'))

    ...

Sublevel <extension directory/whatever/sub-extension>/:file:`cogeno/<sub_extension_name>.py` file:

::

    from pathlib import Path

    import cogeno

    component_path = Path(__file__).parent.parent

    cogeno.options_argv_append('--edts:dts-pp-defines', 'MY_SUB_EXTENSION=1')

    ...
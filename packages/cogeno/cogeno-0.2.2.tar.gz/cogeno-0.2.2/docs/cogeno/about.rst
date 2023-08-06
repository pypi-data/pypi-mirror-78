..
    Copyright (c) 2004-2015 Ned Batchelder
    SPDX-License-Identifier: MIT
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_about:

About Cogeno
############

For some repetitive or parameterized coding tasks, it's convenient to
use a code generating tool to build code fragments, instead of writing
(or editing) that source code by hand.

Cogeno, the inline code generation tool, processes
`Python 3 <https://www.python.org>`_ or `Jinja2 <http://jinja.pocoo.org/>`_
script "snippets" inlined in your source files. It can also access CMake build
parameters and device tree information to generate source code automatically
tailored and tuned to a specific project configuration.

Cogeno can be used, for example, to generate source code that creates
and fills data structures, adapts programming logic, creates
configuration-specific code fragments, and more.

About Cogeno scripts
********************

Script snippets that are inlined in a source file are used as code generators.
The tool to scan the source file for the script snippets and process them is
Cogeno. Cogeno and part of this documentation is based on
`Cog <https://nedbatchelder.com/code/cog/index.html>`_ from Ned Batchelder.

The inlined script snippets can contain any `Python 3 <https://www.python.org>`_
or `Jinja2 <http://jinja.pocoo.org/>`_ code, they are regular scripts.

All Python snippets in a source file and all Python snippets of
included template files are treated as a python script with a common set of
global Python variables. Global data created in one snippet can be used in
another snippet that is processed later on. This feature could be used, for
example, to customize included template files.

Jinja2 snippets provide a - compared to Python - simplified script language.

An inlined script snippet can always access the cogeno module. The cogeno
module encapsulates and provides all the functions to retrieve information
(options, devicetree properties, CMake variables, config properties) and to
output the generated code.

Cogeno transforms files in a very simple way: it finds snippets of script code
embedded in them, executes the script code, and places its output combined with
the original file into the generated file. The original file can contain
whatever text you like around the script code. It will usually be source code.

For example, if you run this file through cogeno:

::

    /* This is my C file. */
    ...
    /**
     * @code{.cogeno.py}
     * fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
     * for fn in fnames:
     *     cogeno.outl(f'void {fn}();')
     * @endcode{.cogeno.py}
     */
    /** @code{.cogeno.ins}@endcode */
    ...

it will come out like this:

::

    /* This is my C file. */
    ...
    /**
     * @code{.cogeno.py}
     * fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
     * for fn in fnames:
     *     cogeno.outl(f'void {fn}();')
     * @endcode{.cogeno.py}
     */
    void DoSomething();
    void DoAnotherThing();
    void DoLastThing();
    /** @code{.cogeno.ins}@endcode */
    ...

Lines with ``@code{.cogeno.py}`` or ``@code{.cogeno.ins}@endcode`` are marker lines.
The lines between ``@code{.cogeno.py}`` and ``@endcode{.cogeno.py}`` are the
generator Python code. The lines between ``@endcode{.cogeno.py}`` and
``@code{.cogeno.ins}@endcode`` are the output from the generator.

When Cogeno runs, it discards the last generated Python output, executes the
generator Python code, and writes its generated output into the file. All text
lines outside of the special markers are passed through unchanged.

The Cogeno marker lines can contain any text in addition to the marker tokens.
This makes it possible to hide the generator Python code from the source file.

In the sample above, the entire chunk of Python code is a C comment, so the
Python code can be left in place while the file is treated as C code.


About Cogeno extensions
***********************

On invocation Cogeno scans a list of given directories for extension modules
and imports the modules. An extension module may add additional options to the
Cogeno invocation or may provide other information specific to the
extension directory. The :ref:`cogeno_extensions` are available to the script snippets.


About Cogeno modules
********************

Cogeno includes several :ref:`cogeno_modules` to support specific code generation tasks.

* :ref:`cogeno_modules_ccode`
* :ref:`cogeno_modules_cmake`
* :ref:`cogeno_modules_config`
* :ref:`cogeno_modules_edts`
* :ref:`cogeno_modules_protobuf`
* :ref:`cogeno_modules_rstcode`
* :ref:`cogeno_modules_zephyr`

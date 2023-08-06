..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_modules:

Cogeno modules
##############

Cogeno modules provide supporting functions for code generation.

Some modules have to be imported to gain access to the module's functions
and variables. The standard modules are accessible by convenience functions.

 ::

    /* This file uses modules. */
    ...
    /**
     * @code{.cogeno.py}
     * cogeno.import_module('my_special_module')
     * my_special_module.do_everything():
     * @endcode{.cogeno.py}
     */
    /** @code{.cogeno.ins}@endcode */
    ...

.. toctree::
   :maxdepth: 1

   modules/ccode/ccode
   modules/cmake/cmake
   modules/config/config
   modules/edts/edts
   modules/protobuf/protobuf
   modules/rstcode/rstcode
   modules/zephyr/zephyr





..
    Copyright (c) 2018..2020 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_invoke_cogeno:

Invoking Cogeno
###############

Synopsis
********

cogeno [OPTIONS]

Description
***********

Cogeno transforms files in a very simple way: it finds chunks of script code
embedded in them, executes the script code, and places its output combined with
the original file content into the generated file. It supports Python and Jinja2
scripts.

Options
*******

The following options are understood:

``-h, --help``
    show this help message and exit

``-x, --delete-code``
    Delete the generator code from the output file.

``-w, --warn-empty``
    Warn if a file has no generator code in it.

``-n ENCODING, --encoding ENCODING``
    Use ENCODING when reading and writing files.

``-U, --unix-newlines``
    Write the output with Unix newlines (only LF line-endings).

``-D DEFINE, --define DEFINE``
    Define a global string available to your generator code.

``-m DIR [DIR ...], --modules DIR [DIR ...]``
    Use modules from modules DIR. We allow multiple

``-t DIR [DIR ...], --templates DIR [DIR ...]``
    Use templates from templates DIR. We allow multiple

``-e DIR [DIR ...], --extensions DIR [DIR ...]``
    Import extensions from extensions DIR. We allow multiple

``-i FILE, --input FILE``
    Get the input from FILE.

``-o FILE, --output FILE``
    Write the output to FILE. "-" indicates stdout.

``--output-sanitize-suffix``
    Sanitize the suffix of the output file. Remove typical
    template suffixes.

``-l FILE, --log FILE``
    Log to FILE.

``-k FILE, --lock FILE``
    Use lock FILE for concurrent runs of cogeno.

``--base``
    Return the base directory of cogeno. Other options are ignored.

Additional options are related to :ref:`cogeno_modules`.

``--cmake:cache FILE``
    Use CMake variables from CMake cache FILE.

``--cmake:define [defxxx=valyyy ...]``
    Define CMake variables to your generator code.

``--config:db FILE``
    Write or read config database to/ from FILE.

``--config:file FILE``
    Read configuration variables from this FILE.

``--config:kconfig-file FILE``
    Top-level Kconfig FILE (default: Kconfig).

``--config:kconfig-srctree DIR``
    Kconfig files are looked up relative to the srctree DIR (unless absolute paths
    are used), and .config files are looked up relative to the srctree DIR if they
    are not found in the current directory.

``--config:kconfig-defines DEFINE [DEFINE ...]``
    Define variable to Kconfig. We allow multiple.

``--config:inputs FILE [FILE ...]``
    Read configuration file fragment from FILE. We allow multiple.

``--edts:bindings-dirs DIR [DIR ...]``
    Use bindings from bindings DIR for device tree extraction. We allow multiple.

``--edts:bindings-exclude [DIR ...] [FILE ...]``
    Exclude bindings DIR or FILE from usage for device tree extraction. We allow multiple.

``--edts:bindings-no-default``
    Do not add EDTS database's generic bindings to bindings by default.

``--edts:db FILE``
    Write or read EDTS database to/ from FILE.

``--edts:dts FILE``
    Write (see dts-pp-sources) or read device tree specification to/ from this FILE.

``--edts:dts-pp-sources FILE [FILE ...]``
    Generate the DTS file by pre-processing the DTS source FILE(s).

``--edts:dts-pp-include-dirs DIR [DIR ...]``
    Define include DIR(s) to pre-processor.

``--edts:dts-pp-defines DEFINE [DEFINE ...]``
    DEFINE variable to pre-processor.

``--protobuf:db-dir DIR``
    Write or read protocol buffer code databases to/ from DIR.

``--protobuf:sources FILE [FILE ...]``
    The *.proto source FILE(s) to generate the protocol buffer code for.

``--protobuf:include-dirs DIR [DIR ...]``
    Search for *.proto import files in the protocol buffer include DIR(s).

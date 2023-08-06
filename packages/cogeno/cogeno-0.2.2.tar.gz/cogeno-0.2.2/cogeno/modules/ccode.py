# Copyright (c) 2019 Nordic Semiconductor ASA
# Copyright (c) 2019 Linaro Limited
# Copyright (c) 2018..2019 UAVCAN Development Team  <uavcan.org>
# Copyright (c) 2018..2020 Bobby Noelte.
# SPDX-License-Identifier: BSD-3-Clause

# Parts of the code are taken from several sources:
# - https://github.com/UAVCAN/nunavut
#   C_RESERVED_PATTERNS, VariableNameEncoder, ...
#   SPDX-License-Identifier: MIT
# -

import functools
import re

import cogeno

# Taken from https://en.cppreference.com/w/c/language/identifier
# cspell: disable
C_RESERVED_PATTERNS = frozenset(map(functools.partial(re.compile, flags=0), [
    r'^(is|to|str|mem|wcs|atomic_|cnd_|mtx_|thrd_|tss_|memory_|memory_order_)[a-z]',
    r'^u?int[a-zA-Z_0-9]*_t',
    r'^E[A-Z0-9]+',
    r'^FE_[A-Z]',
    r'^U?INT[a-zA-Z_0-9]*_(MAX|MIN|C)',
    r'^(PRI|SCN)[a-zX]',
    r'^LC_[A-Z]',
    r'^SIG_?[A-Z]',
    r'^TIME_[A-Z]',
    r'^ATOMIC_[A-Z]'
]))

C_RESERVED_TOKEN_START_PATTERN = re.compile(r'(^__)|(^_[A-Z])')

##
# @brief Converts 's' to a form suitable for (part of) an identifier.
#
# @param s string
def str2ident(s):
    identifier = s.replace("-", "_") \
                  .replace(",", "_") \
                  .replace("@", "_") \
                  .replace("/", "_") \
                  .replace(".", "_") \
                  .replace("+", "_")
    for pattern in C_RESERVED_PATTERNS:
        if pattern.match(identifier):
            # identifier is reserved
            identifier += '_' + identifier[-1:]
    if C_RESERVED_TOKEN_START_PATTERN.match(identifier):
        # identifier is reseved for C internal use
        identifier = 'x_' + identifier # @TODO better solution
    return identifier

##
# @brief Converts 's' to an uppercase form suitable for (part of) an identifier.
#
# Converts to upper case.
#
# @param s string
def str2ident_uc(s):
    return str2ident(s.upper())

##
# @brief Converts 's' to a lowercase form suitable for (part of) an identifier.
#
# Converts to upper case.
#
# @param s string
def str2ident_lc(s):
    return str2ident(s.lower())

##
# @brief transform string to a valid C preprocessor label
def to_define_label(value: str) -> str:
    return str2ident_uc(value)

##
# @brief Produces a valid C identifier for a given object.
def to_identifier(instance) -> str:
    if hasattr(instance, 'name'):
        raw_name = str(instance.name)  # type: str
    else:
        raw_name = str(instance)

    return str2ident_lc(raw_name)

##
# @brief Write #if guard for config property to output.
#
# If there is a configuration property of the given name the property value
# is used as guard value, otherwise it is set to 0.
#
# @param property_name Property name
def outl_config_guard(property_name):
    is_config = cogeno.config_property(property_name, 0)
    cogeno.outl("#if {} // Guard({}) {}".format(
        is_config, is_config, property_name))

##
# @brief Write #endif guard for config property to output.
#
# This is the closing command for outl_guard_config().
#
# @param property_name Property name
def outl_config_unguard(property_name):
    is_config = cogeno.config_property(property_name, 0)
    cogeno.outl("#endif // Guard({}) {}".format(is_config, property_name))


##
# @brief Write 's' as a comment.
#
# @param s string, is allowed to have multiple lines.
# @param blank_before True adds a blank line before the comment.
def out_comment(s, blank_before=True):
    if blank_before:
        cogeno.outl("")

    if "\n" in s:
        # Format multi-line comments like
        #
        #   /*
        #    * first line
        #    * second line
        #    *
        #    * empty line before this line
        #    */
        res = ["/*"]
        leading = True
        for line in s.splitlines():
            # Avoid leading empty lines
            if leading:
                if line.strip() == '':
                    continue
                leading = False
            # Avoid an extra space after '*' for empty lines. They turn red in
            # Vim if space error checking is on, which is annoying.
            res.append(" *" if not line.strip() else " * " + line)
        res.append(" */")
        cogeno.outl("\n".join(res))
    else:
        # Format single-line comments like
        #
        #   /* foo bar */
        cogeno.out("/* ", s, " */")


##
# @brief Writes an overview comment with misc. info about EDTS.
def out_edts_comment_overview():
    edts = cogeno.edts()
    bindings_dirs = ""
    for binding_dir in edts.bindings_dirs():
        bindings_dirs += "  {}\n".format(binding_dir)
    dependency_order = edts.device_ids_by_dependency_order()
    dependency_ordinals = ""
    ordinal = 0
    while ordinal < len(dependency_order):
        device_id = dependency_order[ordinal]
        if device_id is None:
            device_id = "<not activated>"
        dependency_ordinals += "  {}: {}\n".format(ordinal, device_id)
        ordinal += 1

    s = f"""\
DTS input file:
  {edts.dts_path()}

Directories with bindings:
{bindings_dirs}

Devices in dependency order (ordinal and path):
{dependency_ordinals}
"""

    out_comment(s, blank_before=False)


# Writes a comment describing 'device'
def out_edts_comment_device(device_id):
    edts = cogeno.edts()

    s = f"""\
Devicetree node:
  {edts.device_property(device_id, 'path')}
"""

    out_comment(s)

##
# @brief Write EDTS database properties as C defines.
#
# @param prefix Define label prefix. Default is 'EDT_'.
def out_edts_defines(prefix = 'EDT_'):
    out_edts_comment_overview()
    cogeno.outl("")

    out_comment("Aliases")
    cogeno.outl("")
    for alias, alias_device_id in cogeno.edts().aliases().items():
        define_label = to_define_label("{}ALIAS_{}".format(prefix, alias))
        define_value = to_define_label(prefix + alias_device_id)
        cogeno.outl("#define {}\t{}".format(define_label, define_value))

    out_comment("Compatibles")
    cogeno.outl("")
    for compatible, compatible_devices in cogeno.edts().compatibles().items():
        for index, compatible_ref in compatible_devices.items():
            define_label = to_define_label("{}COMPATIBLE_{}_{}".format(
                prefix, compatible, index))
            if index == 'count':
                define_value = compatible_ref
            else:
                define_value = to_define_label(prefix + compatible_ref)
            cogeno.outl("#define {}\t{}".format(define_label, define_value))

    out_comment("Names")
    cogeno.outl("")
    for device_id in cogeno.edts()['devices']:
        name = cogeno.edts().device_name_by_id(device_id)
        define_label = to_define_label("{}NAME_{}".format(prefix, name))
        define_value = to_define_label(prefix + device_id)
        cogeno.outl("#define {}\t{}".format(define_label, define_value))
        device_name = cogeno.edts().device_property(device_id, 'name')
        if device_name != name:
            define_label = to_define_label("{}NAME_{}".format(prefix, device_name))
            cogeno.outl("#define {}\t{}".format(define_label, define_value))

    out_comment("Dependencies")
    cogeno.outl("")
    dependency_order = cogeno.edts().device_ids_by_dependency_order()
    ordinal = 0
    while ordinal < len(dependency_order):
        device_id = dependency_order[ordinal]
        if not device_id is None:
            define_label = to_define_label("{}DEPEND_{}".format(prefix, ordinal))
            define_value = to_define_label(prefix + device_id)
            cogeno.outl("#define {}\t{}".format(define_label, define_value))
        ordinal += 1

    out_comment("Devices")
    cogeno.outl("")
    for device_id in cogeno.edts()['devices']:
        properties = cogeno.edts().device_properties_flattened(device_id)
        out_edts_comment_device(device_id)
        cogeno.outl("")
        for prop_path, prop_value in properties.items():
            define_label = to_define_label("{}{}_{}".format(prefix, device_id,
                                                      prop_path))
            if prop_value in cogeno.edts()['devices'] or prop_value == '/':
                # Property value is a device-id
                prop_value = to_define_label("{}{}".format(prefix, prop_value))
            cogeno.outl("#define {}\t{}".format(define_label, prop_value))

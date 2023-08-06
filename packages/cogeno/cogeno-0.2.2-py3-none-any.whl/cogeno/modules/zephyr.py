# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import re
from string import Template

import cogeno
cogeno.import_module('ccode')


##
# @brief Template for device definition
#
# The template works on the following placeholders:
# - ${device-name}
# - ${driver-name}
# - ${device-config}
# - ${device-api}
# - ${device-data}
# - ${device-level}
# - ${device-prio}
# - ${device-init}
# - ${device-pm-control}
#
# @note See Zephyr include/device.h DEVICE_DEFINE
_device_define_tmpl = """\
#if CONFIG_DEVICE_POWER_MANAGEMENT
static struct device_pm __pm_${device-name} __used
\t= {\n
\t.usage = ATOMIC_INIT(0),
\t.lock = _Z_SEM_INITIALIZER(__pm_${device-name}.lock, 1, 1),
\t.signal = K_POLL_SIGNAL_INITIALIZER(__pm_${device-name}.signal),
\t.event = K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
\t\tK_POLL_MODE_NOTIFY_ONLY,
\t\t&__pm_${device-name}.signal),
};
#endif
static Z_DECL_ALIGN(struct device) __device_${device-name} __used
\t__attribute__((__section__(\".device_${device-level}\" STRINGIFY(${device-prio})))) = {
\t.name = "${driver-name}",
\t.config = (&${device-config}),
\t.api = (&${device-api}),
\t.data = (&${device-data}),
#if CONFIG_DEVICE_POWER_MANAGEMENT
\t.device_pm_control = (${device-pm-control}),
\t.pm  = &__pm_${device-name},
#endif
};
static const Z_DECL_ALIGN(struct init_entry) __init_${device-name} __used
\t__attribute__((__section__(\".init_${device-level}\" STRINGIFY(${device-prio})))) = {
\t.init = ${device-init},
\t.dev = &__device_${device-name},
};
"""

##
# Aliases for EDTS property paths.
_property_path_aliases = {
    'reg/0/address' : 'reg/address',
    'reg/0/size' : 'reg/size',
}

##
# @brief Converts 's' to a form suitable for (part of) an identifier
#
# @param s string
# @return identifier
def str2ident(s):

    return s.replace("-", "_") \
            .replace(",", "_") \
            .replace("@", "_") \
            .replace("/", "_") \
            .replace(".", "_") \
            .replace("+", "_") \
            .upper()

##
# @brief Get device name from device id
#
# @param device_id device id
# @return device name
def device_name_by_id(device_id):
    device_name = str2ident(cogeno.edts().device_name_by_id(device_id)
                                         .strip('"'))
    return device_name.lower()

##
# @brief Declare a single device instance.
#
# Generate device instances code for a device instance that:
#
# - match the driver names that
# - is activated ('status' = 'ok') in the board device tree file and that is
# - configured by Kconfig.
#
# The device name is derived from the device tree label property or - if not
# avalable - the node name.
#
# @param device_config_symbol
#   A configuration symbol for device instantiation.
#   (e.g. 'CONFIG_SPI_0')
# @param driver_name
#   The name this instance of the driver can be looked up from
#   user mode with device_get_binding().
# @param device_init
#   Address to the init function of the driver.
# @param device_pm_control
#   The device power management function
# @param device_level
#   The initialization level at which configuration occurs.
#   Must be one of the following symbols, which are listed in the order
#   they are performed by the kernel:
#   \n
#   \li PRE_KERNEL_1: Used for devices that have no dependencies, such as those
#   that rely solely on hardware present in the processor/SOC. These devices
#   cannot use any kernel services during configuration, since they are not
#   yet available.
#   \n
#   \li PRE_KERNEL_2: Used for devices that rely on the initialization of devices
#   initialized as part of the PRE_KERNEL_1 level. These devices cannot use any
#   kernel services during configuration, since they are not yet available.
#   \n
#   \li POST_KERNEL: Used for devices that require kernel services during
#   configuration.
#   \n
#   \li POST_KERNEL_SMP: Used for initialization objects that require kernel
#   services during configuration after SMP initialization
#   \n
#   \li APPLICATION: Used for application components (i.e. non-kernel components)
#   that need automatic configuration. These devices can use all services
#   provided by the kernel during configuration.
# @param device_prio
#   The initialization priority of the device, relative to
#   other devices of the same initialization level. Specified as an integer
#   value in the range 0 to 99; lower values indicate earlier initialization.
#   Must be a decimal integer literal without leading zeroes or sign (e.g. 32),
#   or an equivalent symbolic name (e.g. \#define MY_INIT_PRIO 32 or e.g.
#   CONFIG_KERNEL_INIT_PRIORITY_DEFAULT + 5).
# @param device_api
#   Identifier of the device api.
#   (e.g. 'spi_stm32_driver_api')
# @param device_info
#   Device info template for device driver config, data and interrupt
#   initialisation.
# @param device_defaults
#   Device default property values. `device_defaults` is a dictionary of
#   property path : property value (e.g. { 'label' : 'My default label' }).
# @return True if device is declared, False otherwise
def device_declare_single(device_config_symbol,
                          driver_name,
                          device_init,
                          device_pm_control,
                          device_level,
                          device_prio,
                          device_api,
                          device_info,
                          device_defaults = {}):
    device_configured = cogeno.config_property(device_config_symbol, '<not-set>')
    if device_configured == '<not-set>' or device_configured[-1] == '0':
        # Not configured - do not generate
        #
        # The generation decision must be taken by cogeno here
        # (vs. #define CONFIG_xxx) to cope with the following situation:
        #
        # If config is not set the device may also be not activated in the
        # device tree. No device tree info is available in this case.
        # An attempt to generate code without the DTS info
        # will lead to an exception for a valid situation.
        ccode.out_comment(f"!!! '{driver_name}' not configured '{device_config_symbol}'!!!")
        return False

    edts = cogeno.edts()
    device_id = edts.device_id_by_name(driver_name)
    if device_id is None:
        # this should not happen
        cogeno.error("Did not find driver name '{}'.".format(driver_name))

    # Presets for local mapping this device data to template
    presets = device_defaults
    presets['device-init'] = device_init
    presets['device-pm-control'] = device_pm_control
    presets['device-level'] = device_level
    presets['device-prio'] = device_prio
    presets['device-api'] = device_api
    presets['device-config-symbol'] = device_config_symbol
    # Presets for local mapping of specific device declaration vars/ constants
    device_name = device_name_by_id(device_id)
    driver_name = driver_name.strip('"')
    presets['device-name'] = device_name
    presets['driver-name'] = driver_name
    presets['device-data'] = "{}_data".format(device_name)
    presets['device-config'] = "{}_config".format(device_name)
    presets['device-config-irq'] = "{}_config_irq".format(device_name)
    # Presets for global mapping of specific device declaration vars/ constants
    for dev_id in edts['devices']:
        device_name = device_name_by_id(dev_id)
        driver_name = edts.device_property(dev_id, 'label').strip('"')
        presets['{}:device-name'.format(dev_id)] = device_name
        presets['{}:driver-name'.format(dev_id)] = driver_name
        presets['{}:device-data'] = '{}_data' \
            .format(dev_id, device_name.lower())
        presets['{}:device-config'] = "{}_config" \
            .format(dev_id, device_name.lower())
        presets['{}:device-config-irq'] = "{}_config_irq" \
            .format(dev_id, device_name.lower())

    # device info
    if device_info:
        device_info = edts.device_template_substitute(device_id, device_info,
                                            presets, _property_path_aliases)
        cogeno.outl(device_info)

    # device init
    cogeno.outl(edts.device_template_substitute(device_id, _device_define_tmpl,
                                            presets, _property_path_aliases))
    return True

##
# @brief Declare multiple device instances.
#
# Generate device instances code for all device instances that:
#
# - match the driver names that
# - are activated ('status' = 'ok') in the board device tree file and that are
# - configured by Kconfig.
#
# @param device_config_symbols
#   A list of configuration symbols for device instantiation.
#   (e.g. ['CONFIG_SPI_0', 'CONFIG_SPI_1'])
# @param driver_names
#   A list of driver names for device instantiation. The list shall be ordered
#   as the list of device configs.
#   (e.g. ['SPI_0', 'SPI_1'])
# @param device_inits
#   A list of device initialisation functions or a single function. The
#   list shall be ordered as the list of device configs.
#   (e.g. 'spi_stm32_init')
# @param device_pm_controls
#   A list of device power management functions or a single function. The
#   list shall be ordered as the list of device configs.
#   (e.g. 'device_pm_control_nop')
# @param device_levels
#   A list of driver initialisation levels or one single level definition. The
#   list shall be ordered as the list of device configs.
#   (e.g. 'PRE_KERNEL_1')
# @param device_prios
#   A list of driver initialisation priorities or one single priority
#   definition. The list shall be ordered as the list of device configs.
#   (e.g. 32)
# @param device_api
#   Identifier of the device api.
#   (e.g. 'spi_stm32_driver_api')
# @param device_info
#   Device info template for device driver config, data and interrupt
#   initialisation.
# @param device_defaults
#   Device default property values. `device_defaults` is a dictionary of
#   property path : property value.
def device_declare_multi(device_config_symbols,
                         driver_names,
                         device_inits,
                         device_pm_controls,
                         device_levels,
                         device_prios,
                         device_api,
                         device_info,
                         device_defaults = {}):
    devices_declared = []
    for i, device_config_symbol in enumerate(device_config_symbols):
        driver_name = driver_names[i]
        if isinstance(device_inits, str):
            device_init = device_inits
        else:
            try:
                device_init = device_inits[i]
            except:
                device_init = device_inits
        if isinstance(device_pm_controls, str):
            device_pm_control = device_pm_controls
        else:
            try:
                device_pm_control = device_pm_controls[i]
            except:
                device_pm_control = device_pm_controls
        if isinstance(device_levels, str):
            device_level = device_levels
        else:
            try:
                device_level = device_levels[i]
            except:
                device_level = device_levels
        if isinstance(device_prios, str):
            device_prio = device_prios
        else:
            try:
                device_prio = device_prios[i]
            except:
                device_prio = device_prios

        device_declared = device_declare_single(device_config_symbol,
                                                driver_name,
                                                device_init,
                                                device_pm_control,
                                                device_level,
                                                device_prio,
                                                device_api,
                                                device_info,
                                                device_defaults)
        devices_declared.append(str(device_declared))

    if 'True' not in devices_declared:
        err = "No active device found for {} = {} and {}.".format(
            ', '.join(device_config_symbols), ', '.join(devices_declared),
            ', '.join(driver_names))
        cogeno.log(err)
        cogeno.error(err)

# Copyright (c) 2017 Linaro Limited
# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import sys
import os
import re
from copy import deepcopy
from pathlib import Path

# Add libraries dir to path to make edtlib find it´s local imports
sys.path.append(str(Path(__file__).parent.joinpath('libraries').resolve()))
from .libraries.edtlib import EDT, EDTError

##
# @brief ETDS Database extractor
#
# Methods for ETDS database extraction from DTS.
#
class EDTSExtractorMixin(object):
    __slots__ = []

    ##
    # @brief Get EDTS device id associated to node.
    #
    # The device id is the path to the device node.
    #
    # According to the specifcation: "A node in the devicetree can be uniquely
    # identified by specifying the full path from the root node, through all
    # descendant nodes, to the desired node. A unit address may be omitted if
    # the full path to the node is unambiguous."
    #
    # To avoid ambiguous device ids the unit address is added if the device node
    # name misses it and there is a reg property in the node.
    #
    # @param node extended device tree node
    # @return ETDS device id
    def _extract_device_id(self, node):
        if '@' in node.path:
            return node.path
        elif node.regs:
            unit_address = hex(int(node.regs[0].address)).lower()
            return node.path + '@' + unit_address
        else:
            return node.path


    ##
    # @brief Extract aliases infos
    #
    # Handles:
    # - /aliases node
    #
    # Generates in EDTS.aliases:
    # - {alias} : {alias-value}
    #
    # @param node
    def _extract_aliases(self, node):

        if node.binding_path:
            # Aliases are controlled by a binding
            for alias, property in node.props.items():
                if property.type in ('phandle', 'path'):
                    self.insert_alias(alias,
                                      self._extract_device_id(property.val))
        else:
            # No binding - aliases are of
            # - path type defined as a string.
            # - path as a reference by label
            #
            # Path happends to be also the device id !-)
            for alias, property in node._node.props.items():
                node = property.to_path()
                property_val = node.path
                self.insert_alias(alias, property_val)


    ##
    # @brief Extract chosen infos
    #
    # Handles:
    # - /chosen node
    #
    # Generates in EDTS.chosen:
    # - {chosen} : {chosen-value}
    #
    # @param node
    def _extract_chosen(self, node):

        if node.binding_path:
            # Chosen is controlled by a binding
            for chosen, property in node.props.items():
                if chosen in ("stdout-path", "stdout", "linux,stdout-path"):
                    # stdout", "linux,stdout-path are deprecated
                    values = property.val.split(':', 2)
                    for i, value in enumerate(values):
                        if i == 0:
                            chosen_node = self._edt._node2enode[self._edt._dt.get_node(value)]
                            self.insert_chosen("{}/controller".format(chosen),
                                               self._extract_device_id(chosen_node))
                        elif i == 1:
                            self.insert_chosen("{}/data".format(chosen), value)
                elif property.type in ('boolean', 'int', 'string'):
                    self.insert_chosen(chosen, property.val)
                elif property.type in ('array', 'string-array'):
                    i = 0
                    for value in property.val:
                        self.insert_chosen("{}/{}".format(chosen, i), value)
                        i += 1
                    self.insert_chosen("{}/count".format(chosen), i)
                elif property.type in ('phandle', 'path'):
                    self.insert_chosen(
                        chosen, self._extract_device_id(property.val))
                elif property.type in ('phandles'):
                    i = 0
                    for phandle in property.val:
                        self.insert_chosen("{}/{}".format(chosen, i),
                                           self._extract_device_id(phandle))
                        i += 1
                    self.insert_chosen("{}/count".format(chosen), i)
                elif property.type in ('phandle-array'):
                    i = 0
                    for controller_and_data in property.val:
                        self.insert_chosen("{}/{}/controller".format(chosen, i),
                            self._extract_device_id(controller_and_data.controller))
                        for data_name, data_value in controller_and_data.data.items():
                            self.insert_chosen("{}/{}/{}"
                                .format(chosen, i, data_name), data_value)
                        i += 1
                    self.insert_chosen("{}/count".format(chosen), i)
        else:
            # No binding - all chosen property values are of string type.
            for chosen, property in node._node.props.items():
                property_val = property.to_string()
                self.insert_chosen(chosen, property_val)


    ##
    # @brief Extract default directive infos
    #
    # Handles:
    # - TBD
    # - gpio-ranges             : phandle-array
    # - dma-channels            : array
    # - dma-requests            : array
    # - dmas                    : phandle-array
    # - dma-names               : string-array
    # - pwms                    : phandle-array
    # - pwm-names               : string-array
    #
    # Generates in EDTS:
    # - name
    # - path
    # - parent                  : device id of parent device
    # - node-label/{index}      : node label
    # - node-label/count        : number of node labels
    #
    # Dependency information
    # ----------------------
    # - depend/ordinal          : A non-negative integer value such that the
    #                             value for a Node is less than the value for
    #                             all Nodes that depend on it.
    # - depend/on/{index}       TBD
    # - depend/on/count         TBD
    # - depend/by/{index}       TBD
    # - depend/by/count         TBD
    #
    # DMA controller device
    # ---------------------
    # - dma-channels            : Number of DMA channels supported by the
    #                             controller.
    # - dma-requests            : Number of DMA request signals supported by the
    #                             controller
    #
    # DMA client device
    # -----------------
    # - dma/index/{name}        : index of dma channel with name
    # - dma/{index}/name        : name of dma channel
    # - dma/{index}/controller  : device id of dma controller
    # - dma/{index}/<cell-name> : <cell-value>
    #                             (cell-name from cell-names of controller)
    # - dma/count                : number of dma channels used
    #
    # GPIO controller device
    # ----------------------
    # - gpio-range/index/{name}                : index of range with name
    # - gpio-range/{index}/name                : range name
    # - gpio-range/{index}/controller          : device_id of pin controller
    # - gpio-range/{index}/gpio-base           : base pin of gpio
    # - gpio-range/{index}/count               : number of pins
    # - gpio-range/{index}/pinctrl-base        : base pin of pin controller
    # - gpio-range/count                       : number of gpio ranges
    #
    # PWM client device
    # -----------------
    # - pwm/index/{name}        : index of pwm input with name
    # - pwm/{index}/name        : name of pwm input
    # - pwm/{index}/controller  : device id of pwm controller
    # - pwm/{index}/<cell-name> : <cell-value>
    #                             (cell-name from cell-names of controller)
    # - pwm/count                : number of pwm inputs used
    #
    # @param node
    def _extract_default(self, node):

        device_id = self._extract_device_id(node)

        self.insert_device_property(device_id, "name", node.name)
        self.insert_device_property(device_id, "path", node.path)

        # node labels
        label_i = 0
        if node.labels:
            for label in node.labels:
                self.insert_device_property(device_id,
                    "node-label/{}".format(label_i), label)
                label_i += 1
        self.insert_device_property(device_id, "node-label/count", label_i)

        # dependencies
        self.insert_device_property(device_id, "depend/ordinal",
                                    node.dep_ordinal)
        depend_on_i = 0
        if node.depends_on:
            for depend_on in node.depends_on:
                depend_on_id = self._extract_device_id(depend_on)
                self.insert_device_property(device_id,
                    "depend/on/{}".format(depend_on_i), depend_on_id)
                depend_on_i += 1
        self.insert_device_property(device_id, "depend/on/count", depend_on_i)
        depend_by_i = 0
        if node.required_by:
            for depend_by in node.required_by:
                depend_by_id = self._extract_device_id(depend_by)
                self.insert_device_property(device_id,
                    "depend/by/{}".format(depend_by_i), depend_by_id)
                depend_by_i += 1
        self.insert_device_property(device_id, "depend/by/count", depend_by_i)

        # compatibles
        compat_i = 0
        if node.compats:
            for compat in node.compats:
                self.insert_device_property(device_id,
                    "compatible/index/{}".format(compat), compat_i)
                self.insert_device_property(device_id,
                    "compatible/{}".format(compat_i), compat)
                if compat == node.matching_compat:
                    self.insert_device_property(device_id,
                                                "compatible/match", compat_i)
                compat_i += 1
        self.insert_device_property(device_id, "compatible/count", compat_i)

        parent_device_id = self._extract_device_id(node.parent)
        self.insert_device_property(device_id, "parent", parent_device_id)

        for name, property in node.props.items():
            if name.startswith((
                    "#",
                    "reg",
                    "interrupts", "interrupts-extended",
                    "pinctrl-"
                )) or name.endswith((
                    "gpios", "-map", "-names"
                )):
                # skip properties already handled by other extractions.
                continue
            if property.type == 'boolean':
                if property.val:
                    value = 1
                else:
                    value = 0
                self.insert_device_property(device_id, name, value)
            elif property.type in ('int', 'string'):
                self.insert_device_property(device_id, name, property.val)
            elif property.type in ('array', 'string-array'):
                i = 0
                for value in property.val:
                    self.insert_device_property(device_id,
                        "{}/{}".format(name, i), value)
                    i += 1
                self.insert_device_property(device_id,
                                            "{}/count".format(name), i)
            elif property.type in ('phandle', 'path'):
                self.insert_device_property(device_id, name,
                    self._extract_device_id(property.val))
            elif property.type in ('phandles'):
                if name.endswith("s"):
                    name = name[:-1]
                i = 0
                for phandle in property.val:
                    self.insert_device_property(device_id,
                        "{}/{}".format(name, i),
                        self._extract_device_id(phandle))
                    i += 1
                self.insert_device_property(device_id,
                                            "{}/count".format(name), i)
            elif property.type in ('phandle-array'):
                if name.endswith("s"):
                    name = name[:-1]
                i = 0
                for controller_and_data in property.val:
                    if not controller_and_data.name:
                        controller_and_data_name = "{}_{}".format(name.upper(), i)
                    else:
                        controller_and_data_name = controller_and_data.name
                    self.insert_device_property(device_id,
                        "{}/{}/name".format(name, i), controller_and_data_name)
                    self.insert_device_property(device_id,
                        "{}/index/{}".format(name, controller_and_data_name), i)
                    self.insert_device_property(device_id,
                        "{}/{}/controller".format(name, i),
                        self._extract_device_id(controller_and_data.controller))
                    for data_name, data_value in controller_and_data.data.items():
                        self.insert_device_property(device_id, "{}/{}/{}"
                            .format(name, i, data_name), data_value)
                    i += 1
                self.insert_device_property(device_id,
                                            "{}/count".format(name), i)

    ##
    # @brief Extract reg directive info
    #
    # Handles:
    # - reg
    # - reg-names
    #
    # Generates in EDTS:
    # - reg/index/{name}        : index of register with name
    # - reg/{index}/name        : register name
    # - reg/{index}/address
    # - reg/{index}/size
    # - reg/count               : number of registers
    #
    # @param node
    def _extract_reg(self, node):

        device_id = self._extract_device_id(node)
        if node.regs:
            i = 0
            for reg in node.regs:
                if not reg.name:
                    reg_name = "REG_{}".format(i)
                else:
                    reg_name = reg.name
                self.insert_device_property(device_id, "reg/index/{}"
                    .format(reg_name), i)
                self.insert_device_property(device_id, "reg/{}/name"
                    .format(i), reg_name)
                self.insert_device_property(device_id, "reg/{}/address"
                    .format(i), reg.addr)
                self.insert_device_property(device_id, "reg/{}/size"
                    .format(i), reg.size)
                i += 1
            self.insert_device_property(device_id, "reg/count", i)

    ##
    # @brief Extract interrupts directive info
    #
    # Handles:
    # - interrupts
    # - interrupts-extended
    # - interrupt-names
    #
    # Generates in EDTS:
    # - interrupt/index/{name}           : index of interrupt with name
    # - interrupt/{index}/name           : interrupt name
    # - interrupt/{index}/controller     : device id of interrupt controller
    # - interrupt/{index}/{cell-name}    : {cell-value}
    # - interrupt/count                  : number of interrupts
    #
    # @param node
    def _extract_interrupts(self, node):

        device_id = self._extract_device_id(node)
        if node.interrupts:
            i = 0
            for interrupt in node.interrupts:
                if not interrupt.name:
                    interrupt_name = "IRQ_{}".format(i)
                else:
                    interrupt_name = interrupt.name
                self.insert_device_property(device_id, "interrupt/index/{}"
                    .format(interrupt_name), i)
                self.insert_device_property(device_id, "interrupt/{}/name"
                    .format(i), interrupt_name)
                interrupt_parent = self._extract_device_id(interrupt.controller)
                self.insert_device_property(device_id, "interrupt/{}/controller"
                    .format(i), interrupt_parent)
                for data_name, data_value in interrupt.data.items():
                    self.insert_device_property(device_id, "interrupt/{}/{}"
                        .format(i, data_name), data_value)
                i += 1
            self.insert_device_property(device_id, "interrupt/count", i)

    ##
    # @brief Extract gpio directives info
    #
    # Handles:
    # - xxx-gpios
    #
    # Generates in EDTS:
    # - xxx-gpios/{index}/controller            : device_id of gpio controller
    # - xxx-gpios/{index}/<cell-name> : <cell-value>
    #                  (cell-name from cell-names of gpio controller)
    # - xxx-gpios/count                         : number of xxx gpios
    #
    # @param node
    def _extract_gpio(self, node):

        device_id = self._extract_device_id(node)

        for gpios_name, gpios_specifiers in node.props.items():
            if gpios_name == "gpios" or gpios_name.endswith("-gpios"):
                i = 0
                for gpio_specifier in gpios_specifiers.val:
                    gpio_controller = self._extract_device_id(gpio_specifier.controller)
                    self.insert_device_property(device_id, "{}/{}/controller"
                        .format(gpios_name, i), gpio_controller)
                    for data_name, data_value in gpio_specifier.data.items():
                        self.insert_device_property(device_id, "{}/{}/{}"
                            .format(gpios_name, i, data_name), data_value)
                    i += 1
                self.insert_device_property(device_id, "{}/count"
                                                       .format(gpios_name), i)

    ##
    # @brief Extract clock related directives.
    #
    # Handles:
    # - clock-output-names
    # - clock-indices
    # - clocks
    # - clock-names
    # - clock-ranges
    # - clock-frequency
    # - clock-accuracy
    # - oscillator
    # - assigned-clocks
    # - assigned-clock-parents
    # - assigned-clock-rates
    #
    # Generates in EDTS:
    #
    # Clock provider device
    # ---------------------
    # - clock-output/index/{name}   : index of clock output with name
    # - clock-output/{index}/name   : clock output name
    # - clock-output/{index}/clock-frequency : fixed clock output frequency in Hz
    # - clock-output/{index}/clock-accuracy : accuracy of clock in ppb (parts per billion).
    # - clock-output/{index}/oscillator :  True
    #
    # Clock consumer device
    # ---------------------
    # - clock/index/{name}     : index of clock input with name
    # - clock/{index}/name     : name of clock input
    # - clock/{index}/provider : device id of clock provider
    # - clock/{index}/<cell-name> : <cell-value>
    #                  (cell-name from cell-names of provider)
    # - clock-ranges            : True
    # - assigned-clock/{index}/provider : device id of provider of assigned clock
    # - assigned-clock/{index}/rate : selected rate of assigned clock in Hz
    # - assigned-clock/{index}/<cell-name> : <cell-value>
    #                           (cell-name from cell-names of provider)
    # - assigned-clock/{index}/parent/provider : provider of parent clock of assigned clock
    # - assigned-clock/{index}/parent/<cell-name> : <cell-value>
    #                                  (cell-name from cell-names of provider)
    #
    # Other device
    # ------------
    # - clock-frequency : clock frequency in Hz
    #
    # @param node
    def _extract_clocks(self, node):

        device_id = self._extract_device_id(node)

        # clock provider
        if node.clock_outputs:
            i = 0
            for clock_output in node.clock_outputs:
                if not clock_output.name:
                    clock_output_name = "CLOCK_{}".format(i)
                else:
                    clock_output_name = clock_output.name
                self.insert_device_property(device_id, "clock-output/index/{}"
                    .format(clock_output_name), i)
                self.insert_device_property(device_id, "clock-output/{}/name"
                    .format(i), clock_output_name)
                for data_name, data_value in clock_output.data.items():
                    self.insert_device_property(device_id, "clock-output/{}/{}"
                        .format(i, data_name), data_value)
                i += 1
            self.insert_device_property(device_id, "clock-output/count", i)

        # clock consumer
        if node.clocks:
            i = 0
            for clock in node.clocks:
                if not clock.name:
                    clock_name = "CLOCK_{}".format(i)
                else:
                    clock_name = clock.name
                self.insert_device_property(device_id, "clock/index/{}"
                    .format(clock_name), i)
                self.insert_device_property(device_id, "clock/{}/name"
                    .format(i), clock_name)
                provider = self._extract_device_id(clock.controller)
                self.insert_device_property(device_id,
                    "clock/{}/provider".format(i), provider)
                for data_name, data_value in clock.data.items():
                    self.insert_device_property(device_id, "clock/{}/{}"
                        .format(i, data_name), data_value)
                i += 1
            self.insert_device_property(device_id, "clock/count", i)

        if 'assigned-clocks' in node.props:
            i = 0
            for assigned_clock in node.props['assigned-clocks'].val:
                if not assigned_clock.name:
                    assigned_clock_name = "CLOCK_{}".format(i)
                else:
                    assigned_clock_name = assigned_clock.name
                self.insert_device_property(device_id, "assigned-clock/index/{}"
                    .format(clock_name), i)
                self.insert_device_property(device_id, "assigned-clock/{}/name"
                    .format(i), clock_name)
                provider = self._extract_device_id(assigned_clock.controller)
                self.insert_device_property(device_id,
                    "clock/{}/provider".format(i), provider)
                for data_name, data_value in assigned_clock.data.items():
                    self.insert_device_property(device_id, "assigned-clock/{}/{}"
                        .format(i, data_name), data_value)
                i += 1
            self.insert_device_property(device_id, "assigned-clock/count", i)

    ##
    # @brief Extract partitions info
    #
    # Handles:
    # - partitions nodes of flash
    #
    # Generates in EDTS.devices[{device-id}]:
    #
    # Flash device
    # ------------
    # - controller                 : device id of flash controller
    # - partition/index/{name}     : index of partition with name
    # - partition/{index}/name     : name of the partition
    # - partition/{index}/address  : address of partition within flash/ partition
    # - partition/{index}/size     : size of partition
    # - partition/{index}/flash    : device_id of flash device
    # - partition/{index}/controller : device_id of flash controller
    # - partition/{index}/<cell-name> : <cell-value>
    # - partition/count            : number of partions
    #
    # @param node
    def _extract_partitions(self, node):
        if not node.partitions or node.parent.name == 'partitions':
            # Node does not have partitions (no flash device node)
            # or is a child of a partitions node (no flash device node)
            return

        device_id = self._extract_device_id(node)
        i = 0
        for partition in node.partitions:
            self.insert_device_property(device_id, "partition/index/{}"
                .format(partition.name), i)
            self.insert_device_property(device_id, "partition/{}/name"
                .format(i), partition.name)
            flash = self._extract_device_id(partition.flash)
            self.insert_device_property(device_id, "partition/{}/flash"
                .format(i), flash)
            controller = self._extract_device_id(partition.controller)
            self.insert_device_property(device_id, "partition/{}/controller"
                .format(i), controller)
            self.insert_device_property(device_id, "partition/{}/address"
                .format(i), partition.addr)
            self.insert_device_property(device_id, "partition/{}/size"
                .format(i), partition.size)
            for prop_name, prop_value in partition.attributes.items():
                if isinstance(prop_value, bool):
                    if prop_value:
                        prop_value = 1
                    else:
                        prop_value = 0
                self.insert_device_property(device_id, "partition/{}/{}"
                    .format(i, prop_name), prop_value)
            i += 1
        self.insert_device_property(device_id, "partition/count", i)
        self.insert_device_property(device_id, "controller", controller)


    ##
    # @brief Extract gpio leds info
    #
    # Handles:
    # - gpio led nodes of gpio leds controllers
    #
    # Generates in EDTS.devices[{device-id}]:
    #
    # Gpio leds controller device
    # ---------------------------
    # - gpio-led/index/{name}     : index of gpio led with name
    # - gpio-led/{index}/name     : name of the gpio led
    # - gpio-led/{index}/controller : device_id of flash controller
    # - gpio-led/{index}/gpio/index/{gpio-name} : index of the gpio control with name
    # - gpio-led/{index}/gpio/{gpio-index}/name : name of the gpio control
    # - gpio-led/{index}/gpio/{gpio-index}/controller : device_id of the gpio controller
    # - gpio-led/{index}/gpio/{gpio-index}/<cell-name> : <cell-value>
    # - gpio-led/{index}/gpio/count : number of gpio controls for led
    # - gpio-led/{index}/led-pattern/{index} : led pattern value
    # - gpio-led/{index}/led-pattern/count   : number of led pattern values
    # - gpio-led/{index}/<cell-name> : <cell-value>
    # - gpio-led/count            : number of partions
    #
    # @param node
    def _extract_gpio_leds(self, node):
        if not node.gpio_leds:
            # Node does not have gpio leds children
            return

        device_id = self._extract_device_id(node)
        i = 0
        for gpio_led in node.gpio_leds:
            self.insert_device_property(device_id, "gpio-led/index/{}"
                .format(gpio_led.name), i)
            self.insert_device_property(device_id, "gpio-led/{}/name"
                .format(i), gpio_led.name)
            controller = self._extract_device_id(gpio_led.controller)
            self.insert_device_property(device_id, "gpio-led/{}/controller"
                .format(i), controller)
            for data_name, data_value in gpio_led.data.items():
                if data_name == "gpios":
                    gpio_i = 0
                    for gpio in data_value:
                        if not gpio.name:
                            gpio_name = "GPIO_{}".format(gpio_i)
                        else:
                            gpio_name = gpio.name
                        self.insert_device_property(device_id,
                            "gpio-led/{}/gpio/index/{}"
                            .format(i, gpio_name), gpio_i)
                        self.insert_device_property(device_id,
                            "gpio-led/{}/gpio/{}/name"
                            .format(i, gpio_i), gpio_name)
                        controller = self._extract_device_id(gpio.controller)
                        self.insert_device_property(device_id,
                            "gpio-led/{}/gpio/{}/controller"
                            .format(i, gpio_i), controller)
                        for gpio_data_name, gpio_data_value in gpio.data.items():
                            self.insert_device_property(device_id,
                                "gpio-led/{}/gpio/{}/{}"
                                .format(i, gpio_i, gpio_data_name), gpio_data_value)
                    self.insert_device_property(device_id,
                        "gpio-led/{}/gpio/count".format(i), gpio_i)
                    continue
                elif data_name == "led-pattern":
                    led_pattern_i = 0
                    for led_pattern in data_value:
                        self.insert_device_property(device_id,
                            "gpio-led/{}/led-pattern/{}"
                            .format(i, led_pattern_i), led_pattern)
                        led_pattern_i += 1
                    self.insert_device_property(device_id,
                         "gpio-led/{}/led-pattern/count"
                         .format(i, led_pattern_i), led_pattern_i)
                    continue
                elif isinstance(data_value, bool):
                    if data_value:
                        data_value = 1
                    else:
                        data_value = 0
                self.insert_device_property(device_id, "gpio-led/{}/{}"
                    .format(i, data_name), data_value)
            i += 1
        self.insert_device_property(device_id, "gpio-led/count", i)


    ##
    # @brief Extract pinctrl related directives.
    #
    # Handles:
    # - pinctrl-x
    # - pinctrl-names
    #
    # Generates in EDTS.devices[{device-id}]:
    #
    # Pin controller device
    # ---------------------
    # - pinctrl-state/index/{name}     : index of pinctrl state with name
    # - pinctrl-state/{index}/name     : name of the pinctrl state
    # - pinctrl-state/{index}/path     : path of the pinctrl state node
    # - pinctrl-state/{index}/pincfg/index/{name} : index of pin
    #                                               configuration with name
    # - pinctrl-state/{index}/pincfg/{index}/name : name of the pin
    #                                                configuration
    # - pinctrl-state/{index}/pincfg/{index}/groups/{index} : group name
    # - pinctrl-state/{index}/pincfg/{index}/groups/count   :
    # - pinctrl-state/{index}/pincfg/{index}/pins/{index}   : pin identifier
    # - pinctrl-state/{index}/pincfg/{index}/pins/count     :
    # - pinctrl-state/{index}/pincfg/{index}/muxes/{index}  : mux value
    # - pinctrl-state/{index}/pincfg/{index}/muxes/count    :
    # - pinctrl-state/{index}/pincfg/{index}/function       : function name
    # - pinctrl-state/{index}/pincfg/{index}/bias-disable        : pincfg value
    # - pinctrl-state/{index}/pincfg/{index}/bias-high-impedance : ..
    # - pinctrl-state/{index}/pincfg/{index}/bias-bus-hold       : ..
    # - pinctrl-state/{index}/pincfg/{index}/..                  : ..
    # - pinctrl-state/{index}/pincfg/count : number of pin configurations
    # - pinctrl-state/count : number of pinctrl states
    # - pinctrl-group/index/{name}      : index of group with name
    # - pinctrl-group/{index}/name      : name of the group
    # - pinctrl-group/count : number of pinctrl groups
    # - pinctrl-function/index/{name}
    # - pinctrl-function/{index}/name
    # - pinctrl-function/count : number of pinctrl functions
    # - pinctrl-gpio-range/index/{name}         : index of range with name
    # - pinctrl-gpio-range/{index}/name         : range name
    # - pinctrl-gpio-range/{index}/gpio         : device_id of gpio controller
    # - pinctrl-gpio-range/{index}/gpio-base    : base pin of gpio
    # - pinctrl-gpio-range/{index}/count        : number of pins
    # - pinctrl-gpio-range/{index}/pinctrl-base : base pin of pin controller
    # - pinctrl-gpio-range/count                : number of gpio ranges
    #
    # Pinctrl client device
    # ---------------------
    # - pinctrl/index/{name}           : index of pinctrl with name
    # - pinctrl/{index}/name           : name of the pinctrl
    # - pinctrl/{index}/pinctrl-state/{index}/pin-controller : device_id of
    #                                                          pin controller
    # - pinctrl/{index}/pinctrl-state/{index}/name : name of pinctrl state
    # - pinctrl/{index}/pinctrl-state/count : number of pinctrl states
    #                                         referenced by the pinctrl
    # - pinctrl/count : number of pinctrls
    #
    # @param node
    def _extract_pinctrl(self, node):

        device_id = self._extract_device_id(node)

        # Pin controller device
        if node.pinctrl_states:
            groups = []
            functions = []

            pinctrl_state_i = 0
            for pinctrl_state in node.pinctrl_states:
                if not pinctrl_state.name:
                    pinctrl_state_name = "PINCTRL_STATE_{}".format(
                        pinctrl_state_i)
                else:
                    pinctrl_state_name = pinctrl_state.name
                self.insert_device_property(device_id, "pinctrl-state/index/{}"
                    .format(pinctrl_state_name), pinctrl_state_i)
                self.insert_device_property(device_id, "pinctrl-state/{}/name"
                    .format(pinctrl_state_i), pinctrl_state_name)
                self.insert_device_property(device_id, "pinctrl-state/{}/path"
                    .format(pinctrl_state_i), pinctrl_state.path)
                pincfg_i = 0
                for pincfg in pinctrl_state.pincfgs:
                    if pincfg.name:
                        pincfg_name = pincfg.name
                    else:
                        pincfg_name = "PINCFG_{}".format(pincfg_i)
                    self.insert_device_property(device_id,
                        "pinctrl-state/{}/pincfg/index/{}"
                        .format(pinctrl_state_i, pincfg_name), pincfg_i)
                    self.insert_device_property(device_id,
                        "pinctrl-state/{}/pincfg/{}/name"
                        .format(pinctrl_state_i, pincfg_i), pincfg_name)
                    if pincfg.groups:
                        group_i = 0
                        for group in pincfg.groups:
                            groups.append(group)
                            self.insert_device_property(device_id,
                                "pinctrl-state/{}/pincfg/{}/groups/{}"
                                .format(pinctrl_state_i, pincfg_i, group_i),
                                group)
                            group_i += 1
                        self.insert_device_property(device_id,
                            "pinctrl-state/{}/pincfg/{}/groups/count"
                            .format(pinctrl_state_i, pincfg_i), group_i)
                    if pincfg.pins:
                        pin_i = 0
                        for pin in pincfg.pins:
                            self.insert_device_property(device_id,
                                "pinctrl-state/{}/pincfg/{}/pins/{}"
                                .format(pinctrl_state_i, pincfg_i, pin_i),
                                pin)
                            pin_i += 1
                        self.insert_device_property(device_id,
                            "pinctrl-state/{}/pincfg/{}/pins/count"
                            .format(pinctrl_state_i, pincfg_i), pin_i)
                    if pincfg.muxes:
                        mux_i = 0
                        for mux in pincfg.muxes:
                            self.insert_device_property(device_id,
                                "pinctrl-state/{}/pincfg/{}/muxes/{}"
                                .format(pinctrl_state_i, pincfg_i, mux_i),
                                mux)
                            mux_i += 1
                        self.insert_device_property(device_id,
                            "pinctrl-state/{}/pincfg/{}/muxes/count"
                            .format(pinctrl_state_i, pincfg_i), mux_i)
                    if pincfg.function:
                        functions.append(pincfg.function)
                        self.insert_device_property(device_id,
                            "pinctrl-state/{}/pincfg/{}/function"
                            .format(pinctrl_state_i, pincfg_i), pincfg.function)
                    for config_name, config_value in pincfg.configs.items():
                        if isinstance(config_value, bool):
                            if config_value:
                                config_value = 1
                            else:
                                config_value = 0
                        self.insert_device_property(device_id,
                            "pinctrl-state/{}/pincfg/{}/{}"
                            .format(pinctrl_state_i, pincfg_i, config_name),
                            config_value)
                    pincfg_i += 1
                self.insert_device_property(device_id,
                    "pinctrl-state/{}/pincfg/count"
                    .format(pinctrl_state_i), pincfg_i)
                pinctrl_state_i += 1
            self.insert_device_property(device_id, "pinctrl-state/count",
                                        pinctrl_state_i)

            group_i = 0
            if groups:
                # sorted list of groups with duplicates removed
                groups = list(set(groups))
                groups.sort()
                for group in groups:
                    self.insert_device_property(device_id,
                                                "pinctrl-group/index/{}"
                                                .format(group), group_i)
                    self.insert_device_property(device_id, "pinctrl-group/{}"
                                                .format(group_i), group)
                    group_i += 1
            self.insert_device_property(device_id, "pinctrl-group/count",
                                        group_i)

            function_i = 0
            if functions:
                # sorted list of functions with duplicates removed
                functions = list(set(functions))
                functions.sort()
                for function in functions:
                    self.insert_device_property(device_id,
                                                "pinctrl-function/index/{}"
                                                .format(function), function_i)
                    self.insert_device_property(device_id, "pinctrl-function/{}"
                                                .format(function_i), function)
                    function_i += 1
            self.insert_device_property(device_id, "pinctrl-function/count",
                                        function_i)
        if node.pinctrl_gpio_ranges:
            gpio_range_i = 0
            for gpio_range in node.pinctrl_gpio_ranges:
                if not gpio_range.name:
                    gpio_range_name = "PINCTRL_GPIO_RANGE_{}".format(
                                                                   gpio_range_i)
                else:
                    gpio_range_name = gpio_range.name
                self.insert_device_property(device_id,
                    "pinctrl-gpio-range/index/{}".format(gpio_range_name),
                    gpio_range_i)
                self.insert_device_property(device_id,
                    "pinctrl-gpio-range/{}/name".format(gpio_range_i),
                    gpio_range_name)
                gpio_device_id = self._extract_device_id(gpio_range.controller)
                self.insert_device_property(device_id,
                    "pinctrl-gpio-range/{}/gpio".format(gpio_range_i),
                    gpio_device_id)
                for data_name, data_value in gpio_range.data.items():
                    if isinstance(data_value, bool):
                        if data_value:
                            data_value = 1
                        else:
                            data_value = 0
                    self.insert_device_property(device_id,
                        "pinctrl-gpio-range/{}/{}".format(gpio_range_i, data_name),
                        data_value)
                gpio_range_i += 1
            self.insert_device_property(device_id, "pinctrl-gpio-range/count",
                                        gpio_range_i)

        # Pinctrl client device
        if node.pinctrls:
            pinctrl_i = 0
            for pinctrl in node.pinctrls:
                if not pinctrl.name:
                    pinctrl_name = "PINCTRL_{}".format(pinctrl_state_i)
                else:
                    pinctrl_name = pinctrl.name
                self.insert_device_property(device_id, "pinctrl/index/{}"
                    .format(pinctrl_name), pinctrl_i)
                self.insert_device_property(device_id, "pinctrl/{}/name"
                    .format(pinctrl_i), pinctrl_name)
                pinctrl_state_i = 0
                for pinctrl_state in pinctrl.conf_nodes:
                    pin_controller = self._extract_device_id(
                        pinctrl_state.pin_controller)
                    self.insert_device_property(device_id,
                        "pinctrl/{}/pinctrl-state/{}/pin-controller"
                        .format(pinctrl_i, pinctrl_state_i), pin_controller)
                    self.insert_device_property(device_id,
                        "pinctrl/{}/pinctrl-state/{}/name"
                        .format(pinctrl_i, pinctrl_state_i), pinctrl_state.name)
                    pinctrl_state_i += 1
                self.insert_device_property(device_id,
                    "pinctrl/{}/pinctrl-state/count".format(pinctrl_i),
                    pinctrl_state_i)
                pinctrl_i += 1
            self.insert_device_property(device_id, "pinctrl/count", pinctrl_i)


    ##
    # @brief Extract DTS info to database
    #
    # @param dts_path DTS file
    # @param bindings_dirs YAML file directories, we allow multiple
    # @param bindings_exclude YAML file directories and YAML files, we allow multiple
    # @param bindings_no_default Do not use default bindings
    def extract(self, dts_path, bindings_dirs, bindings_exclude, bindings_no_default):

        if not bindings_no_default:
            # Assure the EDTS generic bindings are given priority over other bindings.
            bindings_dirs.insert(0, Path(__file__).parent.joinpath('dts', 'bindings').resolve())
        try:
            # Assure every path is a string for edtlib
            dts_path_s = str(dts_path)
            bindings_dirs_s = [str(x) for x in bindings_dirs]
            bindings_exclude_s = [str(x) for x in bindings_exclude]
            self._edt = EDT(dts_path_s, bindings_dirs_s,
                            warn_file = None, bindings_exclude = bindings_exclude_s)
        except EDTError as e:
            sys.exit("devicetree error: " + str(e))

        # Extract device tree specification
        for node in self._edt.nodes:
            if node.name in ("chosen"):
                self._extract_chosen(node)
                continue
            if node.name in ("aliases"):
                self._extract_aliases(node)
                continue
            if node.name in ("/", "partitions"):
                # Special nodes, handled elsewhere
                continue
            if any(compat in ('pinctrl-state', 'pincfg', 'partition',         \
                              'fixed-partition', 'gpio-led')                  \
                   for compat in node.compats):
                # nodes handled by extract_pinctrl or extract_partitions
                # as child-nodes
                continue

            self._extract_reg(node)
            self._extract_interrupts(node)
            self._extract_gpio(node)
            self._extract_clocks(node)
            self._extract_gpio_leds(node)
            self._extract_partitions(node)
            self._extract_pinctrl(node)
            self._extract_default(node)

        # Remember the sources of the extended device tree database
        self._edts['info']['dts_path'] = str(self._edt.dts_path)
        self._edts['info']['bindings_dirs'] = []
        for binding_dir in self._edt.bindings_dirs:
            self._edts['info']['bindings_dirs'].append(str(binding_dir))
        # Split dts source in lines - easier to read in json file
        self._edts['info']['dts_source'] = []
        for line in self._edt.dts_source.splitlines():
            self._edts['info']['dts_source'].append(line)

    ##
    # @brief Device tree file path.
    #
    # @return Device tree file path
    def dts_path(self):
        return self._edts['info']['dts_path']

    ##
    # @brief Bindings directories paths
    #
    # @return List of binding directories
    def bindings_dirs(self):
        return self._edts['info']['bindings_dirs']

    ##
    # @brief DTS source code
    #
    # DTS source code of the loaded devicetree after merging nodes
    # and processing /delete-node/ and /delete-property/.
    #
    # @return DTS source code as string
    def dts_source(self):
        return '\n'.join(self._edts['info']['dts_source'])

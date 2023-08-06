# Copyright (c) 2018 Linaro Limited
# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path
from string import Template

##
# @brief ETDS Database consumer
#
# Methods for ETDS database usage.
#
class EDTSConsumerMixin(object):
    __slots__ = []

    ##
    # @brief Get info
    #
    # @param None
    # @return edts 'info' dict
    def info(self):
        return self._edts['info']

    ##
    # @brief Get compatibles
    #
    # @param None
    # @return edts 'compatibles' dict
    def compatibles(self):
        return self._edts['compatibles']

    ##
    # @brief Get aliases
    #
    # @param None
    # @return edts 'aliases' dict
    def aliases(self):
        return self._edts['aliases']

    ##
    # @brief Get chosen
    #
    # @param None
    # @return edts 'chosen' dict
    def chosen(self):
        return self._edts['chosen']

    ##
    # @brief Get device ids of all activated compatible devices.
    #
    # @param compatibles compatible(s)
    # @return list of device ids of activated devices that are compatible
    def device_ids_by_compatible(self, compatibles):
        device_ids = dict()
        if not isinstance(compatibles, list):
            compatibles = [compatibles, ]
        for compatible in compatibles:
            if compatible in self._edts['compatibles']:
                count = self._edts['compatibles'][compatible]['count']
                for i in range(0, count):
                    device_ids[self._edts['compatibles'][compatible][str(i)]] = 1
        return list(device_ids.keys())

    ##
    # @brief Get device ids of activated devices sorted by dependency ordinal
    #
    # Device ids of devices that are not activated but have an ordinal
    # associated are set to None.
    #
    # @param None
    # @return list of device ids of activated devices sorted by dependency ordinal
    def device_ids_by_dependency_order(self):
        dependencies = {}
        max_ordinal = 0
        for device_id in self._edts['devices']:
            ordinal = int(self.device_property(device_id, 'depend/ordinal'))
            if ordinal > max_ordinal:
                max_ordinal = ordinal
            dependencies[str(ordinal)] = device_id
        ordinal = 0
        dependency_order = []
        while ordinal <= max_ordinal:
            device_id = dependencies.get(str(ordinal), None)
            dependency_order.append(device_id)
            ordinal += 1
        return dependency_order

    ##
    # @brief Get device id of activated device with given name.
    #
    # @param name
    # @return device id
    def device_id_by_name(self, name):
        for device_id, device in self._edts['devices'].items():
            if name == device.get('name', None):
                return device_id
            for node_label_idx in range(0, device.get('node-label/count', 0)):
                if name == device.get(f'node-label/{node_label_idx}', None):
                    return device_id
            if name == device.get('label', None):
                return device_id
        print("consumer.py: Device with name",
               "'{}' not available in EDTS".format(name))
        return None

    ##
    # @brief Get device id of activated device for given alias.
    #
    # @param alias
    # @return device id or None
    def device_id_by_alias(self, alias):
        return self.aliases().get(alias, None)


    ##
    # @brief Get device id of activated device for given chosen.
    #
    # @param chosen
    # @return device id or None
    def device_id_by_chosen(self, chosen):
        return self.chosen().get(chosen, None)


    ##
    # @brief Get label/ name of a device by device id.
    #
    # If the label is omitted, the name is taken
    # from the node name (including unit address).
    #
    # @param device_id
    # @return name
    def device_name_by_id(self, device_id):
        name = self.device_property(device_id, 'label', None)
        if name is None:
            name = self.device_property(device_id, 'name')
        return name

    ##
    # @brief Get device tree property value of a device.
    #
    # @param device_id
    # @param property_path Path of the property to access
    #                      (e.g. 'reg/0/address', 'interrupts/prio', 'device_id', ...)
    # @param default Default value provided if device or property not available
    # @return property value
    def device_property(self, device_id, property_path, default="<unset>"):
        if not device_id in self._edts['devices']:
            print("consumer.py: Device with id ",
                  "'{}' not available in EDTS".format(device_id))
            if default == "<unset>":
                default = f"Device {device_id} not available" 
            return default
        property_value = self._edts['devices'][device_id]
        property_path_elements = property_path.strip("'").split('/')
        for property_path_elem in property_path_elements:
            if isinstance(property_value, dict):
                property_value = property_value.get(property_path_elem, None)
            elif isinstance(property_value, list):
                if int(property_path_elem) < len(property_value):
                    property_value = property_value[int(property_path_elem)]
                else:
                    property_value = None
            else:
                property_value = None
        if property_value is None:
            if default == "<unset>":
                default = "Device tree property {} not available in {}" \
                                .format(property_path, device_id)
            return default
        return property_value

    ##
    # @brief Get all device tree properties of a device.
    #
    # @param device_id
    # @return Dictionary of properties
    def device_properties(self, device_id):
        if not device_id in self._edts['devices']:
            print("consumer.py: Device with id ",
                  "'{}' not available in EDTS".format(device_id)) 
            return {}
        return self._edts['devices'][device_id]

    def _device_properties_flattened(self, properties, path, flattened,
                                     path_prefix):
        if isinstance(properties, dict):
            for prop_name, prop_value in properties.items():
                super_path = "{}/{}".format(path, prop_name).strip('/')
                self._device_properties_flattened(prop_value,
                                                  super_path, flattened,
                                                  path_prefix)
        elif isinstance(properties, list):
            for i, prop in enumerate(properties):
                super_path = "{}/{}".format(path, i).strip('/')
                self._device_properties_flattened(prop, super_path, flattened,
                                                  path_prefix)
        else:
            flattened[path_prefix + path] = properties

    ##
    # @brief Device properties flattened to property path : value.
    #
    # @param device_id
    # @param path_prefix
    # @return dictionary of property_path and property_value
    def device_properties_flattened(self, device_id, path_prefix = ""):
        flattened = dict()
        self._device_properties_flattened(self.device_properties(device_id), '',
                                          flattened, path_prefix)
        return flattened


    class _DeviceLocalTemplate(Template):
        # pattern is ${<property_path>}
        # never starts with /
        # extend default pattern by '-' '/' ','
        idpattern = r'[_a-z][_a-z0-9\-/,]*'


    class _DeviceGlobalTemplate(Template):
        # pattern is ${<device-id>:<property_path>}
        # device ID is the same as node address
        # always starts with /
        # extend default pattern by '-', '@', '/', ':'
        idpattern = r'/[_a-z0-9\-/,@:]*'


    def _device_template_aliases_mapping(self, mapping, aliases):
        aliases_mapping = {}
        for property_path, property_value in mapping.items():
            for alias_property_path, alias in aliases.items():
                if property_path.endswith(alias_property_path):
                    property_path = property_path[:-len(alias_property_path)] \
                                    + alias
                    aliases_mapping[property_path] = property_value
        return aliases_mapping


    ##
    # @brief Substitude device property value placeholders in template
    #
    # Local placeholders may be defined with direct and indirect path
    # resolution:
    #    - ${<property_path>}
    #    - ${path/${<property_path>}}
    #    - ${path/${<device-id>:<property_path>}}
    #
    # Global placeholders may also be defined with direct and indirect path
    # resolution:
    #    - ${<device-id>:<property_path>}
    #    - ${${<property_path>}:<property_path>}
    #    - ${${path/${<property_path>}}:<property_path>}
    #    - ${${path/${<device-id>:<property_path>}}:<property_path>}
    #    - ${${<device-id>:<property_path>}:<property_path>}
    #    - ${${<device-id>:path/${<property_path>}}:<property_path>}
    #    - ${${<device-id>:path/${<device-id>:<property_path>}}:<property_path>}
    #
    # @param device_id
    # @param template
    # @param presets dict of preset property-path : property value items
    #                either of the local form "<property_path>" : value or
    #                the global form "<device-id>:<property_path>" : value
    # @param aliases dict of property path alias : property path items.
    def device_template_substitute(self, device_id, template, presets={},
                                   aliases={}):
        local_presets = {}
        global_presets = {}
        for preset_key, preset_value in presets.items():
            if ':' in preset_key:
                global_presets[preset_key] = preset_value
            else:
                local_presets[preset_key] = preset_value

        # mapping for local placeholders ${<property_path>}
        local_mapping = {}
        local_mapping.update(local_presets)
        properties_flattened = self.device_properties_flattened(device_id)
        local_mapping.update(properties_flattened)
        local_mapping.update(self._device_template_aliases_mapping(
            local_mapping, aliases))
        # mapping for global placeholders ${<device-id>:<property_path>}
        global_mapping = {}
        global_mapping.update(global_presets)
        for device_id in self._edts['devices']:
            path_prefix = device_id + ':'
            properties_flattened = self.device_properties_flattened(device_id,
                                                                    path_prefix)
            global_mapping.update(properties_flattened)
        global_mapping.update(self._device_template_aliases_mapping(
            global_mapping, aliases))

        # 1. substitude local placeholdes
        #    - ${<property_path>}
        substituted = self._DeviceLocalTemplate(template).safe_substitute(
                                                                local_mapping)
        # 2. substitude global placeholders
        #    - ${<device-id>:<property_path>}
        #    and 1 level local indirects
        #    - ${${<property_path>}:<property_path>}
        substituted = self._DeviceGlobalTemplate(substituted).safe_substitute(
                                                                global_mapping)
        # 3. substitude 2 level local indirect
        #    - ${path/${<property_path>}}
        #    and 2 level local/global indirect
        #    - ${path/${<device-id>:<property_path>}}
        substituted = self._DeviceLocalTemplate(substituted).safe_substitute(
                                                                local_mapping)
        # 4. substitude 2 level global indirect
        #    - ${${<device-id>:<property_path>}:<property_path>}
        #    and 2 level global/local indirect
        #    - ${${path/${<property_path>}}:<property_path>}
        #    - ${${path/${<device-id>:<property_path>}}:<property_path>}
        #    and 2 level global/global indirect
        #    - ${${<device-id>:path/${<property_path>}}:<property_path>}
        #    - ${${<device-id>:path/${<device-id>:<property_path>}}:<property_path>}
        substituted = self._DeviceGlobalTemplate(substituted).safe_substitute(
                                                                global_mapping)

        return substituted


    ##
    # @brief Load extended device tree database from JSON file.
    #
    # @param file_path Path of JSON file
    def load(self, file_path):
        with Path(file_path).open(mode = "r", encoding="utf-8") as load_file:
            self._edts = json.load(load_file)

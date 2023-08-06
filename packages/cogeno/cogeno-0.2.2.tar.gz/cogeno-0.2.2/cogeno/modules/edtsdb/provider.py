#!/usr/bin/env python3
#
# Copyright (c) 2018 Bobby Noelte
# Copyright (c) 2018 Linaro Limited
#
# SPDX-License-Identifier: Apache-2.0
#

import json
from pathlib import Path

##
# @brief ETDS Database provider
#
# Methods for ETDS database creation.
#
class EDTSProviderMixin(object):
    __slots__ = []

    def _update_device_compatible(self, device_id, compatible):
        if compatible not in self._edts['compatibles']:
            self._edts['compatibles'][compatible] = dict()
            count = 0
        else:
            count = self._edts['compatibles'][compatible]['count']
        for i in range(0, count):
            if self._edts['compatibles'][compatible][str(i)] == device_id:
                return
        self._edts['compatibles'][compatible][str(count)] = device_id
        self._edts['compatibles'][compatible]['count'] = count + 1

    def _inject_cell(self, keys, property_access_point, property_value):

        for i in range(0, len(keys)):
            if i < len(keys) - 1:
                # there are remaining keys
                if keys[i] not in property_access_point:
                    property_access_point[keys[i]] = dict()
                property_access_point = property_access_point[keys[i]]
            else:
                # we have to set the property value
                if keys[i] in property_access_point and \
                    property_access_point[keys[i]] != property_value:
                    # Property is already set and we're overwiting with a new
                    # different value. Trigger an error
                    raise Exception("Overwriting edts cell {} with different value\n \
                                     Initial value: {} \n \
                                     New value: {}".format(property_access_point,
                                     property_access_point[keys[i]],
                                     property_value
                                     ))
                property_access_point[keys[i]] = property_value

    ##
    # @brief Insert an alias.
    #
    # @param alias_path Alias
    # @param alias_value The value the alias aliases.
    def insert_alias(self, alias_path, alias_value):
        keys = alias_path.strip("'").split('/')
        self._inject_cell(keys, self._edts['aliases'], alias_value)

    def insert_chosen(self, chosen_path, chosen_value):
        keys = chosen_path.strip("'").split('/')
        self._inject_cell(keys, self._edts['chosen'], chosen_value)

    ##
    # @brief Insert property value for the child of a device id.
    #
    # @param device_id
    # @param child_name
    # @param property_path Path of the property to access
    #                      (e.g. 'reg/0', 'interrupts/prio', 'label', ...)
    # @param property_value value
    #
    def insert_child_property(self, device_id, child_name, property_path, property_value):

        # normal property management
        if device_id not in self._edts['devices']:
            self._edts['devices'][device_id] = dict()
            self._edts['devices'][device_id]['device-id'] = device_id

        # Inject prop
        keys = ['children', child_name]
        prop_keys = property_path.strip("'").split('/')
        keys.extend(prop_keys)
        property_access_point = self._edts['devices'][device_id]
        self._inject_cell(keys, property_access_point, property_value)

        # Compute and inject unique device-id
        keys = ['device-id']
        child_id = device_id + '/' + child_name
        property_access_point = self._edts['devices'][device_id]['children']\
                                                                [child_name]
        self._inject_cell(keys, property_access_point, child_id)

        # Update alias struct if needed
        if property_path.startswith('alias'):
            self.insert_alias(property_value, child_id)

    ##
    # @brief Insert property value for the device of the given device id.
    #
    # @param device_id
    # @param property_path Path of the property to access
    #                      (e.g. 'reg/0', 'interrupts/prio', 'label', ...)
    # @param property_value value
    #
    def insert_device_property(self, device_id, property_path, property_value):

        # special properties
        if property_path.startswith('compatible/') \
           and not property_path.startswith(('compatible/count',
                                             'compatible/index',
                                             'compatible/match')):
            self._update_device_compatible(device_id, property_value)
        if property_path.startswith('alias'):
            aliased_device = device_id
            if 'children' in property_path:
                # device_id is the parent_id
                # property_path is children/device_id/alias
                aliased_device = property_path.split('/')[1]
            self.insert_alias(property_value, aliased_device)

        # normal property management
        if device_id not in self._edts['devices']:
            self._edts['devices'][device_id] = dict()
            self._edts['devices'][device_id]['device-id'] = device_id
        if property_path == 'device-id':
            # already set
            return
        keys = property_path.strip("'").split('/')
        property_access_point = self._edts['devices'][device_id]

        self._inject_cell(keys, property_access_point, property_value)

    ##
    # @brief Write json file
    #
    # @param file_path Path of the file to write
    #
    def save(self, file_path):
        with Path(file_path).open(mode="w", encoding="utf-8") as save_file:
            json.dump(self._edts, save_file, indent = 4, sort_keys=True)

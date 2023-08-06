# Copyright (c) 2018 Linaro Limited
# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from collections.abc import Mapping

from .consumer import EDTSConsumerMixin
from .provider import EDTSProviderMixin
from .extractor import EDTSExtractorMixin

##
# @brief Extended DTS database
#
# Database schema:
#
# @code
# _edts dict(
#   'aliases': dict(alias) : sorted list(device-id)),
#   'chosen': dict(chosen),
#   'devices':  dict(device-id :  device-struct),
#   'compatibles':  dict(compatible : sorted list(device-id)),
#   ...
# )
#
# device-struct dict(
#   'device-id' : device-id,
#   'compatible' : list(compatible) or compatible,
#   'label' : label,
#   '<property-name>' : property-value
# )
#
# property-value
#   for "boolean", "string", "int" -> string
#   for 'array', "string-array", "uint8-array" -> dict(index : string)
#   for "phandle-array" -> dict(index : device-id)
#
# @endcode
#
# Database types:
#
# - device-id: opaque id for a device (do not use for other purposes),
# - compatible: any of ['st,stm32-spi-fifo', ...] - 'compatibe' from <binding>.yaml
# - label: any of ['UART_0', 'SPI_11', ...] - label directive from DTS
#
class EDTSDb(EDTSConsumerMixin, EDTSProviderMixin, EDTSExtractorMixin, Mapping):

    def __init__(self, *args, **kw):
        self._edts = dict(*args, **kw)
        # setup basic database schema
        for edts_key in ('info', 'devices', 'compatibles', 'aliases', 'chosen'):
            if not edts_key in self._edts:
                self._edts[edts_key] = dict()

    def __getitem__(self, key):
        return self._edts[key]

    def __iter__(self):
        return iter(self._edts)

    def __len__(self):
        return len(self._edts)


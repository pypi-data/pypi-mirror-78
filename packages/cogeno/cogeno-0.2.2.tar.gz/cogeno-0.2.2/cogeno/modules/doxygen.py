# Copyright (c) 2018..2020 Bobby Noelte
# SPDX-License-Identifier: Apache-2.0

import wurfapi

import cogeno

class DoxygenDB(object):
    pass







##
# @brief Get doxygen database prepared for cogeno use.
#
# @param force_extract force extraction from Kconfig file if available
# @return config properties database.
def doxygen(force_extract = False):
    if not hasattr(cogeno, '_doxgendb'):
        # Make the config database a hidden attribute of the generator
        cogeno._doxygendb = None
    
    
    return cogeno._doxygendb

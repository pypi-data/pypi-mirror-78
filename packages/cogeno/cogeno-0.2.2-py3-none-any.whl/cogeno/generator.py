# Copyright 2004-2016, Ned Batchelder.
#           http://nedbatchelder.com/code/cog
# Copyright (c) 2018 Bobby Noelte.
#
# SPDX-License-Identifier: MIT

import sys
import os
import re
import imp
import inspect

from pathlib import Path

##
# Make relative import work also with __main__
if __package__ is None or __package__ == '':
    # use current directory visibility
    from context import Context, ContextMixin
    from options import Options, OptionsMixin
    from lock import LockMixin
    from inlinegen import InlineGenMixin
    from pygen import PyGenMixin
    from jinja2gen import Jinja2GenMixin
    from paths import PathsMixin
    from stdmodules import StdModulesMixin
    from include import IncludeMixin
    from log import LogMixin
    from error import ErrorMixin, Error
    from output import OutputMixin
    from importmodule import ImportMixin
    from redirectable import RedirectableMixin
else:
    # use current package visibility
    from .context import Context, ContextMixin
    from .options import Options, OptionsMixin
    from .lock import LockMixin
    from .inlinegen import InlineGenMixin
    from .pygen import PyGenMixin
    from .jinja2gen import Jinja2GenMixin
    from .paths import PathsMixin
    from .stdmodules import StdModulesMixin
    from .include import IncludeMixin
    from .log import LogMixin
    from .error import ErrorMixin, Error
    from .output import OutputMixin
    from .importmodule import ImportMixin
    from .redirectable import RedirectableMixin

class CodeGenerator(ContextMixin, OptionsMixin, LockMixin, InlineGenMixin,
                    PyGenMixin, Jinja2GenMixin,
                    PathsMixin, StdModulesMixin,
                    IncludeMixin, LogMixin, ErrorMixin, OutputMixin,
                    ImportMixin, RedirectableMixin):

    # The cogeno module
    cogeno_module = None

    # Stack of module module states
    cogeno_module_states = []

    ##
    # @brief Magic mumbo-jumbo so that imported Python modules
    #        can say "import cogeno" and get our state.
    #
    # Make us the module.
    @classmethod
    def _init_cogeno_module(cls):
        if cls.cogeno_module is None:
            cls.cogeno_module = imp.new_module('cogeno')
            cls.cogeno_module.path = []
        sys.modules['cogeno'] = cls.cogeno_module

    ##
    # @brief Save our state to the "cogeno" module.
    #
    # Prepare to restore the current state before saving
    # to the module
    def _set_cogeno_module_state(self):
        restore_state = {}
        module_states = self.cogeno_module_states
        module = self.cogeno_module
        # Code generator state
        restore_state['_context'] = getattr(module, '_context', None)
        module._context = self._context
        # Paths
        restore_state['module_path'] = module.path[:]
        restore_state['sys_path'] = sys.path[:]
        # CodeGenerator methods (& classes) that are relevant to templates
        # Look for the Mixin classes.
        for base_cls in inspect.getmro(CodeGenerator):
            if "Mixin" in base_cls.__name__:
                for member_name, member_value in inspect.getmembers(base_cls):
                    if member_name.startswith('_'):
                        continue
                    if inspect.isroutine(member_value) \
                       or inspect.isclass(member_value):
                        restore_state[member_name] = \
                            getattr(module, member_name, None)
                        setattr(module, member_name,
                            getattr(self, member_name))
        # Generator method(s)
        for member_name in ('cogeno_state',):
            restore_state[member_name] = getattr(module, member_name, None)
            setattr(module, member_name, getattr(self, member_name))
        module_states.append(restore_state)

    def _restore_cogeno_module_state(self):
        module_states = self.cogeno_module_states
        module = self.cogeno_module
        restore_state = module_states.pop()
        # Paths
        sys.path = restore_state['sys_path']
        module.path = restore_state['module_path']
        # Code generator state
        module._context = restore_state['_context']
        # CodeGenerator methods (& classes) that are relevant to templates
        # Look for the Mixin classes.
        for base_cls in inspect.getmro(CodeGenerator):
            if "Mixin" in base_cls.__name__:
                for member_name, member_value in inspect.getmembers(base_cls):
                    if member_name.startswith('_'):
                        continue
                    if inspect.isroutine(member_value) \
                       or inspect.isclass(member_value):
                        setattr(module, member_name, restore_state[member_name])
        # Generator method(s)
        for member_name in ('cogeno_state',):
            setattr(module, member_name, restore_state[member_name])

    def __init__(self):
        # the actual generation context
        self._context = None
        # Create the cogeno module if not available
        self._init_cogeno_module()

    ##
    # @brief evaluate context
    #
    # Inserts the context outstring in the current context
    #
    # @param context The context to evaluate
    # @return outstring created by the context - jinja2 needs that
    def _evaluate_context(self, context):
        self.context_enter(context)

        if self.context().script_is_inline():
            self._inline_evaluate()
        elif self.context().script_is_python():
            self._python_evaluate()
        elif self.context().script_is_jinja2():
            self._jinja2_evaluate()
        else:
            # This should never happen
            self.error("Context '{}' with unknown script type '{}' for evaluation."
                       .format(self.context(), self.context().script_type()),
                       frame_index = -2)

        return self.context_exit()

    ##
    # @brief numeric cogeno state id
    def cogeno_state(self):
        return len(self.cogeno_module_states)

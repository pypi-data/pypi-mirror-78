# -*- coding: utf-8 -*-
# (c) 2020 Martin Wendt and contributors; see https://github.com/mar10/stressor-ps
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
"""
"""
import logging

import psutil

__version__ = "0.0.3"

logger = logging.getLogger("stressor")


def register(activity_base, macro_base, arg_parser, **kwargs):

    class PsAllocActivity(activity_base):
        """Define a new activity named 'PsAlloc'.

        The activity is autoamtically registered by the plugin loader, because
        it becomes a known subclass of `activity_base`.
        The name 'PsAlloc' is automatically derrived from the class name.

        Examples:
            sequences:
                main:
                    # Allocate 1 GiB memory per session
                    - activity: PsAlloc
                      allocate_mb: 1024
                      per_session: true
        """
        _mandatory_args = None
        _known_args = {"allocate_mb", "per_session"}
        _info_args = ("name", "allocate_mb")

        def __init__(self, config_manager, **activity_args):
            """The contructor is only instantiated once and shared among sessions."""
            super().__init__(config_manager, **activity_args)
            if "allocate_mb" not in activity_args:
                raise RuntimeError("Missing option 'allocate_mb'")
            self.memory_chunks = []
            return

        def execute(self, session, **expanded_args):
            """"""
            MB = 1024 * 1024
            allocate_mb = int(expanded_args.get("allocate_mb", 0))
            allocate = MB * allocate_mb
            per_session = expanded_args.get("per_session", False)

            if self.memory_chunks and not per_session:
                return True

            logger.info("PsAlloc allocating {:,} bytes".format(allocate))
            chunk = "*" * allocate
            self.memory_chunks.append(chunk)
            return True

    return


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

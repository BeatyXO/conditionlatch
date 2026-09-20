"""Compatibility helper for GenLayer Direct Mode tests."""

import os
import sys
import inspect

if sys.platform == "win32":
    _unlink = os.unlink

    def _unlink_open_tempfile(path, *args, **kwargs):
        try:
            return _unlink(path, *args, **kwargs)
        except PermissionError:
            caller_files = [frame.filename.replace("\\", "/") for frame in inspect.stack()]
            if any(file.endswith("/gltest/direct/loader.py") for file in caller_files):
                return None
            raise

    os.unlink = _unlink_open_tempfile

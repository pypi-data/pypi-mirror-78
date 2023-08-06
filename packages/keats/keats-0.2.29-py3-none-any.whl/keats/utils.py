import json
import os
import shutil
import tempfile
from os.path import abspath
from os.path import isfile


class TemporaryPath:
    def __init__(self, path):
        self.path = path
        self.existed = isfile(path)

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if not self.existed and isfile(self.path):
            os.remove(self.path)


class SafeFileWriter:
    """A safe temporary file will be written.

    If no exceptions occur, the file will be copied to the location in
    the path. Otherwise, the temp file will be deleted.
    """

    def __init__(self, path, mode="w"):
        self.path = abspath(path)
        prefix = ""
        suffix = ".safe.backup"
        _, self.tmp_path = tempfile.mkstemp(prefix=prefix, suffix=suffix)
        self.file = None
        self.mode = mode

    def __enter__(self):
        self.file = open(self.tmp_path, self.mode)
        return self.file

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        if not exception_type:
            shutil.copyfile(self.tmp_path, self.path)
        os.remove(self.tmp_path)


def write_safe_file(path, txt, comparator=None, mode="w"):
    """Content is safely written.

    If content is the same as existing content, do nothing.
    """
    do_write = True
    if isfile(path):
        existing = open(path, "r").read()
        if comparator is None:

            def comparator(txt1, txt2):
                return txt1.strip() == txt2.strip()

        elif comparator == "json":

            def comparator(txt1, txt2):
                return json.loads(txt1) == json.loads(txt2)

        if comparator(existing, txt):
            do_write = False
    if do_write:
        with SafeFileWriter(path, mode) as f:
            f.write(txt)
        return True
    return False


def writelines_safe_file(path, lines, comparator=None, mode="w"):
    """Content is safely written.

    If content is the same as existing content, do nothing.
    """
    return write_safe_file(path, "\n".join(lines), comparator=comparator, mode=mode)

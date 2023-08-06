# -*- coding: utf-8 -*-

import os
import datetime
import time
import tempfile
import shutil
from .randomutils import uuid4

def mkdir(folder):
    os.makedirs(folder, exist_ok=True)
    return os.path.exists(folder) and os.path.isdir(folder)

def rm(filename):
    """Make sure a file or a directory has been deleted.
    """
    if os.path.exists(filename):
        if os.path.isfile(filename):
            os.unlink(filename)
        else:
            shutil.rmtree(filename, ignore_errors=True, onerror=None)
        return not os.path.exists(filename)
    else:
        return True

def filecopy(src, dst, dst_is_a_folder=False):
    if dst_is_a_folder:
        src_name = os.path.basename(src)
        dst = os.path.join(dst, src_name)
    shutil.copy2(src, dst)

def treecopy(src, dst, keep_src_folder_name=True):
    if keep_src_folder_name:
        src_name = os.path.basename(src)
        dst = os.path.join(dst, src_name)
    shutil.copytree(src, dst)

def copy(src, dst, keep_src_folder_name=True, dst_is_a_folder=False):
    if os.path.exists(src):
        if os.path.isfile(src):
            filecopy(src, dst, dst_is_a_folder)
        else:
            treecopy(src, dst, keep_src_folder_name)

def pathjoin(path1, path2):
    return os.path.join(path1, path2)


def readfile(filename, binary=False, encoding="utf-8"):
    if binary:
        with open(filename, "rb") as fobj:
            return fobj.read()
    else:
        with open(filename, "r", encoding=encoding) as fobj:
            return fobj.read()

def write(filename, data, encoding="utf-8"):
    if isinstance(data, bytes):
        with open(filename, "wb") as fobj:
            fobj.write(data)
    else:
        with open(filename, "w", encoding="utf-8") as fobj:
            fobj.write(data)


def get_temp_workspace(prefix="", makedir=True):
    folder_name = prefix + str(uuid4())
    path = os.path.abspath(os.path.join(tempfile.gettempdir(), folder_name))
    if makedir:
        mkdir(path)
    return path

def rename(filepath, name):
    """Only change filename or directory name, but CAN not change the path, e.g. /a/b.txt -> /a/c.txt is ok, /a/b.txt -> /b/b.txt is NOT ok.
    """
    name = os.path.basename(name)
    folder = os.path.dirname(filepath)
    dst = os.path.abspath(os.path.join(folder, name))
    os.rename(filepath, dst)
    return dst

def move(src, dst):
    os.rename(src, dst)

def file_content_replace(filename, original, replacement, binary=False, encoding="utf-8", recursive=True, ignore_errors=True):
    file_replaced = []
    file_failed = {}

    def replace(filename, original, replacement, binary=False, encoding="utf-8"):
        content = readfile(filename, binary, encoding)
        content = content.replace(original, replacement)
        write(filename, content, encoding)

    if os.path.isfile(filename):
        try:
            replace(filename, original, replacement, binary, encoding)
            file_replaced.append(filename)
        except Exception as error:
            file_failed[path] = error
            if not ignore_errors:
                raise error
    else:
        folder = filename
        for root, dirs, files in os.walk(folder):
            for filename in files:
                path = os.path.abspath(os.path.join(root, filename))
                try:
                    replace(path, original, replacement, binary, encoding)
                    file_replaced.append(path)
                except Exception as error:
                    file_failed[path] = error
                    if not ignore_errors:
                        raise error

    return file_replaced, file_failed

def touch(filename):
    """Make sure a file exists
    """
    if os.path.exists(filename):
        os.utime(filename, (time.time(), time.time()))
    else:
        with open(filename, "wb") as fobj:
            pass
    return os.stat(filename)

def expand(filename):
    """Expand user and expand vars.
    """
    return os.path.abspath(os.path.expandvars(os.path.expanduser(filename)))

def first_exists_file(*filenames):
    """Return the first exists file's abspath. If none file exists, return None.
    """
    for filename in filenames:
        filename = expand(filename)
        if os.path.exists(filename):
            return filename
    return None

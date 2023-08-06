# (c) 2012-2020 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""

Cross-platform supports for reading, writing, copying, deleting, etc... files from S3 or local

.. parsed-literal::

             ,--._______,-.
           ,','  ,    .  ,_`-.
          / /  ,' , _` ``. |  )       `-..
         (,';'""`/ '"`-._ ` `/ ______    \\
           : ,o.-`- ,o.  )`` -'      `---.))
           : , d8b ^-.   '|   `.      `    `.
           |/ __:_     `. |  ,  `       `    \
           | ( ,-.`-.    ;'  ;   `       :    ;
           | |  ,   `.      /     ;      :    \
           ;-'`:::._,`.__),'             :     ;
          / ,  `-   `--                  ;     |
         /  `                   `       ,      |
        (    `     :              :    ,`      |
         `   `.    :     :        :  ,'  `    :
          `    `|-- `     ` ,'    ,-'     :-.-';
          :     |`--.______;     |        :    :
           :    /           |    |         |   \
           |    ;           ;    ;        /     ;
         _/--' |   -hrr-   :`-- /         `_:_:_|
       ,',','  |           |___ \
       `^._,--'           / , , .)
                          `-._,-'
"""

import shutil
import os
from glob import glob
import logging

from newtools.optional_imports import s3fs
from newtools.aws import S3Location
from .doggo import FileDoggo

logger = logging.getLogger("newtools.doggo.fs")


class DoggoFileSystem:
    """
    Implements common file operations using either S3 or local file system depending on whether the path
    begins "s3://"

    """
    __s3fs = None

    def __init__(self, session=None):
        s3fs.S3FileSystem.read_timeout = 600
        self.__s3fs = s3fs.S3FileSystem(session=session)

    @property
    def _s3fs(self):
        """
        S3FS caching does not respect other applications updating S3 so therefore we invalidate
        the cache before using

        :return: the S3FS File system
        """
        self.__s3fs.invalidate_cache()
        return self.__s3fs

    def is_s3(self, path1, path2=None):
        """
        Returns true if the passed path is on S3

        :param path1: the first path to check
        :param path2: the second path to check
        :raises NotImplementedError: if only one of the two paths in on S3
        :return: True if both are S3, False if neither are, and raises an exception for mixed types
        """
        p1_s3 = path1.startswith("s3://")
        p2_s3 = p1_s3 if path2 is None else path2.startswith("s3://")

        if p1_s3 != p2_s3:
            raise NotImplementedError("DoggoFileSystem does not support copying between S3 and local")
        if path2 is not None:
            return path1.startswith("s3://") and path2.startswith("s3://")
        else:
            return path1.startswith("s3://")

    def _check_folders(self, path):
        if not self.is_s3(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def cp(self, source, destination):
        """
        Copies a file, per shutil.copy()

        :param source: source path
        :param destination: destination path
        :raises NotImplementedError: if only one of the two paths in on S3
        """
        if self.is_s3(source, destination):
            return self._s3fs.cp(source, destination)
        else:
            self._check_folders(destination)
            return shutil.copy(source, destination)

    def mv(self, source, destination):
        """
        Moves a file per shutil.move()

        :param source: source path
        :param destination: destination path
        :raises NotImplementedError: if only one of the two paths in on S3
        """
        if self.is_s3(source, destination):
            return self._s3fs.mv(source, destination)
        else:
            self._check_folders(destination)
            return shutil.move(source, destination)

    def exists(self, path):
        """
        Returns true if a path exists, per os.path.exists()

        :param path: the path to check
        :return: True if the path exists, otherwise False
        """
        if self.is_s3(path):
            return self._s3fs.exists(path)
        else:
            return os.path.exists(path)

    def size(self, path):
        """
        Returns the size of a file per os.path.getsize()

        :param path: the path to check
        :return: the size of the file at this path
        """
        if self.is_s3(path):
            return self._s3fs.size(path)
        else:
            return os.path.getsize(path)

    def rm(self, path):
        """
        Removes a file, per os.remove()

        :param path: the file to remove
        """
        if self.is_s3(path):
            return self._s3fs.rm(path)
        else:
            return os.remove(path)

    def glob(self, glob_string):
        """
        Searched for a file per glob.glob(recursive=True)


        :param glob_string: the path to search
        :return:
        """
        if self.is_s3(glob_string):
            return [S3Location(a) for a in self._s3fs.glob(glob_string)]
        else:
            return glob(glob_string, recursive=True)

    def open(self, path, mode, *args, **kwargs):
        """
        Opens a file, per open()

        :param path: the path to open
        :param mode: the mode to open in
        :param args: any arguments in the FileDoggo class
        :param kwargs: any keyword arguments for the FileDoggo class
        :return: a file handle
        """
        if "w" in mode:
            self._check_folders(path)
        return FileDoggo(path, mode, *args, **kwargs)

    def join(self, path, *paths):
        """
        Joins to paths per os.path.join()
        :param path: the first path
        :param paths: the paths to joins
        :return:
        """
        if self.is_s3(path):
            return S3Location(path).join(*paths)
        else:
            return os.path.join(path, *paths)

    def split(self, path):
        """
        Splits a path into prefix and file, per os.path.split()
        :param path:
        :return:
        """
        if self.is_s3(path):
            loc = S3Location(path)
            if loc.prefix is not None:
                return S3Location(loc.bucket).join(loc.prefix), loc.file
            else:
                return S3Location(loc.bucket), loc.file
        else:
            return os.path.split(path)

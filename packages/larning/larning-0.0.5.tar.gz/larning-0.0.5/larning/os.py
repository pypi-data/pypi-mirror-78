from collections.abc import Callable
from abc import ABC, abstractmethod, abstractproperty
from pydantic import validate_arguments
from typing import Iterable
from larning.strings_i import concatenate_with_separation
from subprocess import check_output, STDOUT, run, CompletedProcess, PIPE
from os import environ, system, chdir, getcwd
from os.path import exists, normpath, isabs, expandvars
from larning.property import with_property
from sys import stdout, stderr


@with_property("exit_code", "stdout", "stderr")
class Proc(Callable):
    @property
    def _command(self) -> str:
        return concatenate_with_separation(self._args, " ")

    @validate_arguments
    def __init__(self, *args: str, wd_path: str = None, shell=False, env=None):
        self._shell, self._env, = shell, env
        self._args = [expandvars(arg) for arg in args]
        self._wd = Directory(getcwd()) if wd_path is None else Directory(wd_path)

    def __str__(self) -> str:
        return concatenate_with_separation([self._wd.path, self._command], "$ ")

    def __call__(self) -> "Proc":
        args = self._command if self._shell else self._args
        with self._wd:
            p: CompletedProcess = run(
                args, stdout=stdout, stderr=STDOUT, env=self._env, shell=self._shell,
            )
            self.stdout, self.stderr, self.exit_code = (
                "p.stdout.decode()",
                "p.stderr.decode()",
                p.returncode,
            )
            try:
                p.check_returncode()
            except Exception as e:
                print(f"exitcode=={self.exit_code}\nstdout=={self.stdout}\nstderr=={self.stderr}")
                raise e
        return self


@with_property("path")
class VirtualDiskComponent(ABC, Callable):
    @validate_arguments
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @validate_arguments
    def path_setter(self, path: str):
        self._path = normpath(path)


class Directory(VirtualDiskComponent):
    def __call__(self):
        chdir(self.path)

    def __enter__(self):
        self._past_path = getcwd()
        chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self._past_path)

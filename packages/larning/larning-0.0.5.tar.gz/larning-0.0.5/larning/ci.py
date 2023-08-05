from collections.abc import Iterable
from larning.property import with_property
from larning.abc import Namable, Printable, ContextManager
from collections.abc import Sequence
from collections.abc import Callable as aCallable
from typing import Callable as tCallable
from typing import Any
from pydantic import validate_arguments
from abc import ABCMeta
from larning.metaclass import CollectorType
from larning.os import Proc
from typing import Union
from larning.strings import func_to_str, concatenate_with_separation
from contextlib import contextmanager
from sys import argv
from shutil import rmtree
from os.path import isdir, exists
from os import mkdir

AbstractCollectorMetaclass = type("AbstractCollectorMetaclass", (CollectorType, ABCMeta), {})


class InputVariable(
    Namable, Printable, metaclass=AbstractCollectorMetaclass,
):
    def __init__(self, name: str):
        self._name, self._value = name, None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        if self._value is None:
            self._value = input(str(self) + ":=")
        return self._value

    @staticmethod
    def convert_InputVariables(args, kwargs, func: tCallable[["InputVariable"], Any]):
        args = [func(arg) if isinstance(arg, InputVariable) else arg for arg in args]
        kwargs = {key: func(value) if isinstance(value, InputVariable) else value for key, value in kwargs.items()}
        return args, kwargs

    def __str__(self):
        return "<@" + self._name + "@>" if self._value is None else self._value

    class Factory:
        def __getattr__(self, name):
            try:
                return InputVariable[name]
            except IndexError:
                return InputVariable(name)


class Task(
    Namable, Printable, aCallable, metaclass=AbstractCollectorMetaclass,
):
    @validate_arguments
    def __init__(self, func: tCallable, args=None, kwargs=None, name: Union[str, None] = None):
        self._func, self._args, self._kwargs, self._name, = func, args, kwargs, name
        self._args = [] if self._args is None else self._args
        self._kwargs = dict() if self._kwargs is None else self._kwargs

    def __str__(self):
        return self.name + "->" + func_to_str(self._func, *self._args, **self._kwargs)

    def __call__(self):
        args, kwargs = InputVariable.convert_InputVariables(self._args, self._kwargs, lambda x: x.value)
        return self._func(*args, **kwargs)

    @property
    def name(self):
        return self._name

    class Factory:
        def __setattr__(self, name, l: list):
            args, kwargs = [], {}
            for i in l:
                if isinstance(i, Sequence):
                    args = i
                if isinstance(i, dict):
                    kwargs = i
            Task(l[0], args, kwargs, name=name)

        def __getattr__(self, name):
            return Task[name]


class ProcTask(Task):
    def __init__(self, args=None, kwargs=None, name: Union[str, None] = None):
        self._args, self._kwargs, self._name, = args, kwargs, name
        self._args = [] if self._args is None else self._args
        self._kwargs = dict() if self._kwargs is None else self._kwargs

    def __str__(self):
        args, kwargs = InputVariable.convert_InputVariables(self._args, self._kwargs, lambda x: str(x))
        return self.name + "->" + str(Proc(*args, **kwargs))

    def __call__(self):
        args, kwargs = InputVariable.convert_InputVariables(self._args, self._kwargs, lambda x: x.value)
        p = Proc(*args, **kwargs)()
        return concatenate_with_separation([p.exit_code, p.stdout, p.stderr], "->")

    class Factory:
        def __setattr__(self, name, l: list):
            ProcTask(args=l[1:], kwargs={"wd_path": l[0]}, name=name)

        def __getattr__(self, name):
            return ProcTask[name]


class Script(
    Namable, Printable, aCallable, Iterable, metaclass=AbstractCollectorMetaclass,
):
    def __init__(self, *tasks: Task, name: Union[str, None] = None):
        self._tasks, self._name = tasks, name

    def __iter__(self):
        return iter(self._tasks)

    @property
    def name(self):
        return self._name

    def __str__(self):
        sep = "\n\t\t"
        return self.name + ":" + sep + concatenate_with_separation([str(task) for task in self._tasks], sep)

    def __call__(self):
        ret = []
        print(f"Script |{self.name}| is running:")
        for task in self._tasks:
            if input(f"Press Enter to run |{str(task)}| or s to skip actual task...") == "s":
                continue
            t = task()
            print(task.name + "==" + str(t)), ret.append(t)
        return ret

    class Factory:
        def __setattr__(self, name, l: list):
            Script(*l, name=name)


@contextmanager
def ci_manager():
    yield InputVariable.Factory(), Task.Factory(), ProcTask.Factory(), Script.Factory()
    template = "there is not any script with name: {}"
    if len(argv) > 1:
        for arg in argv[1:]:
            if arg in Script:
                Script[arg]()
            else:
                raise NameError(template.format(arg))
    else:
        [print(s) for s in Script]
        name = input("Select a Script: ")
        if name in Script:
            Script[name]()
        else:
            raise NameError(template.format(name))


def rmdirs(*paths):
    for path in paths:
        if isdir(path):
            rmtree(path)


def mkdirs(*paths):
    for path in paths:
        if not exists(path):
            mkdir(path)

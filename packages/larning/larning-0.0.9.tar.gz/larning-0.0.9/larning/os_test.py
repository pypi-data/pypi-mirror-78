from larning.os import Proc, Directory
from larning.testing import name
from os import environ
from pytest import raises
from subprocess import CalledProcessError
from os import chdir, getcwd
from os.path import split, expandvars

original_wd = getcwd()


def setup_function(func):
    chdir(original_wd)


@name(Directory.__call__, 1, globals())
def _():
    Directory("/dev")()
    assert getcwd() == "/dev"


@name(Directory.__enter__, 1, globals())
def _():
    with Directory("/dev"):
        assert getcwd() == "/dev"
    assert getcwd() == original_wd


@name(expandvars, 1, globals())
def _():
    assert expandvars("$PATH").startswith("/")


@name(Proc._command.fget, 1, globals())
def _():
    assert Proc("echo", 1)._command == "echo 1"


@name(Proc.__init__, "_args", globals())
def _():
    assert Proc("echo", 1)._args == ["echo", "1"]
    assert Proc("$PATH")._args[0][0] == "/"


@name(Proc.__str__, 1, globals())
def _():
    assert str(Proc("echo", 1)) == getcwd() + "$ echo 1"


@name(Proc, "properties", globals())
def _():
    basic = Proc("echo", 1)()
    shell = Proc("echo", 1, shell=True)()
    assert basic.exit_code == 0 == shell.exit_code


@name(Proc.__call__, "error", globals())
def _():
    with raises(FileNotFoundError):
        Proc("ech")()
    with raises(FileNotFoundError):
        Proc("set")()
    with raises(CalledProcessError):
        Proc("ech", shell=True)()
    assert Proc("set", shell=True)().exit_code == 0


@name(Proc.__call__, "dirchange", globals())
def _():
    original_wd = getcwd()
    Proc("cd", "..", ";", "pwd", shell=True)()
    assert original_wd == getcwd()

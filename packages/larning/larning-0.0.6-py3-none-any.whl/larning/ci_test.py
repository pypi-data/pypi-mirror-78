from larning.testing import name, input_manager, argv_manager
from larning.ci import InputVariable, Task, Script, ProcTask, ci_manager
from pytest import raises
from pydantic import ValidationError
from sys import argv
from unittest.mock import MagicMock
from larning.os import Proc


@name(Script, "1_", globals())
def _():
    ...


def setup_function():
    InputVariable.clear(), Task.clear(), ProcTask.clear(), Script.clear()


@name(InputVariable.__init__, 0, globals())
def _():
    a = InputVariable("a")
    assert a._name == "a" and a._value == None and a in InputVariable


@name(InputVariable.__str__, 0, globals())
def _():
    a = InputVariable("a")
    assert str(a) == "<@a@>"


@name(InputVariable.value.fget, 0, globals())
def _():
    a = InputVariable("a")
    a._value = 1
    assert a.value == 1
    a = InputVariable("a")
    with input_manager("A"):
        assert a.value == "A"


@name(InputVariable.Factory, 0, globals())
def _():
    InputVariable.clear()
    InputVariableFactory = InputVariable.Factory()
    a = InputVariableFactory.a
    b = InputVariableFactory.b
    a2 = InputVariableFactory.a
    assert a is a2
    assert InputVariable._objects == {a, b}


@name(Task.__str__, 0, globals())
def _():
    t = Task(lambda: 1, (1,), {"a": "a"}, name="name")
    assert str(t) == "name-><lambda>(1, a='a')"


@name(Task.__str__, InputVariable.__name__, globals())
def _():
    name = InputVariable("name")
    t = Task(lambda: 1, (name,), name="name")
    assert str(t) == "name-><lambda>(<@name@>)"
    name._value = "a"
    assert str(t) == "name-><lambda>(a)"


@name(Task.__call__, InputVariable.__name__, globals())
def _():
    t = Task((lambda x, y=None: x + y), [InputVariable("x")], {"y": InputVariable("y")}, name="name",)
    with input_manager("x\ny"):
        assert t() == "xy"
    assert t() == "xy"


@name(Task.Factory, 1, globals())
def _():
    TaskFactory = Task.Factory()
    TaskFactory.a = [lambda x: x, [1], {}]
    assert TaskFactory.a.name == "a" and isinstance(TaskFactory.a, Task) and TaskFactory.a() == 1
    TaskFactory.b = [lambda: 2]
    assert TaskFactory.b.name == "b" and TaskFactory.b() == 2


@name(ProcTask, 1, globals())
def _():
    assert len(Task) == 0 == len(ProcTask)
    Task(lambda: 1)
    assert len(Task) == 1 and len(ProcTask) == 0
    ProcTask()
    assert len(Task) == 1 and len(ProcTask) == 1
    assert hasattr(ProcTask, "_objects")


@name(ProcTask.__str__, 1, globals())
def _():
    assert str(ProcTask(["echo", "a", InputVariable.Factory().a], {"wd_path": "/home"}, "ProcName",)) == "ProcName->/home$ echo a <@a@>"


@name(ProcTask.__call__, 1, globals())
def _():
    with input_manager("a"):
        p = Proc()
        p._exit_code = 0
        assert ProcTask(["echo", "a", InputVariable.Factory().a], {"wd_path": "/home"}, "ProcName",)() == p.exit_msg


@name(ProcTask.Factory.__setattr__, 1, globals())
def _():
    pF = ProcTask.Factory()
    assert len(ProcTask) == 0
    pF.ProcName = ["/home", "echo", "a", InputVariable.Factory().a]
    assert len(ProcTask) == 1
    assert str(pF.ProcName) == "ProcName->/home$ echo a <@a@>"


@name(Script.__str__, 1, globals())
def _():
    assert "name:\n\t\t1-><lambda>()\n\t\t2-><lambda>()" == str(Script(Task(lambda: 1, name="1"), Task(lambda: 2, name="2"), name="name"))


@name(Script.__call__, 1, globals())
def _():
    with input_manager("\n\n"):
        assert Script(Task(lambda: 1, name="1"), Task(lambda: 2, name="2"), name="name")() == [1, 2]
    with input_manager("\n1\n\n2\n"):
        assert Script(
            Task(lambda x: x, [InputVariable("1")], name="1"), Task(lambda y=None: y, kwargs={"y": InputVariable("2")}, name="2"), name="name",
        )() == ["1", "2"]


@name(ci_manager, "goodargv", globals())
def _():
    with argv_manager("", "script1"):
        with ci_manager() as (iF, tF, pF, sF):
            assert (
                isinstance(iF, InputVariable.Factory) and isinstance(tF, Task.Factory) and isinstance(pF, ProcTask.Factory) and isinstance(sF, Script.Factory)
            )
            sF.script1 = []
            sF.script2 = []
            assert "script1" in Script


@name(ci_manager, "badargv", globals())
def _():
    with argv_manager("", "bad"):
        with raises(NameError):
            with ci_manager() as (iF, tF, pF, sF):
                assert (
                    isinstance(iF, InputVariable.Factory)
                    and isinstance(tF, Task.Factory)
                    and isinstance(pF, ProcTask.Factory)
                    and isinstance(sF, Script.Factory)
                )
                sF.script1 = []
                sF.script2 = []
                assert "script1" in Script


@name(ci_manager, "goodinput", globals())
def _():
    with argv_manager():
        with input_manager("script2"):
            with ci_manager() as (iF, tF, pF, sF):
                assert (
                    isinstance(iF, InputVariable.Factory)
                    and isinstance(tF, Task.Factory)
                    and isinstance(pF, ProcTask.Factory)
                    and isinstance(sF, Script.Factory)
                )
                sF.script1 = []
                sF.script2 = []
                assert "script1" in Script


@name(ci_manager, "badinput", globals())
def _():
    with argv_manager():
        with input_manager("bad"):
            with raises(NameError):
                with ci_manager() as (iF, tF, pF, sF):
                    assert (
                        isinstance(iF, InputVariable.Factory)
                        and isinstance(tF, Task.Factory)
                        and isinstance(pF, ProcTask.Factory)
                        and isinstance(sF, Script.Factory)
                    )
                    sF.script1 = []
                    sF.script2 = []
                    assert "script1" in Script


@name(ci_manager, "call", globals())
def _():
    with argv_manager("", "script1"):
        with ci_manager() as (iF, tF, pF, sF):
            assert (
                isinstance(iF, InputVariable.Factory) and isinstance(tF, Task.Factory) and isinstance(pF, ProcTask.Factory) and isinstance(sF, Script.Factory)
            )
            sF.script1 = []
            sF.script2 = []
            Script.__call__ = MagicMock()
            Script.__call__.assert_not_called()
    Script.__call__.assert_called_once()


@name(Script.Factory.__setattr__, 1, globals())
def _():
    sF = Script.Factory()
    t = Task(lambda x: x, [1], name="name")
    sF.a = [t]
    assert len(Script) == 1 and isinstance(Script["a"], Script)
    for i in Script:
        for j in i:
            assert j.name == "name" and j() == 1

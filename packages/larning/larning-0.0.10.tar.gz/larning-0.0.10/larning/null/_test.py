from larning.testing import name
from larning.null import null_manager


@name(null_manager, 1, globals())
def _():
    with null_manager() as i:
        assert i == None

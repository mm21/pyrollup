from types import ModuleType

__all__ = [
    "rollup",
]


def rollup(*mods: ModuleType) -> list[str]:
    """
    Evaluate and return public API symbols for each submodule, accounting for
    any allow-list and/or block-list provided by the submodule.
    """

    syms: list[str] = []

    # traverse submodules
    for mod in mods:
        all_: list[str] | None = None
        rollup: list[str] | None = None
        nrollup: list[str] | None = None

        allow_list: list[str] = []
        block_list: list[str] = []

        try:
            all_ = mod.__all__
        except AttributeError as e:
            pass

        try:
            rollup = mod.__rollup__
        except AttributeError as e:
            pass

        try:
            nrollup = mod.__nrollup__
        except AttributeError as e:
            pass

        # set allow-list/block-list
        if rollup is not None:
            allow_list = rollup
        elif all_ is not None:
            allow_list = all_

        if nrollup is not None:
            block_list = nrollup

        # evaluate symbols for this submodule
        syms += [sym for sym in allow_list if sym not in block_list]

    return syms

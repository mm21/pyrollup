# pyrollup
Simple mechanism to rollup API symbols to a Python module from its submodules

## Background

Conventionally, a Python package's public API symbols (or at least a subset) are exported from the top-level package. These symbols are typically imported from various submodules in the module hierarchy. This leads to a rather tedious listing of symbols exported (via a module's `__init__.py`) at each level.

For example:

```python
from .submodule_a import ClassA, ClassA2
from .submodule_b import ClassB
from .submodule_c import ClassC

__all__ = [
    ClassA,
    ClassA2
    ClassB,
    ClassC,
]
```

The definition of `__all__` can be omitted, although some schools of thought encourage its use.

## Problem statement

With the above approach, the burden of which symbols are considered public for a given submodule falls on the containing module importing them. In addition, `__all__` must be maintained alongside symbol imports, potentially resulting in duplication.

This can become problematic for complex projects with many nested symbols imported at the top-level package. For example:

```python
from .submodule_a import ClassA, ClassA2
from .submodule_a.submodule_a1 import ClassA1_1, ClassA1_2
from .submodule_a.submodule_a2 import ClassA2_1, ClassA2_2
from .submodule_a.submodule_a3 import ClassA3_1, ClassA3_2
from .submodule_b import ClassB
from .submodule_c import ClassC

__all__ = [
    ClassA,
    ClassA2,
    ClassA1_1,
    ClassA1_2,
    ClassA2_1,
    ClassA2_2,
    ClassA3_1,
    ClassA3_2,
    ClassB,
    ClassC,
]
```

In addition, submodules must similarly maintain their own imports and/or definition of `__all__` if they export symbols from their submodules.

## Proposed solution

Ideally, a module should "rollup" public symbols from its submodules, letting each submodule decide which symbols those are. Submodules should therefore optionally provide an allow-list and block-list to describe which public symbols should be propagated to the parent module.

In other words, a given module should have ownership of:

- Its own public symbols (Python convention)
    - Defined by `__all__`
- Which of those public symbols should be propagated to parent modules (functionality provided by `pyrollup`)
    - Defined by
        - `__rollup__`: allow-list, defaulting to `__all__`
        - `__nrollup__`: block-list, defaulting to `[]`

Then, the example above can be modified as:

```python
from pyrollup import rollup

# import submodules
from . import submodule_a, submodule_b, submodule_c

# import public symbols from each submodule
from .submodule_a import *
from .submodule_b import *
from .submodule_c import *

# export public symbols from each submodule, filtered by allow-list/block-list
__all__ = rollup(submodule_a, submodule_b, submodule_c)
```

This allows a project with a complex module hierarchy to flexibly propagate public symbols from wherever they are defined to the top-level package.

## Downsides

Static analysis tools are unable to evaluate the value of `__all__` since with this approach it is computed dynamically upon import. Therefore, code documentation generator tools using static analysis (e.g. [autoapi](https://github.com/readthedocs/sphinx-autoapi) or [autodoc2](https://github.com/sphinx-extensions2/sphinx-autodoc2)) will fail to detect a module's public symbols.

Tools using the traditional approach of importing the package for which documentation is being generated (e.g. Sphinx's built-in [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)) should have no problem with such dynamic imports.

It is possible to use a "hybrid" approach; the author has had some success with extending [autodoc2](https://github.com/sphinx-extensions2/sphinx-autodoc2) to work with dynamically-evaluated `__all__`. 

TODO: document and generalize this solution

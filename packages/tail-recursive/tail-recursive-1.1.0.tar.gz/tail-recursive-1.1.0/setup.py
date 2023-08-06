# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tail_recursive']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tail-recursive',
    'version': '1.1.0',
    'description': 'Tail recursion with a simple decorator api.',
    'long_description': "![tests](https://github.com/0scarB/tail-recursive/workflows/Tests/badge.svg)\n\nUse the `tail_recursive` decorator to simply define tail recursive functions.\n\nIf you are encountering **maximum recursion depth errors** or **out-of-memory crashes** tail recursion can be a helpful strategy.\n\n### Example\n\n```python\nimport tail_recursive from tail_recursive\n\n\n# Pick a larger value if n is below your system's recursion limit.\nx = 5000\n\n\ndef factorial_without_tail_recursion(n, accumulator=1):\n    if n == 1:\n        return accumulator\n    return factorial_without_tail_recursion(n - 1, n * accumulator)\n\n\ntry:\n    # This will exceed the maximum recursion depth.\n    factorial_without_tail_recursion(x)\nexcept RecursionError:\n    pass\n\n\n@tail_recursive\ndef factorial(n, accumulator=1):\n    if n == 1:\n        return accumulator\n    # It is important that you return the return value of the `tail_call`\n    # method for tail recursion to take effect!\n    return factorial.tail_call(n - 1, n * accumulator)\n\n\n# Implementation with tail recursion succeeds because the function is\n# called sequentially under the hood.\nfactorial(x)\n```\n\nThe `tail_call` method returns an object which stores a function (e.g. `factorial`) and\nits arguments. The function is then lazily evaluated once the object has been returned\nfrom the caller function (in this case also `factorial`). This means that the\nresources in the caller function's scope are free to be garbage collected and that its\nframe is popped from the call stack before we push the returned function on.\n\n## Other Packages\n\nCheck out [tco](https://github.com/baruchel/tco) for an alternative api with extra functionality.\n",
    'author': '0scarB',
    'author_email': 'oscarb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/0scarB/tail-recursive',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elegy',
 'elegy.callbacks',
 'elegy.data',
 'elegy.losses',
 'elegy.metrics',
 'elegy.nn',
 'elegy.regularizers']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.5.0,<2.0.0',
 'deepdish>=0.3.6,<0.4.0',
 'deepmerge>=0.1.0,<0.2.0',
 'dm-haiku>=0.0.2,<0.0.3',
 'jaxlib>=0.1.51,<0.2.0',
 'numpy>=1.19.0,<2.0.0',
 'optax>=0.0.1,<0.0.2',
 'pytest-cov>=2.10.0,<3.0.0',
 'pytest>=5.4.3,<6.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'tables>=3.6.1,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tensorboardx>=2.1,<3.0',
 'toolz>=0.10.0,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'elegy',
    'version': '0.2.2',
    'description': 'Elegy is a Neural Networks framework based on Jax and Haiku.',
    'long_description': '# Elegy\n\n[![PyPI Status Badge](https://badge.fury.io/py/elegy.svg)](https://pypi.org/project/elegy/)\n[![Coverage](https://img.shields.io/codecov/c/github/poets-ai/elegy?color=%2334D058)](https://codecov.io/gh/poets-ai/elegy)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/elegy)](https://pypi.org/project/elegy/)\n[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://poets-ai.github.io/elegy/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/poets-ai/elegy/issues)\n[![Status](https://github.com/poets-ai/elegy/workflows/GitHub%20CI/badge.svg)](https://github.com/poets-ai/elegy/actions?query=workflow%3A"GitHub+CI")\n\n-----------------\n\n_Elegy is a Neural Networks framework based on Jax inspired by Keras and Haiku._  \n\nElegy implements the Keras API but makes changes to play better with Jax and gives more flexibility around [losses and metrics](https://poets-ai.github.io/elegy/guides/modules-losses-metrics/), it also ports Haiku\'s excellent [module system](https://poets-ai.github.io/elegy/guides/module-system/) and makes it easier to use. Elegy is in an early stage, feel free to send us your feedback!\n\n#### Main Features\n\n* **Familiar**: Elegy should feel very familiar to Keras users.\n* **Flexible**: Elegy improves upon the basic Keras API by letting users optionally take more control over the definition of losses and metrics.\n* **Easy-to-use**: Elegy maintains all the simplicity and ease of use that Keras brings with it.\n* **Compatible**: Elegy strives to be compatible with the rest of the Jax ecosystem.\n\nFor more information take a look at the [Documentation](https://poets-ai.github.io/elegy).\n\n## Installation\n\nInstall Elegy using pip:\n```bash\npip install elegy\n```\n\nFor Windows users we recommend the Windows subsystem for linux 2 [WSL2](https://docs.microsoft.com/es-es/windows/wsl/install-win10?redirectedfrom=MSDN) since [jax](https://github.com/google/jax/issues/438) does not support it yet.\n\n## Quick Start\nElegy greatly simplifies the training of Deep Learning models compared to pure Jax where, due to Jax\'s functional nature, users have to do a lot of book keeping around the state of the model. In Elegy you just have to follow 3 basic steps:\n\n**1.** Define the architecture inside an `elegy.Module`:\n```python\nclass MLP(elegy.Module):\n    def call(self, x: jnp.ndarray) -> jnp.ndarray:\n        x = elegy.nn.Linear(300)(x)\n        x = jax.nn.relu(x)\n        x = elegy.nn.Linear(10)(x)\n        return x\n```\nNote that we can define sub-modules on-the-fly directly in the `call` (forward) method.\n\n**2.** Create a `Model` from this module and specify additional things like losses, metrics, and optimizers:\n```python\nmodel = elegy.Model(\n    module=MLP(),\n    loss=[\n        elegy.losses.SparseCategoricalCrossentropy(from_logits=True),\n        elegy.regularizers.GlobalL2(l=1e-5),\n    ],\n    metrics=elegy.metrics.SparseCategoricalAccuracy(),\n    optimizer=optax.rmsprop(1e-3),\n)\n```\n**3.** Train the model using the `fit` method:\n```python\nmodel.fit(\n    x=X_train,\n    y=y_train,\n    epochs=100,\n    steps_per_epoch=200,\n    batch_size=64,\n    validation_data=(X_test, y_test),\n    shuffle=True,\n    callbacks=[elegy.callbacks.TensorBoard("summaries")]\n)\n```\n\nAnd you are done! For more information check out:\n\n\n* Our [Getting Started](https://poets-ai.github.io/elegy/getting-started/) tutorial.\n* Elegy\'s [Documentation](https://poets-ai.github.io/elegy).\n* The [examples](https://github.com/poets-ai/elegy/tree/master/examples) directory.\n* [What is Jax?](https://github.com/google/jax#what-is-jax)\n\n## Why Jax & Elegy?\n\nGiven all the well-stablished Deep Learning framework like TensorFlow + Keras or Pytorch + Pytorch-Lightning/Skorch, it is fair to ask why we need something like Jax + Elegy? Here are some of the reasons why this framework exists.\n\n#### Why Jax?\n\n**Jax** is a linear algebra library with the perfect recipe:\n* Numpy\'s familiar API\n* The speed and hardware support of XLA\n* Automatic Differentiation\n\nThe awesome thing about Jax is that Deep Learning is just a use-case that it happens to excel at but you can use it for most task you would use NumPy for. Jax is so compatible with Numpy that is array type actually inherits from `np.ndarray`.\n\nIn a sense, Jax takes the best of both TensorFlow and Pytorch in a principled manner: while both TF and Pytorch historically converged to the same set of features, their APIs still contain quirks they have to keep for compatibility.\n\n#### Why Elegy?\n\nWe believe that **Elegy** can offer the best experience for coding Deep Learning applications by leveraging the power and familiarity of Jax API, an easy-to-use and succinct Module system, and packaging everything on top of a convenient Keras-like API. Elegy improves upon other Deep Learning frameworks in the following ways:\n\n1. Its hook-based [Module System](https://poets-ai.github.io/elegy/guides/module-system/) makes it easier (less verbose) to write model code compared to Keras & Pytorch since it lets you declare sub-modules, parameters, and states directly on your `call` (forward) method. Thanks to this you get shape inference for free so there is no need for a `build` method (Keras) or propagating shape information all over the place (Pytorch). A naive implementation of `Linear` could be as simple as:\n\n```python\nclass Linear(elegy.Module):\n    def __init__(self, units):\n        super().__init__()\n        self.units = units\n\n    def call(self, x):\n        w = elegy.get_parameter("w", [x.shape[-1], self.units], initializer=jnp.ones)\n        b = elegy.get_parameter("b", [self.units], initializer=jnp.ones)\n\n        return jnp.dot(x, w) + b\n```\n2. It has a very flexible system for defining the inputs for [losses and metrics](https://poets-ai.github.io/elegy/guides/modules-losses-metrics/) based on _dependency injection_ in opposition to Keras rigid requirement to have matching (output, label) pairs, and being unable to use additional information like inputs, parameters, and states in the definition of losses and metrics. \n3. Its hook system preserve\'s [reference information](https://poets-ai.github.io/elegy/guides/module-system/) from a module to its sub-modules, parameters, and states while maintaining a functional API. This is crucial since most Jax-based frameworks like Flax and Haiku tend to loose this information which makes it very tricky to perform tasks like transfer learning where you need to mix a pre-trained models into a new model (easier to do if you keep references).\n\n## Features\n* `Model` estimator class\n* `losses` module\n* `metrics` module\n* `regularizers` module\n* `callbacks` module\n* `nn` layers module\n\nFor more information checkout the **Reference API** section in the [Documentation](https://poets-ai.github.io/elegy).\n\n## Contributing\nDeep Learning is evolving at an incredible pace, there is so much to do and so few hands. If you wish to contibute anything from a loss or metric to a new awesome feature for Elegy just open an issue or send a PR! For more information check out our [Contibuting Guide](https://poets-ai.github.io/elegy/guides/contributing).\n\n## About Us\nWe are some friends passionate about ML.\n\n## License\nApache\n\n## Citing Elegy\n\nTo cite this project:\n\n**BibTeX**\n\n```\n@software{elegy2020repository,\nauthor = {PoetsAI},\ntitle = {Elegy: A Keras-like deep learning framework based on Jax},\nurl = {https://github.com/poets-ai/elegy},\nversion = {0.2.2},\nyear = {2020},\n}\n```\n\nWhere the current *version* may be retrieved either from the `Release` tag or the file [elegy/\\_\\_init\\_\\_.py](https://github.com/poets-ai/elegy/blob/master/elegy/__init__.py) and the *year* corresponds to the project\'s release year.',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://poets-ai.github.io/elegy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

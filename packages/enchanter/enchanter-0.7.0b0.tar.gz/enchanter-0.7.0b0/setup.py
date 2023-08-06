# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enchanter',
 'enchanter.addons',
 'enchanter.addons.layers',
 'enchanter.callbacks',
 'enchanter.engine',
 'enchanter.metrics',
 'enchanter.preprocessing',
 'enchanter.preprocessing.signal',
 'enchanter.tasks',
 'enchanter.utils',
 'enchanter.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['comet_ml>=3.1.3,<4.0.0',
 'numpy>=1.17,<2.0',
 'pandas>=1.0,<2.0',
 'scikit-learn>=0.23,<0.24',
 'tensorboard>=2.1,<3.0',
 'tensorflow-datasets>=3.2.1,<4.0.0',
 'tensorflow>=2.3.0,<3.0.0',
 'torch>=1.6,<2.0',
 'tqdm>=4.41,<5.0']

setup_kwargs = {
    'name': 'enchanter',
    'version': '0.7.0b0',
    'description': 'Enchanter is a library for machine learning tasks for comet.ml users.',
    'long_description': '# Enchanter\n\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/84197fb283924f02a1667cea49dd031a)](https://app.codacy.com/manual/KawashimaHirotaka/enchanter?utm_source=github.com&utm_medium=referral&utm_content=khirotaka/enchanter&utm_campaign=Badge_Grade_Dashboard)\n[![CI testing](https://github.com/khirotaka/enchanter/workflows/CI/badge.svg)](https://github.com/khirotaka/enchanter/actions)\n[![Build & Publish](https://github.com/khirotaka/enchanter/workflows/Build%20&%20Publish/badge.svg)](https://github.com/khirotaka/enchanter/actions)\n[![Documentation Status](https://readthedocs.org/projects/enchanter/badge/?version=latest)](https://enchanter.readthedocs.io/ja/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/enchanter?color=brightgreen)](https://pypi.org/project/enchanter/)\n[![license](https://img.shields.io/github/license/khirotaka/enchanter?color=light)](LICENSE)\n[![Using PyTorch](https://img.shields.io/badge/PyTorch-red.svg?labelColor=f3f4f7&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMjU2cHgiIGhlaWdodD0iMzEwcHgiIHZpZXdCb3g9IjAgMCAyNTYgMzEwIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIj4KICAgIDxnPgogICAgICAgIDxwYXRoIGQ9Ik0yMTguMjgxMDM3LDkwLjEwNjQxMiBDMjY4LjU3Mjk4OCwxNDAuMzk4MzYzIDI2OC41NzI5ODgsMjIxLjA3NTAzNCAyMTguMjgxMDM3LDI3MS43MTYyMzUgQzE2OS4wMzY4MzUsMzIyLjAwODE4NiA4OC4wMTA5MTQxLDMyMi4wMDgxODYgMzcuNzE4OTYzMiwyNzEuNzE2MjM1IEMtMTIuNTcyOTg3NywyMjEuNDI0Mjg0IC0xMi41NzI5ODc3LDE0MC4zOTgzNjMgMzcuNzE4OTYzMiw5MC4xMDY0MTIgTDEyNy44MjUzNzUsMCBMMTI3LjgyNTM3NSw0NS4wNTMyMDYgTDExOS40NDMzODMsNTMuNDM1MTk3OCBMNTkuNzIxNjkxNywxMTMuMTU2ODg5IEMyMi4wMDI3Mjg1LDE1MC4xNzczNTMgMjIuMDAyNzI4NSwyMTAuOTQ2Nzk0IDU5LjcyMTY5MTcsMjQ4LjY2NTc1NyBDOTYuNzQyMTU1NSwyODYuMzg0NzIgMTU3LjUxMTU5NiwyODYuMzg0NzIgMTk1LjIzMDU1OSwyNDguNjY1NzU3IEMyMzIuOTQ5NTIzLDIxMS42NDUyOTMgMjMyLjk0OTUyMywxNTAuODc1ODUzIDE5NS4yMzA1NTksMTEzLjE1Njg4OSBMMjE4LjI4MTAzNyw5MC4xMDY0MTIgWiBNMTczLjIyNzgzMSw4NC41MTg0MTc1IEMxNjMuOTY5MzM4LDg0LjUxODQxNzUgMTU2LjQ2Mzg0Nyw3Ny4wMTI5MjYzIDE1Ni40NjM4NDcsNjcuNzU0NDMzOCBDMTU2LjQ2Mzg0Nyw1OC40OTU5NDEzIDE2My45NjkzMzgsNTAuOTkwNDUwMiAxNzMuMjI3ODMxLDUwLjk5MDQ1MDIgQzE4Mi40ODYzMjMsNTAuOTkwNDUwMiAxODkuOTkxODE0LDU4LjQ5NTk0MTMgMTg5Ljk5MTgxNCw2Ny43NTQ0MzM4IEMxODkuOTkxODE0LDc3LjAxMjkyNjMgMTgyLjQ4NjMyMyw4NC41MTg0MTc1IDE3My4yMjc4MzEsODQuNTE4NDE3NSBaIiBmaWxsPSIjRUU0QzJDIj48L3BhdGg+CiAgICA8L2c+Cjwvc3ZnPgo=)](https://pytorch.org/)\n\nEnchanter is a library for machine learning tasks for comet.ml users.\n\n## Installation\nTo install the stable release.\n```shell script\npip install enchanter\n```\n\nor\n\nTo install the latest(unstable) release. \n```shell script\npip install git+https://github.com/khirotaka/enchanter.git\n```\n\nIf you want to install with a specific branch, you can use the following.\n```shell script\n# e.g.) Install enchanter from develop branch.\npip install git+https://github.com/khirotaka/enchanter.git@develop\n```\n\n## Documentation\n*   [API Reference](https://enchanter.readthedocs.io/ja/latest/)\n*   [Tutorial](https://enchanter.readthedocs.io/ja/latest/tutorial/modules.html)\n\n## Getting Started\nTry your first Enchanter Program\n\n### Training Neural Network\n\n```python\nfrom comet_ml import Experiment\nimport torch\nimport enchanter\n\nmodel = torch.nn.Linear(6, 10)\noptimizer = torch.optim.Adam(model.parameters())\n\nrunner = enchanter.tasks.ClassificationRunner(\n    model, \n    optimizer,\n    criterion=torch.nn.CrossEntropyLoss(),\n    experiment=Experiment()\n)\n\nrunner.add_loader("train", train_loader)\nrunner.train_config(epochs=10)\nrunner.run()\n```\n\n### Hyper parameter searching using Comet.ml\n\n```python\nfrom comet_ml import Optimizer\n\nimport torch\nimport torch.nn as nn\nimport torch.optim as optim\nfrom sklearn.datasets import load_iris\n\nimport enchanter.tasks as tasks\nimport enchanter.addons as addons\nimport enchanter.addons.layers as layers\nfrom enchanter.utils import comet\n\n\nconfig = comet.TunerConfigGenerator(\n    algorithm="bayes",\n    metric="train_avg_loss",\n    objective="minimize",\n    seed=0,\n    trials=1,\n    max_combo=10\n)\n\nconfig.suggest_categorical("activation", ["addons.mish", "torch.relu", "torch.sigmoid"])\nopt = Optimizer(config.generate())\n\nx, y = load_iris(return_X_y=True)\nx = x.astype("float32")\ny = y.astype("int64")\n\n\nfor experiment in opt.get_experiments():\n    model = layers.MLP([4, 512, 128, 3], eval(experiment.get_parameter("activation")))\n    optimizer = optim.Adam(model.parameters())\n    runner = tasks.ClassificationRunner(\n        model, optimizer=optimizer, criterion=nn.CrossEntropyLoss(), experiment=experiment\n    )\n\n    runner.fit(x, y, epochs=1, batch_size=32)\n```\n\n\n### Training with Mixed Precision\nRunners with defined in `enchanter.tasks` are now support Auto Mixed Precision.  \nWrite the following.\n\n\n```python\nfrom torch.cuda import amp\nfrom enchanter.tasks import ClassificationRunner\n\n\nrunner = ClassificationRunner(...)\nrunner.scaler = amp.GradScaler()\n```\n\n\nIf you want to define a custom runner that supports mixed precision, do the following.\n```python\nfrom torch.cuda import amp\nimport torch.nn.functional as F\nfrom enchanter.engine import BaseRunner\n\n\nclass CustomRunner(BaseRunner):\n    # ...\n    def train_step(self, batch):\n        x, y = batch\n        with amp.autocast():        # REQUIRED\n            out = self.model(x)\n            loss = F.nll_loss(out, y)\n        \n        return {"loss": loss}\n\n\nrunner = CustomRunner(...)\nrunner.scaler = amp.GradScaler()\n```\n\nThat is, you can enable AMP by using `torch.cuda.amp.autocast()` in `.train_step()`, `.val_step()` and `.test_step()`.\n\n## License\n[Apache License 2.0](LICENSE)\n',
    'author': 'Hirotaka Kawashima',
    'author_email': 'khirotaka@vivaldi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://enchanter.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)

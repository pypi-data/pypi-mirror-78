# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canvasutils']

package_data = \
{'': ['*']}

install_requires = \
['canvasapi>=2.0.0,<3.0.0', 'ipywidgets>=7.5.1,<8.0.0']

setup_kwargs = {
    'name': 'canvasutils',
    'version': '0.1.1',
    'description': 'Utilities for interacting with Canvas using Python and the canvasapi.',
    'long_description': '# CanvasUtils\n\nUtilities for interacting with Canvas using Python and the canvasapi.\n\n## Installation\n\n```bash\npip install canvasutils\n```\n\n## Features\n\n- Submit files to Canvas from within a Jupyter notebook.\n- Create assignments (coming)\n- Create assignment rubrics (coming)\n\n## Dependencies\n\nSee the file [pyproject.toml](pyproject.toml), `[tool.poetry.dependencies]`.\n\n## Usage\n\n### Assignment Submission in Jupyter\n\nThe submit module is made to be used within a Jupyter notebook (.ipynb file):\n\n![](docs/img/assignment_submit.gif)\n\n```python\napi_url = "https://canvas.instructure.com/"\ncourse_code = 123456\n\nfrom canvasutils.submit import submit\nsubmit(course_code, api_url=api_url, token_present=False)  # token present false allows you to enter token interactively.\n```\n\n## Contributors\n\nContributions are welcomed and recognized. You can see a list of contributors in the [contributors tab](https://github.com/TomasBeuzen/canvasutils/graphs/contributors).\n\n### Credits\n\nThis package was originally based on [this repository](https://github.com/eagubsi/JupyterCanvasSubmit) created by Emily Gubski and Steven Wolfram.\n',
    'author': 'Tomas Beuzen',
    'author_email': 'tomas.beuzen@stat.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomasBeuzen/canvasutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

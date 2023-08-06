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
    'version': '0.2.0',
    'description': 'Utilities for interacting with Canvas using Python and the canvasapi.',
    'long_description': '# CanvasUtils\n\nUtilities for interacting with Canvas using Python and the canvasapi.\n\n## Installation\n\n```bash\npip install canvasutils\n```\n\n`canvasutils` depends on the `ipywidgets` packages. To make sure widgets render correctly in notebooks, you may need to enable the widgets extension in Jupyter following [these instructions in the ipywidgets docs](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installation), in particular, follow [these instructions](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-the-jupyterlab-extension) if using Jupyter Lab.\n\n## Features\n\n- Submit files to Canvas from within a Jupyter notebook.\n- Create assignments (coming)\n- Create assignment rubrics (coming)\n\n## Dependencies\n\nSee the file [pyproject.toml](pyproject.toml), `[tool.poetry.dependencies]`.\n\n## Usage\n\n### Assignment Submission in Jupyter\n\nThe submit module is made to be used within a Jupyter notebook (.ipynb file):\n\n![](docs/img/assignment_submit.gif)\n\n```python\napi_url = "https://canvas.instructure.com/"\ncourse_code = 123456\n\nfrom canvasutils.submit import submit\nsubmit(course_code, api_url=api_url, token_present=False)  # token present false allows you to enter token interactively.\n```\n\n## Contributors\n\nContributions are welcomed and recognized. You can see a list of contributors in the [contributors tab](https://github.com/TomasBeuzen/canvasutils/graphs/contributors).\n\n### Credits\n\nThis package was originally based on [this repository](https://github.com/eagubsi/JupyterCanvasSubmit) created by Emily Gubski and Steven Wolfram.\n\n| Lecture | Notebook | Recordings | Practice Exercises |\n|---------|----------|------------|--------------------|\n| 1       | ✔️       |            |                    |\n| 2       | ✔️       |            |                    |\n| 3       |          |            |                    |\n| 4       |          |            |                    |\n| 5       |          |            |                    |\n| 6       |          |            |                    |\n| 7       |          |            |                    |\n| 8       |          |            |                    |\n\n| Lab | Draft | Complete |\n|-----|-------|----------|\n| 1   | ✔️    |          |\n| 2   | ✔️    |          |\n| 3   | ✔️    |          |\n| 4   |       |          |',
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

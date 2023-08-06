# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfan',
 'pyfan.amto',
 'pyfan.amto.array',
 'pyfan.amto.json',
 'pyfan.devel',
 'pyfan.devel.obj',
 'pyfan.gen',
 'pyfan.gen.rand',
 'pyfan.graph',
 'pyfan.graph.generic',
 'pyfan.graph.tools',
 'pyfan.panda.categorical',
 'pyfan.panda.inout',
 'pyfan.panda.sandbox',
 'pyfan.panda.stats',
 'pyfan.sandbox',
 'pyfan.stats.interpolate',
 'pyfan.stats.multinomial',
 'pyfan.util',
 'pyfan.util.inout',
 'pyfan.util.path',
 'pyfan.util.pdf',
 'pyfan.util.rmd',
 'pyfan.util.timer']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.20,<0.30.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numba>=0.50.1,<0.51.0',
 'numpy>=1.18.5,<2.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'pyfan',
    'version': '0.1.42',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

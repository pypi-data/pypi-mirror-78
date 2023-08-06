from setuptools import setup, find_packages
import sys

requirements = []

sys.path.insert(0, 'src')
from emqx.erlport import __version__

setup(
    name='emqx-erlport',
    maintainer='adek06',
    maintainer_email='adek06@outlook.com',
    url='https://www.emqx.io',
    version=__version__,
    description='',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    keywords='emqx',
    zip_safe=False,
    install_requires=requirements,
)

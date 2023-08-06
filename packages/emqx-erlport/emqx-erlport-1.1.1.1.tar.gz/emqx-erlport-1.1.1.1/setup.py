from setuptools import setup, find_packages
import sys

requirements = []

sys.path.insert(0, 'src')
from emqx.erlport import __version__

setup(
    name='emqx-erlport',
    maintainer='JianBo He',
    maintainer_email='heeejianbo@gmail.com',
    url='https://github.com/emqx/erlport',
    version=__version__,
    description='',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    keywords='emqx',
    zip_safe=False,
    install_requires=requirements,
)

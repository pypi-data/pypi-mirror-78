from setuptools import setup, find_packages
import sys

requirements = []

sys.path.insert(0, 'src')
__version__ = '0.1.1'

setup(
    name='emqx-erlport',
    maintainer='JianBo He',
    maintainer_email='heeejianbo@gmail.com',
    version=__version__,
    description='',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    keywords='emqx',
    zip_safe=False,
    install_requires=requirements,
)

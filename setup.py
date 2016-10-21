from sys import stderr
from setuptools import setup, find_packages


version = '0.0.1'

print(find_packages(exclude=['ez_setup', 'tests', 'predicates']), file=stderr)

setup(name='PythonVoronoi',  # Feel free to change this
      version=version,
      author='Drew Monroe',  # feel free to change this, too
      url=r'https://github.com/DrewMonroe/python-voronoi',
      packages=find_packages(exclude=['ez_setup', 'tests', 'predicates']))

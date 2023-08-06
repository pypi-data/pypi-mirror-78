"""_____________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2CodeGenerator Package Installation*

:details: SiLA2CodeGenerator setup.

:authors: Timm Severin (timm.severin@tum.de)
          Mark Dörr (mar.doerrk@uni-greifswald.de)
          Florian Meinicke (florian.meinicke@cetoni.de)

:date: (creation)          2018-06-10
:date: (last_modified)     2020-08-13
________________________________________________________________________
"""

import os

from setuptools import setup, find_packages

package_name = 'sila2codegenerator'

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        return file.read().strip()

setup(name=package_name,
      version=read(os.path.join(package_name, 'VERSION')),
      description='SiLA2 code generator for Python3',
      long_description=read('README.rst'),
      author='Timm Severin, Mark Dörr',
      author_email='mark.doerr@uni-greifswald.de',
      keywords=('SiLA2, codegenerator, lab automation,  laboratory, instruments,'
                'experiments, evaluation, visualisation, serial interface, robots'),
      url='https://gitlab.com/SiLA2/sila_python',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'lxml',
          'sila2lib',
          ],
      test_suite='',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Utilities',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                   'Topic :: Scientific/Engineering :: Information Analysis'],
      include_package_data=True,
      package_data={package_name: ['VERSION', 'templates/*/*']},
      entry_points={
          'console_scripts': [
              'silacodegenerator=sila2codegenerator.sila2codegenerator:main'
          ]
      },
      setup_requires=['wheel'],
    )

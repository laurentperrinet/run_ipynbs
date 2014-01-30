from setuptools import setup

import pypandoc

output = pypandoc.convert('README.md', 'rst')

setup(name='run_ipynbs',
      version='1.1',
      license='GPLv3',
      description='Run non-interactively ipython notebook files',
      long_description=output,
      keywords='ipython, notebooks, non-interactive, console',
      url='https://github.com/hadim/run_ipynbs',
      author='HadiM',
      author_email='hadrien.mary@gmail.com',
      classifiers=[
          'Framework :: IPython',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
      ],
      install_requires=[
          'Jinja2',
          'Pygments',
          'ipython',
          'pyzmq',
      ],
      scripts=[
          'run_ipynbs.py'
      ]
      )

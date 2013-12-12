from setuptools import setup

setup(name='run_ipynbs',
      version='1.0',
      license='GPLv3',
      description='Run non-interactively ipython notebook files',
      long_description=open('README.md').read(),
      keywords='ipython, notebooks, non-interactive, console',
      url='https://github.com/hadim/run_ipynbs',
      author='HadiM',
      author_email='hadrien.mary@gmail.com',
      classifiers=[
          'Framework :: IPython',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
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

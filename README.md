# run_ipynbs

Run non-interactively ipython notebook files. Strongly inspired from https://gist.github.com/minrk/2620876.

## Features

- run several notebooks
- reporte failed cells and display error (traceback)
- display cell output in live !

## Easy installation

Copy paste run_ipynbs.py to your system and execute it.

Or with pip : `pip install git+https://github.com/hadim/run_ipynbs.git#egg=master`

## Usage

```
$ ./run_ipynbs.py --help
2013-12-12 13:27:24:INFO: Use standard KernelManager
usage: run_ipynbs.py [-h] [--output] ipynbs [ipynbs ...]

positional arguments:
  ipynbs             Ipynb files you want to run

optional arguments:
  -h, --help         show this help message and exit
  --output, -o  Display cells output while they run
```

Execute a notebook without output :

```
 $ ./run_ipynbs.py test.ipynb
2013-12-12 13:27:53:INFO: Use standard KernelManager
2013-12-12 13:27:53:INFO: Running test.ipynb
2013-12-12 13:27:55:INFO: Run cell #0
2013-12-12 13:27:55:INFO: Done
2013-12-12 13:27:55:INFO: Run cell #1
2013-12-12 13:27:55:ERROR: Fail to execute cell #2
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-3-43a14fcd4265> in <module>()
----> 1 print(hello)

NameError: name 'hello' is not defined
2013-12-12 13:27:55:INFO: Run cell #2
2013-12-12 13:27:55:INFO: Done
2013-12-12 13:27:55:INFO: Run cell #3
2013-12-12 13:27:59:INFO: Done
2013-12-12 13:27:59:INFO: 4 cells runned with 1 cells failed
```

Execute a notebook with live output :

```
$ ./run_ipynbs.py test.ipynb -l
2013-12-12 13:28:40:INFO: Use standard KernelManager
2013-12-12 13:28:40:INFO: Running test.ipynb
2013-12-12 13:28:42:INFO: Run cell #0
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19

2013-12-12 13:28:42:INFO: Done
2013-12-12 13:28:42:INFO: Run cell #1
2013-12-12 13:28:42:ERROR: Fail to execute cell #2
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-3-43a14fcd4265> in <module>()
----> 1 print(hello)

NameError: name 'hello' is not defined
2013-12-12 13:28:42:INFO: Run cell #2
Hello !

2013-12-12 13:28:43:INFO: Done
2013-12-12 13:28:43:INFO: Run cell #3
I'm gonna sleep 3s
I wake up now :-D


2013-12-12 13:28:46:INFO: Done
2013-12-12 13:28:46:INFO: 4 cells runned with 1 cells failed
```

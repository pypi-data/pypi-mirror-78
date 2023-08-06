# py2cfg
Python3 control flow graph generator

`py2cfg` is a package that can be used to produce control flow graphs (CFGs) for Python 3 programs. 
The CFGs it generates can be easily visualised with graphviz.
That graphical analysis is the main purpose of the module.

## Examples
Below is an example of a piece of code that generates the Fibonacci sequence and the CFG produced for it with py2cfg:

```py
# fib.py

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
for _ in range(10):
    next(fib_gen)
```

![The image display works in the Gitlab README.md](fib_cfg.png)

After cloning, see `./examples/` for some code snippets to run this on.
To generate *_cfg.png images for each example, clone this repo and run the following command in the repo root directory:
```sh
git clone repourl
cd intorepodirectory
./generate_examples.sh
```

## Installation via pip3
Note: installation is not required, but is handy.

To install simply run
```sh
pip3 install py2cfg --user
```

or clone this repo and pip install locally
```
git clone <url>
cd intoprojectdirectory
pip3 install . --user
```

## Usage
It can be used three ways:

### Run via shell command
If you have installed, then the default command is py2cfg:
```py
py2cfg <file.py>
``` 
This will create a <file>_cfg.png file, which contains the colored cfg of the file.
If you don't want to install via pip, the innards of the py2cfg command can be run right from the repo:

### Via wrapper
If you have not installed, then you can run a script present in the repo, py2cfg/_runner.py, to directly generate a CFG of a Python program and visualise it:
```sh
cd intoreporootdir
python3 py2cfg/_runner.py path_to_my_code.py
```

### Via import
Whether or not you have installed (easier if you have), to use py2cfg in your own python code, simply import the module in your Python interpreter or program.
Then use the `py2cfg.CFGBuilder` class to build CFGs. 
For example, to build the CFG of a program defined in a file with the path *./example.py*, the following code can be used:

```py
from py2cfg import CFGBuilder

cfg = CFGBuilder().build_from_file('example', './example.py')
```

This returns the CFG for the code in *./example.py* in the `cfg` variable. 
The first parameter of `build_from_file` is the desired name for the CFG, and the second one is the path to the file containing the source code.
The produced CFG can then be visualised with:

```py
cfg.build_visual('exampleCFG', 'pdf')
```

The first paramter of `build_visual` is the desired name for the DOT file produced by the method, and the second one is the format to use for the visualisation.


# Contributing

## Issues
Modifications and improvements to this project are driven via Gitlab-Issues.
Check them out to create one, or fix one.

## Unit tests 
Our minimal tests are run via Gitlab-CI. 
Make sure you don't break them!
* [ ] This is a current task: the tests work locally, but not all work on Gitlab-CI...

## Type hinting
Note: any new additions to the project should adhere to type-hinting standards enforced by:
```sh
mypy --strict --disallow-any-explicit *.py
```
* [ ] This is a current issue -- yes we need to fix some things...

## Style
To maximize the ability of version control to pin down changes, and keep the style consistent, before you make any commit to the project, run this strict code auto-formatter:
```sh
black py2cfg/*.py
```

# Project history
Note: py2cfg is a significantly re-worked and improved fork of the older staticfg project:
* https://github.com/coetaur0/staticfg
* https://pypi.org/project/staticfg/

# Subtomograms
This repository implements the Binary Decomposition and Golden Ratio strategies for performing computed tomography of
dynamic processes described in Kaestner A. __et al.__ Optical Engineering **50**(12), 123201 (December 2011) [https://doi.org/10.1117/1.3660298].

# Installation
Currently only working as a local import. Make sure you run python from the same directory as this repo.
```bash
$ git clone git@github.com:verejoel/subtomograms.git
$ cd subtomograms
```

## Create a Virtual Environment
Do this according to your favourite manager (`direnv`, `pyenv`, `pipenv`). For plain python:
```bash
$ python -m venv ./venv
$ source venv/bin/activate
```

## Install dependencies
```bash
$ pip install -r requirements.txt
```

# Usage
**Note: you may need to use `python3` instead of `python`, depending on your system.
Start a python interpreter session:
```bash
$ python
```

In the interactive session, first import the Generator classes:
```python
>>> from generator import GoldenGenerator, BinaryGenerator
```

You can now use the `GoldenGenerator` and `BinaryGenerator` classes to build subtomograms.

## Binary Decomposition
To use binary decomposition, initialise an object in the following way:
```python
>>> bg = BinaryGenerator(4, 10)
Initialised!
Total projections: 40
Step size per subtomogram: 18.0
Total step size: 4.5
```
Here, the numbers 4 and 10 correspond to the number of subtomograms, and the number of projections per subtomogram,
respectively. The object will be initialised, and report the total number of projects, step size per subtomogram, and 
the total step size when all subtomograms are combined.

You can now calculate the angles for each subtomogram:
```python
>>> bg.print_angles()
Subtomogram     Angles
0               [  0.  36.  72. 108. 144. 180. 216. 252. 288. 324.]
1               [ 18.  54.  90. 126. 162. 198. 234. 270. 306. 342.]
2               [  9.  45.  81. 117. 153. 189. 225. 261. 297. 333.]
3               [ 27.  63.  99. 135. 171. 207. 243. 279. 315. 351.]
```



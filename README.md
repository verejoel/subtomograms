# Subtomograms
This repository implements the Binary Decomposition and Golden Ratio strategies for performing computed tomography of
dynamic processes described in Kaestner A. __et al.__ Optical Engineering **50**(12), 123201 (December 2011) (https://doi.org/10.1117/1.3660298).

## Installation
**Note: you may need to use `python3` instead of `python`, depending on your system.**

Currently only working as a local import. Make sure you run python from the same directory as this repo.
```bash
$ git clone git@github.com:verejoel/subtomograms.git
$ cd subtomograms
```

### Create a Virtual Environment
Do this according to your favourite manager (`direnv`, `pyenv`, `pipenv`). For plain python:
```bash
$ python -m venv ./venv
$ source venv/bin/activate
```

### Install dependencies
```bash
$ pip install -r requirements.txt
```

## Usage
Start a python interpreter session:
```bash
$ python
```

In the interactive session, first import the Generator classes:
```python
>>> from generator import GoldenGenerator, BinaryGenerator
```

You can now use the `GoldenGenerator` and `BinaryGenerator` classes to build subtomograms.

### Binary Decomposition
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

By default, the projections are distrubuted over a full circle. To distribute across a half-circle, call the generator
with the `full_circle` flag set to `False`:
```python
>>> bg = BinaryGenerator(4, 10, full_circle=False)
>>> bg.print_angles()
Subtomogram     Angles
0               [  0.  18.  36.  54.  72.  90. 108. 126. 144. 162.]
1               [  9.  27.  45.  63.  81.  99. 117. 135. 153. 171.]
2               [  4.5  22.5  40.5  58.5  76.5  94.5 112.5 130.5 148.5 166.5]
3               [ 13.5  31.5  49.5  67.5  85.5 103.5 121.5 139.5 157.5 175.5]
```

### Changing the output units
By default, the generators output angles in units of `degrees`, as this is typically more useful for experiments. Should
you prefer radians, simply initialise the generator with the `degrees` flag set to false:
```python
>>> bg = BinaryGenerator(4, 10, degrees=False)
>>> bg.print_angles()
Subtomogram     Angles
0               [0.    0.628 1.257 1.885 2.513 3.142 3.77  4.398 5.027 5.655]
1               [0.314 0.942 1.571 2.199 2.827 3.456 4.084 4.712 5.341 5.969]
2               [0.157 0.785 1.414 2.042 2.67  3.299 3.927 4.555 5.184 5.812]
3               [0.471 1.1   1.728 2.356 2.985 3.613 4.241 4.869 5.498 6.126]
```

By default, values are rounded to three decimal places - to override this, set the class variable `DP` after you create
the generator:
```python
>>> bg.DP = 5
>>> bg.print_angles()
Subtomogram     Angles
0               [0.      0.62832 1.25664 1.88496 2.51327 3.14159 3.76991 4.39823 5.02655 5.65487]
1               [0.31416 0.94248 1.5708  2.19911 2.82743 3.45575 4.08407 4.71239 5.34071 5.96903]
2               [0.15708 0.7854  1.41372 2.04204 2.67035 3.29867 3.92699 4.55531 5.18363 5.81195]
3               [0.47124 1.09956 1.72788 2.35619 2.98451 3.61283 4.24115 4.86947 5.49779 6.12611]
```

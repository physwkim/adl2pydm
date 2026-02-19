# adl2pydm

[![release](https://img.shields.io/github/release/BCDA-APS/adl2pydm.svg)](https://github.com/BCDA-APS/adl2pydm/releases)
[![tag](https://img.shields.io/github/tag/BCDA-APS/adl2pydm.svg)](https://github.com/BCDA-APS/adl2pydm/tags)
[![Python version](https://img.shields.io/pypi/pyversions/adl2pydm.svg)](https://pypi.python.org/pypi/adl2pydm)
[![PyPi](https://img.shields.io/pypi/v/adl2pydm.svg)](https://pypi.python.org/pypi/adl2pydm)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/adl2pydm)](https://anaconda.org/conda-forge/adl2pydm)

[![license: ANL](https://img.shields.io/badge/license-ANL-brightgreen)](LICENSE.txt)
![Unit Tests](https://github.com/BCDA-APS/adl2pydm/workflows/Unit%20Tests/badge.svg)

**NOTE**:  This project is in initial development.  *Be amazed when something works right at this time.  If you find something that does not work right or could be better, please file an [issue](https://github.com/BCDA-APS/adl2pydm/issues/new/choose) since that will be an important matter to be resolved.*

Convert [MEDM](https://epics.anl.gov/extensions/medm/index.php)'s .adl files to [PyDM](https://github.com/slaclab/pydm)'s .ui format

## Features

- Converts all standard MEDM widget types to their PyDM equivalents
- **Proportional scaling** via QGridLayout with stretch factors — widgets resize proportionally when the window is resized, mimicking MEDM's behavior
- Supports overlapping widgets (common in MEDM for labels on backgrounds)
- Recursive layout for composite (embedded) containers
- PySide6 / Qt6 compatible

## Usage

```
adl2pydm -d /output/path screen1.adl screen2.adl ...
```

The output directory is created automatically if it does not exist.

## Options

```
positional arguments:
  adlfiles             MEDM '.adl' file(s) to convert

optional arguments:
  -h, --help           show this help message and exit
  -d DIR, --dir DIR    output directory, default: same directory as input file
  -v, --version        show program's version number and exit
  -log LOG, --log LOG  Provide logging level. Example --log debug', default='warning'
  --use-scatterplot    Translate MEDM 'cartesian plot' widget as `PyDMScatterPlot`
                       instead of `PyDMWaveformPlot`, default=False
  --no-scaling         Disable proportional scaling (use absolute positioning)
```

## Install

Only the `pip` install is working now ([PyPI package](https://pypi.org/project/punx/)):

* `pip install adl2pydm`

Once a `conda` package has been built and uploaded to the
[`aps-anl-tag` channel on conda-forge](https://anaconda.org/aps-anl-tag),
(see [related GitHub issue](https://github.com/BCDA-APS/adl2pydm/issues/85)) then:

* `conda install adl2pydm -c aps-anl-tag`

### Requirements

- Python 3.9+
- PySide6 and PyDM are required at runtime to use the generated `.ui` files

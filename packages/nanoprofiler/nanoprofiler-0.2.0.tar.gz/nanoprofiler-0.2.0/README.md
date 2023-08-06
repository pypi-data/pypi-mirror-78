# nanoProfiler

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![Release](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Release&query=%24[0].name&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fnanogennari%252Fnanoprofiler%2Frepository%2Ftags&style=flat-square)](https://gitlab.com/nanogennari/nanoprofiler/)

A small python profiler using cProfile, pstats, Pandas and matplotlib.

nanoProfiler was primarily designed evaluate the internal variations of execution times in codes with variable complexity. But it can also be used with fixed complexity code.

## Instalation

nanoProfiler can be installed with pip:

    pip install nanoprofiler

or:

    python -m pip install nanoprofiler

### Manual instalation

Clone the repository

    git clone https://gitlab.com/nanogennari/nanoprofiler.git

And run setup script

    cd nanoprofiler
    python setup.py install

## Usage

Usage example:

    from nanoprofiler import Profiler

    pr = Profiler()

    pr.start(name="exec1")
    your_code()
    pr.stop()

    pr.start(name="exec2")
    another_code()
    pr.stop()

    pr.plot_top_time(time="cumtime")
    pr.plot_function(time="tottime")
    pr.save_data("folder/to/save/results", "prefix_for_files")

More details on how to use nanoProfiler can be found [here](https://nanogennari.gitlab.io/nanoprofiler/quick-guide/).

## Documentation

Documentation can be found [here](https://nanogennari.gitlab.io/nanoprofiler).
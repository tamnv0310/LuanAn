[![Package version](https://badge.fury.io/py/sentinelhub.svg)](https://pypi.org/project/sentinelhub/)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/sentinelhub.svg)](https://anaconda.org/conda-forge/sentinelhub)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/sentinelhub.svg?style=flat-square)](https://pypi.org/project/sentinelhub/)
[![Build status](https://travis-ci.org/sentinel-hub/sentinelhub-py.svg?branch=master)](https://travis-ci.org/sentinel-hub/sentinelhub-py)
[![Docs status](https://readthedocs.org/projects/sentinelhub-py/badge/?version=latest)](http://sentinelhub-py.readthedocs.io/en/latest/)
[![Overall downloads](https://pepy.tech/badge/sentinelhub)](https://pepy.tech/project/sentinelhub)
[![Last month downloads](https://pepy.tech/badge/sentinelhub/month)](https://pepy.tech/project/sentinelhub)
[![](https://img.shields.io/pypi/l/sentinelhub.svg)](https://github.com/sentinel-hub/sentinelhub-py/blob/master/LICENSE.md)
[![Code coverage](https://codecov.io/gh/sentinel-hub/sentinelhub-py/branch/master/graph/badge.svg)](https://codecov.io/gh/sentinel-hub/sentinelhub-py)

# Description

The **sentinelhub** Python package allows users to make OGC (WMS and WCS)
web requests to download and process satellite images within your Python
scripts. It supports Sentinel-2 L1C and L2A, Sentinel-1, Landsat 8, MODIS and DEM data source.

The package also supports obtaining data from Amazon Web Service. It can either provide data from public bucket with
Sentinel-2 L1C imagery or requester pays bucket with Sentinel-2 L2A imagery. If specified the downloaded data can be
stored in ESA .SAFE format (all types of .SAFE format are supported).

# Installation

The package requires a Python version >= 3.6 and installed C/C++ compiler. The package is available on
the PyPI package manager and can be installed with

```
$ pip install sentinelhub --upgrade
```

Alternatively, the package can be installed with Conda from `conda-forge` channel

```
conda install -c conda-forge sentinelhub 
```

To install the package manually, clone the repository and
```
$ python setup.py build
$ python setup.py install
```

Before installing `sentinelhub-py` on **Windows** it is recommended to install package `shapely` from
[Unofficial Windows wheels repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

Once installed or updated the package can be configured according to [instructions in documentation](http://sentinelhub-py.readthedocs.io/en/latest/configure.html).

# Content

### OGC web service

Some of the major features are linked to one's [Sentinel Hub account](https://www.sentinel-hub.com/trial):
 * support for Web Map Service (WMS) and Web Coverage Service (WCS) requests using your Sentinel Hub account;
 * support for standard and custom multi-spectra layers, such as unprocessed
 bands, true color imagery, or NDVI;
 * support for multi-temporal requests;
 * support for cloud coverage filtering;
 * support for different Coordinate Reference Systems;
 * support to read and write downloaded data to disk in the most common
 image and data formats;
 * support for various data sources:
   * Sentinel-2 L1C,
   * Sentinel-2 L2A,
   * Sentinel-1,
   * Landsat 8,
   * MODIS,
   * DEM.


### AWS data download

The package allows to download Sentinel-2 data from Sentinel-2 on AWS
and reconstruct data into ESA .SAFE format.

The following are implemented:
 * support for Sentinel-2 L1C and Sentinel-2 L2A data;
 * support of old and new (i.e. compact) .SAFE format;
 * support for downloading of either entire product, or a map of the .SAFE
 structure only;
 * support of command lines entries;
 * adjustable threaded downloads, and optional redownloads of existing data (not default);
 * requires either S-2 product ID, or tile name and date of a product.

In case of Sentinel-2 L2A data AWS access key is required.


### Documentation

For more information on the package and to access the documentation, visit [readthedocs](http://sentinelhub-py.readthedocs.io/).


# Examples

Jupyter notebooks on how to use the modules to execute OGC requests, or
download raw data from AWS in .SAFE format can be found in the [examples](https://github.com/sentinel-hub/sentinelhub-py/tree/master/examples/)
folder, or viewed in the [docs](http://sentinelhub-py.readthedocs.io/):
 * Using OGC web services ([link](http://sentinelhub-py.readthedocs.io/en/latest/examples/ogc_request.html))
 * Using utilities for large geographical areas ([link](http://sentinelhub-py.readthedocs.io/en/latest/examples/large_area_utilities.html))
 * AWS data download ([link](http://sentinelhub-py.readthedocs.io/en/latest/examples/aws_request.html))
 * AWS data download from command line in .SAFE format ([link](http://sentinelhub-py.readthedocs.io/en/latest/aws_cli.html))

# Blog posts

 * [Upgrading the sentinelhub Python package](https://medium.com/sentinel-hub/upgrading-the-sentinelhub-python-package-2665f9c10df)
 * [Release of sentinelhub Python Package 2.0](https://medium.com/sentinel-hub/release-of-sentinelhub-python-package-2-0-a3d47709f8fd)

# Questions and Issues

Feel free to ask questions about the package and its use cases at [Sentinel Hub forum](https://forum.sentinel-hub.com/) or raise an issue on [GitHub](https://github.com/sentinel-hub/sentinelhub-py/issues).

You are welcome to send your feedback to the package authors, Sentinel Hub research team, through any of [Sentinel Hub communication channel](https://sentinel-hub.com/develop/communication-channels).

# License

See [LICENSE](https://github.com/sentinel-hub/sentinelhub-py/blob/master/LICENSE.md).

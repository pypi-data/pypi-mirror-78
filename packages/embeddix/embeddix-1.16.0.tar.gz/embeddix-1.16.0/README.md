# embeddix
[![GitHub release][release-image]][release-url]
[![PyPI release][pypi-image]][pypi-url]
[![Build][build-image]][build-url]
[![MIT License][license-image]][license-url]


[release-image]:https://img.shields.io/github/release/akb89/embeddix.svg?style=flat-square
[release-url]:https://github.com/akb89/embeddix/releases/latest
[pypi-image]:https://img.shields.io/pypi/v/embeddix.svg?style=flat-square
[pypi-url]:https://pypi.org/project/embeddix/
[build-image]:https://img.shields.io/github/workflow/status/akb89/embeddix/CI?style=flat-square
[build-url]:https://github.com/akb89/embeddix/actions?query=workflow%3ACI
[license-image]:http://img.shields.io/badge/license-MIT-000000.svg?style=flat-square
[license-url]:LICENSE.txt

A small toolkit for processing word embeddings with numpy. You can use `embeddix` to convert .txt embeddings (such as glove files) to numpy and vice-versa.

## Install
```shell
pip install embeddix
```

or, after a git clone:
```shell
python3 setup.py install
```

## Use

### Extract vocabulary from a txt embeddings file
```shell
embeddix extract --embeddings /absolute/path/to/embeddings.txt
```

### Convert from txt to numpy
```shell
embeddix convert --to numpy --embeddings /absolute/path/to/embeddings.txt
```

### Convert from numpy to txt
```shell
embeddix convert --to txt --embeddings /absolute/path/to/embeddings.npy
```

### Evaluate DSM on intrinsic tasks
Evaluate on lexical similarity (men, simlex, simverb) or concept categorization (essli, ap, battig)
```shell
embeddix evaluate \
--embeddings /absolute/path/to/embeddings.npy \
--vocab /absolute/path/to/embeddings.vocab \
--dataset instrinsic_task_dataset_name
```

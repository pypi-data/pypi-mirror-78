# README - KDB
> A Python CLI and module for k-mer profiles, similarities, and graph databases

NOTE: This project is pre-alpha, all of the badge links are broken and are just placeholders at the moment. Development is ongoing. But feel free to clone the repository and play with the code for yourself!

## Development Status

[![PyPI version](https://img.shields.io/pypi/v/ngsci.svg)][pip]
[![Python versions](https://img.shields.io/pypi/pyversions/ngsci.svg)][Pythons]
[![Travis Build Status](https://travis-ci.org/MatthewRalston/ngsci.svg?branch=master)](https://travis-ci.org/MatthewRalston/ngsci)
[![Coveralls code coverage](https://img.shields.io/coveralls/MatthewRalston/ngsci/master.svg)][Coveralls]
[![ReadTheDocs status](https://readthedocs.org/projects/ngsci/badge/?version=stable&style=flat)][RTD]


[pip]: https://pypi.org/project/ngsci/
[Pythons]: https://pypi.org/project/ngsci/
[Coveralls]: https://coveralls.io/r/MatthewRalston/ngsci?branch=master
[RTD]: https://ngsci.readthedocs.io/en/latest/

## Summary 

KDB is a Python library designed for bioinformatics applications. It addresses the ['k-mer' problem](https://en.wikipedia.org/wiki/K-mer) (substrings of length k) in a simple and performant manner. It generates a [De Brujin graph](https://en.wikipedia.org/wiki/De_Bruijn_graph) from the k-mer spectrum of fasta or fastq sequencing data and stores the graph and spectrum to the `.kdb` format spec, a bgzf file similar to BAM. 

The principle goal of the library is k-mer statistics and rapid access to specific k-mers and associated abundances with a Python CLI and API. Other goals include access to the k-mer count distribution, k-mer transition probabilities, and more by leveraging the bgzf specification. Another low-hanging fruit could be approximating demultiplexing coefficients for artificial metagenomes.


## Installation

OS X and Linux release:

```sh
pip install ngsci
```

Development installation:

```sh
git clone https://github.com/MatthewRalston/ngsci.git
cd ngsci
pip install -r requirements.txt
pip install -r requirements-dev.txt
PYTHONPATH=$(pwd):$PYTHONPATH
```

## Usage Example

CLI Usage

```bash
./bin/ngsci --help
./bin/ngsci -vv input.bam > output.txt
```



## Documentation

Check out the [Readthedocs documentation](https://ngsci.readthedocs.io/en/latest/), with examples and descriptions of the module usage.

## Development

```bash
pytest --cov=ngsci
```

## License

Created by Matthew Ralston - [Scientist, Programmer, Musician](http://matthewralston.us) - [Email](mailto:mrals89@gmail.com)

Distributed under the GPL v3.0 license. See `LICENSE.txt` for the copy distributed with this project. Open source software is not for everyone, but for those of us starting out and trying to put the ecosystem ahead of ego, we march into the information age with this ethos.

## Contributing

1. Fork it (<https://github.com/MatthewRalston/ngsci/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


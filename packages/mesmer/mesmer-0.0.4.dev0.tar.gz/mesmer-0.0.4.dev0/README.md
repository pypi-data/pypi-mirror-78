[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![mesmer-master Actions Status](https://github.com/bthorne93/mesmer/workflows/mesmer-master/badge.svg)](https://github.com/bthorne93/mesmer/actions)

# mesmer

Package to calculate the log probability of foregrounds.

## Description

Given a dataset $\mathbf{d}$, this package calculates, and samples from, the maximum 
likelihood set of foreground parameters, $P(\mathbf{\theta}}\mathbf{d})$.

This approach has been used in these papers:

1. [Simulated forecasts for primordial B-mode searches in ground-based experiments](https://arxiv.org/abs/1608.00551)
2. [The Simons Observatory: Science goals and forecasts](https://arxiv.org/abs/1808.07445)
3. [Removal of Galactic foregrounds for the Simons Observatory primordial gravitational wave search](https://arxiv.org/abs/1905.08888)

## Useage

[An example note book](examples/example.ipynb) is in the `notebooks` folder.

To add SEDs, edit [the SED functions file](mesmer/seds.py). The likelihood is defined in [the likelihood file](mesmer/likelihood.py).

# License

This project is Copyright (c) Ben Thorne and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the [Astropy package template](https://github.com/astropy/package-template)
which is licensed under the BSD 3-clause license. See the licenses folder for
more information.

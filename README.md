# pulsars

[![version-badge][version-badge]][psrcat]
[![Code style: black][black-badge]][black]

this is my own copy of the [**ATNF pulsars database**][psrcat]. the database is scraped on the 10th of each month, at midnight. the code that scraps is in the **scrap.py** file, and the database itself (in all of its JSONic glory) is in [**pulsars.json**](pulsars.json). if you end up using the data from this repository, do cite the [**original paper**][paper] on the ATNF database and quote the [**web address**][psrcat] of the ATNF database for updated versions. the citation is available in BibTeX format in the [**CITATION.md**](CITATION.md) file. additional statements that apply to the use of the ATNF database are in the [**COPYING.md**](COPYING.md) file. the code itself is licensed under the [**MIT License**](LICENSE). this repository powers the [**koshka**][koshka] package, which aims to make accessing catalogues on pulsars and radio transients easier.

[black]: https://github.com/psf/black
[koshka]: https://github.com/astrogewgaw/koshka
[psrcat]: http://www.atnf.csiro.au/research/pulsar/psrcat
[paper]: http://adsabs.harvard.edu/abs/2005AJ....129.1993M
[version-badge]: https://img.shields.io/badge/version-v1.64-green
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg

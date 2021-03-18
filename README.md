# pulsars

[![version-badge](https://img.shields.io/badge/version-v0.1-green)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

this is my own copy of the [**ATNF pulsars database**](https://www.atnf.csiro.au/research/pulsar/psrcat/). the database is scraped on the 10th of each month, at midnight, according to UTC time. the scraping code is in the standalone **scrap.py** file, and the database itself (in all of its JSONic glory) is in **pcat.json**. the references are available in the **pref.json** file. if you end up using the data from this repository, do cite the [**original paper**]((http://adsabs.harvard.edu/abs/2005AJ....129.1993M)) on the ATNF database and quote the [**web address**](http://www.atnf.csiro.au/research/pulsar/psrcat) of the database for updated versions. the citation is available in BibTeX format in the **CITATION.md** file. additional statements that apply to the use of the ATNF database are in the **COPYING.md** file. the code itself is licensed under the **MIT License**. this repository powers the **neko** package, which aims to make accessing catalogues on pulsars and radio transients easier.
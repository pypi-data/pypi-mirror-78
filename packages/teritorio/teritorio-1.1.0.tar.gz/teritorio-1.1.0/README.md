<p align="center">
<a href="https://travis-ci.org/spapanik/teritorio"><img alt="Build" src="https://travis-ci.org/spapanik/teritorio.svg?branch=master"></a>
<a href="https://coveralls.io/github/spapanik/teritorio"><img alt="Coverage" src="https://coveralls.io/repos/github/spapanik/teritorio/badge.svg?branch=master"></a>
<a href="https://github.com/spapanik/teritorio/blob/master/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/teritorio"></a>
<a href="https://pypi.org/project/teritorio"><img alt="PyPI" src="https://img.shields.io/pypi/v/teritorio"></a>
<a href="https://pepy.tech/project/teritorio"><img alt="Downloads" src="https://pepy.tech/badge/teritorio"></a>
<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# teritorio: ISO codes for countries and currencies

## Installation and usage

### Installation

_teritorio_ can be installed by running `pip install teritorio`. It requires Python 3.7.0+ to run.

### Usage

The two main objects are `Countries` and `Currencies`:

#### Countries usage

```python
from teritorio import Countries

# list all countries
for country in Countries():
    print(country)

# get a specific country
countries = Countries()

# access the country as an attribute
print(countries.DEU)  # Country(english_name='Germany', french_name="Allemagne (l')", alpha_2_code='DE', alpha_3_code='DEU', numeric_code=276)
# access the country with square brackets
print(countries["DEU"])  # Country(english_name='Germany', french_name="Allemagne (l')", alpha_2_code='DE', alpha_3_code='DEU', numeric_code=276)
```

#### Currencies usage

```python
from teritorio import Currencies

# list all currencies
for currency in Currencies():
    print(currency)

# get a specific currency
currencies = Currencies()

# access the currency as an attribute
print(currencies.GBP)  # Currency(code='GBP', name='Pound Sterling', entities=['GUERNSEY', 'ISLE OF MAN', 'JERSEY', 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)'], numeric_code=826, minor_units=2)
# access the currency with square brackets
print(currencies["GBP"])  # Currency(code='GBP', name='Pound Sterling', entities=['GUERNSEY', 'ISLE OF MAN', 'JERSEY', 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)'], numeric_code=826, minor_units=2)
```

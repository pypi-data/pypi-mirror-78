# Welcome to Allokation 👋

![Version](https://img.shields.io/badge/version-0.0.3-blue.svg?cacheSeconds=2592000)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> A python package that gets stocks prices from [yahoo finance](https://finance.yahoo.com/) and calculates how much of each stocks you must buy to have almost equal distribution between the stocks you want in your portfolio

## \*\*\*Disclaimer\*\*\*

**NO FINANCIAL ADVISE** - This library **DO NOT** offer financial advises, it just calculates the amount of stocks you will need to buy based on stocks that **YOU WILL INFORM** and the market price of the day for these stocks, given by [yahoo finance](https://finance.yahoo.com/).

## Requires

- python >= 3.x

## Install

- install via pip

```sh
pip install allokation
```

## Usage

- It's quite simple to use this package, you just need to import the function `allocate_money`, pass a list of tickers you want and the available money you have to invest.

- It will return a dict containing the allocations you must need and the total money you must need to have this portfolio (This total will be less or equal than the available money you informed to the `allocate_money` function). For each stock, it will be returned the `price` that was used to calculate the portfolio, the `amount` of stocks you will need to buy, the `total` money you need to buy this amount of this stock and the `percentage` that this stock represents in your portfolio. For example:

```python
{
    'allocations': {
        'B3SA3': {
            'price': 58.33,
            'amount': 3.0,
            'total': 174.99,
            'percentage': 18.14420803782506
        },
        'BBDC4': {
            'price': 21.97,
            'amount': 9.0,
            'total': 197.73,
            'percentage': 20.50205300485256
        },
        'MGLU3': {
            'price': 88.77,
            'amount': 2.0,
            'total': 177.54,
            'percentage': 18.408610177927088
        },
        'PETR4': {
            'price': 22.92,
            'amount': 9.0,
            'total': 206.28000000000003,
            'percentage': 21.388577827547596
        },
        'VVAR3': {
            'price': 18.9,
            'amount': 11.0,
            'total': 207.89999999999998,
            'percentage': 21.556550951847704
        }
    },
    'total_value': 964.4399999999999
}
```

### Example

Check out the example available in [`example/example.py`](./example/example.py) to see it in action.

## Development Guide

### Getting the project

- clone this repository

```sh
git clone git@github.com:capaci/allokation.git
```

- install dependencies

```sh
pip install -r requirements.txt
pip install -r requirements-tests.txt
```

### Run tests

- Unit tests

```sh
pytest tests/
```

- Coverage

```sh
coverage run -m pytest tests/
coverage report
```

- Linter

```sh
flake8
```

## Author

👤 **Rafael Capaci**

- Website: [capaci.dev](https://capaci.dev)
- Twitter: [@capacirafael](https://twitter.com/capacirafael)
- Github: [@capaci](https://github.com/capaci)
- LinkedIn: [@rafaelcapaci](https://linkedin.com/in/rafaelcapaci)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_

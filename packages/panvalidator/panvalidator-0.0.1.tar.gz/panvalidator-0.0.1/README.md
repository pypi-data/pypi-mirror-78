# PAN validator

[![Build Status](https://travis-ci.com/geaden/panvalidator.svg?branch=main)](https://travis-ci.com/geaden/panvalidator) [![Coverage Status](https://coveralls.io/repos/github/geaden/panvalidator/badge.svg?branch=main)](https://coveralls.io/github/geaden/panvalidator?branch=main)

A [Primary Account Number](https://en.wikipedia.org/wiki/Payment_card_number) 
validation tool.

## Install

```bash
pip install panvalidator
```

## Usage

```python
>>> import panvalidator
>>> result = panvalidator.validate('4444444444444422')
>>> result.is_valid()
True
>>> result = panvalidator.validate('ab')
>>> result.is_valid()
False
>>> print(result.message)
Given PAN has following issue(s):
  1. Invalid length 2.
  2. PAN should have only digits, found: a, b.
  3. Invalid IIN -1.
  4. Invalid luhn.
```

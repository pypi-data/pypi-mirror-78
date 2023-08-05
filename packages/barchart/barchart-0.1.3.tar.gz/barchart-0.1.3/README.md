# barchart
*The Unofficial API for barchart.com*

[![Build Status](https://travis-ci.org/tke578/barchart.svg?branch=master)](https://travis-ci.org/tke578/barchart)
[![PyPI version](https://badge.fury.io/py/barchart.svg)](https://badge.fury.io/py/barchart)
[![Python version](https://img.shields.io/badge/Python-3.8-blue.svg)](https://shields.io/)
[![Downloads](https://pepy.tech/badge/barchart)](https://pepy.tech/project/barchart)


Installation
-----


``` pip install barchart```


Unusual Options Activity
-----

````
from barchart import UOA

uoa = UOA()
uoa.data 

[
  {'Symbol': 'TGT', 'Price': '153.78', 'Type': 'Call', 'Strike': '160.00', 'Exp Date': '08/28/20', 'DTE': '9', 'Bid': '1.53', 'Midpoint': '1.55', 'Ask': '1.56', 'Last': '1.40', 'Volume': '7,382', 'Open Int': '165', 'Vol/OI': '44.74', 'IV': '38.08%', 'Last Trade': '13:19 ET'},
]

#Create CSV file

uoa.to_csv()

````
#### Concerns
The first time you ever run the render() method, it will download Chromium into your home directory (e.g. ~/.pyppeteer/). This only happens once.
Additional necessary [linux packages](https://github.com/miyakogi/pyppeteer/issues/60) may need to be installed.

Timeout issues do sometimes occur when fetching  with `asycnc` since data is loaded onto the DOM asynchronous.
A Timeout Exception will be raised `barchart.helpers.errors.TimeoutError`
At the moment, it takes about 1 minute to fetch and parse 10-12 pages.

If a parsing exception is raised, create a issue ticket.
Parsing exceptions `barchart.helpers.errors.ParsingError: Parsing error: Index error on table headers, check response`
 
Sometimes barchart likes to suppress most of their data at different times of day.



 

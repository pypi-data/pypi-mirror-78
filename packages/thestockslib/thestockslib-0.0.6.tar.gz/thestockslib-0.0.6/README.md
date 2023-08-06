# thestockslib

A simple library to manage stocks data

### Sample code ###

```
# library import
from thestockslib import TheStock

# initialization
stock = TheStock('AAPL')

# getting live price
stock.getliveprice()

# getting current Yahoo recommendation
r = stock.getyahoorecommendation()
TheStock.getyahoorecommendationstring(r)

# getting Yahoo performance outlook information (short term, medium term, long term)
stock.getyahooperformanceoutlook()

# getting historical price at July 31st, 2020
stock.gethistoricalprice('2020-07-31')

# adding some mapping to recommendations actions
stock.addactiontoperiod('buy', 7) # when a 'buy' suggestion is received, consider a sell after 7 days
stock.addactiontoperiod('strong buy', 7) # when a 'strong buy' suggestion is received, consider a sell after 7 days
stock.addactiontoperiod('long-term buy', 30) # when a 'long-term buy' suggestion is received, consider a sell after 30 days

# initializing the suggester name
suggestername = 'Cascend'

# simulating purchases by suggester name
purchases = stock.simulatepurchases(suggestername)
print(purchases)

# simulating sells
stock.simulatesells(purchases)

# compute suggester's reliability for 'buy' actions
stock.getsuggestionreliability(suggestername, 'buy')
```

### Available Enums ###

#### `ConsideredAverage` ####

This `Enum` is used to pass as input the average method to adopt, when historical data are requested.
Following values are possible:
* `OPEN_CLOSE`, to consider as daily value the average between open and close prices for a given stock
* `HIGH_LOW`, to consider as daily value the average between higher and lower prices for that day, for given stock

### Available classes ###

Just a single `TheStock` class is available.

Following methods are supported:

* `__init__(self, t, df='%Y-%m-%d', ca=ConsideredAverage.OPEN_CLOSE)`, initializes the `TheStock` object
  * `t` (`str`) is the ticker/symbol
  * `df` (`str`) is the date format to consider
  * `ca` (`ConsideredAverage`) is the average to consider

* `addactiontoperiod(a, p)`, adds a match between a recommendation action and the duration to consider for that recommendation
  * `a` (`str`) is the action title/name, as mapped with the list of recommedations
  * `p` (`int`) is the period to consider, in days

* `convertdatetime(d)`, converts a datetime object `d` to a string, in the format `df` passed during the object initialization
  * `d` (`datetime`) the datetime object to convert

* `getliveprice(round_decimals=2)`, returns the current live price for the current symbol
  * `round_decimals` (`int`) the decimals to consider for rounding

* `gethistoricalprice(d, round_decimals=2)`, returns the historical price for the current symbol at time `d`
  * `d` (`datetime`) the date to consider
  * `round_decimals` (`int`) the decimals to consider for rounding

* `simulatepurchases(s)`, simulates purchases of the current symbol for the suggester `s`
  * `s` (`str`) the suggester's name to consider

* `simulatesells(p)`, simulates sell of given purchases `p`, after the expiration of the relative period for the action suggested for that purchase
  * `p` (`list`) the list of purchases objects

* `getsuggestionreliability(suggester, suggestion, transactionprice=0.0)`, computes the reliability of a given suggester for a given suggestion
  * `suggester` (`str`) the suggester's name
  * `suggestion` (`str`) the suggestion action
  * `transactionprice` (`float`) the price for transaction to consider

* `generategraphs(fcast_time, apikey, outputname_pre='')`, generates the graphs to be displayed for the current symbol
  * `fcast_time` (`int`) the forecast time to consider, in days
  * `apikey` (`str`) the API key to consider
  * `outputname_pre` (`str`) the preliminary file name to use for generated graphs

* `getyahoorecommendation()`, returns the current Yahoo recommendation for the current symbol

* `getyahooperformanceoutlook()`, returns the current Yahoo performance outlook for the current symbol (output is a list containing, in order, short term, medium term, long term results)

Following statical methods are supported:

* `getrevolutsymbols()`, returns the list of symbols supported by Revolut

* `combineimages(l, vertical=False, outputfile='output.png')`, combines a list of images to an output file
  * `l` (`list`) the list of file names of the input images to combine
  * `vertical` (`bool`) the combination mode (vertical or horizonal)
  * `outputfile` (`str`) the output file name to generate

* `removeimages(outputname_pre='')`, removes all images generated
  * `outputname_pre` (`str`) the preliminary file name to use for generated graphs

* `getyahoorecommendationstring(r)`, retrieves the Yahoo recommendation string from the input value represented as `float`
  * `r` (`float`) the recommendation value represented as `float`

### TODO ###

* Improve code readability


### Contacts ###

You can find me on [Twitter](https://twitter.com) as [@auino](https://twitter.com/auino).

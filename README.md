# flamingo-finance-profit-maximizer

This is a script that uses the compound interest formula to give the user the best possible way of claiming and reinvesting the generated FLM at any given point in time.
on how many times to reinvest the flamingo generated through staking at flamingo.finance.
The script uses the CoinMarketCap API to fetch live data on the current prices of the coins used that are needed for the calculations. 

The script calculates the ideal amount of times a user should claim his/her FLM in a given amount of time. Specifically this script calculates it for 1, 3, 6, 9 months and 1 year.
It is then up to the user to interpret the results and follow the best course of action.

# The limitations of the script

This script gives the ideal scenario at any given point in time. However, there are many variables that this script does not take into account such as the future price volatility of FLM,
GAS, NEO etc. but only because it is just not possible to predict their prices in the future. This means that following the results of this script will allow the user to be more educated
on the investement but it will not produce the best possible scenario as that would require predicting the future.

As of yet, the script also does not take the current FLM into account. That is something that needs to be added.

# The strengths of this script

Regardless of the limitations listed above this script is going to produce better results than not having a strategy at all or claiming the FLM at fixed points in time. 
and that is mainly because it is just not possible to. Such variablthis script does not take into account that t

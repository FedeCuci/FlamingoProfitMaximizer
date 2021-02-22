# flamingo-finance-profit-maximizer

This profit maximizer is a python script which aims to help investors staking their tokens on flamingo.finance. It is aimed at investors which are looking to reinvest the generated FLM from staking their tokens, in the best way possible. Using live data taken from the CoinMarketCap API, it tries to provide the user with a plan on how often FLM should be claimed and staked again at any given point in time in order to maximize profit. The script that uses the compound interest formula to find out how many times the staked assets should be compounded uaing live market data to produce the highest amount of profit at any given point in time. The main formula that this script uses is the following:

Profit = current_staked_assets * (1 + ((current_apy * current_price_flm) / x))^(x*t) - transaction_fee*x

transaction_fee = current_price_gas * 0.011 * 4
x = the amount of times profit is compounded
t = time in years - by changing t, the user can adapt the results to maximize profit in any given point in time.

In the formula above, there are 2 unkowns: P and x. This script finds the x value (which represents how many times FLM should be claimed) that produces the highest P. Specifically 
it uses the scipy library to achieve this. 

However, this can also be done by simply graphing the above function and taking x value where P is greatest.

# The limitations of the profit maximizer

This script gives the ideal scenario at any given point in time. In other words, based on current market data it will produce different results everytime. There are variables that just cannot be taken into account such as the price volatilty of the tokens. These have a big impact on the result, but unfortunately none can know the price of a coin in the future. To be clear, this script does not make any calculation to try and guess the prices of coins in the future and that is why it only produces results with the data it fetches from the CoinMarketCap API each time it is run. 

# The strengths of the profit-maximizer

Regardless of the limitations listed above, following this script is almost guaranteed to generate more profit than randomly claiming FLM or claiming FLM at fixed points in time.

Disclaimer: this tool is based on a mathematical formula and does not predict the future. It should be used at your own risk.

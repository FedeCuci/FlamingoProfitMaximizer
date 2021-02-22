import scipy
import os
from scipy import optimize
import numpy

from terminaltables import AsciiTable
from colorclass import Color, Windows

Windows.enable()

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'id' : '7150,1376,1785'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '7d47f6ed-298d-4cc7-9927-5efad82ff6de',
}

session = Session()
session.headers.update(headers)



try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

  coins = {'NEO' : data['data']['1376']['quote']['USD'], 'FLM' : data['data']['7150']['quote']['USD'], 'GAS' : data['data']['1785']['quote']['USD']}

  current_staked_assets = int(input('Current staked assets ($): '))
  current_apy = input('Current APY (%): ')
  flm_to_claim = int(input('Current amount of FLM to be claimed (FLM): '))
  current_price_neo = coins['NEO']['price'] # Get current price of NEO from CoinMarketCap API
  current_price_flm = coins['FLM']['price'] # Get current price of FLM from CoinMarketCap API
  current_price_gas = coins['GAS']['price'] # Get current price of GAS from CoinMarketCap API
  flm_current_rate_of_production_per_year = current_staked_assets * float('1.' + current_apy)
  current_apy = int(current_apy) / 100
  flm_current_rate_of_production_per_day = flm_current_rate_of_production_per_year / 365
  transaction_fee = (current_price_gas * 0.011) * 4 # In order to reinvest FLM one must first complete 4 transactions paid using GAS



#   times_to_reinvest_per_year = f'1 year: {current_staked_assets} * (1 + {current_apy}/x)^x - {transaction_fee}*x\n'

  ts = {0.08333333 : 30, 0.25 : 91, 0.5 : 182, 0.75 : 275, 1 : 365} # all the t's for the compound interest formula [1 month, 3 months, 6 months, 9 months, 1 year]
  extremes = {} # Hold the

  # https://stackoverflow.com/questions/10146924/finding-the-maximum-of-a-function
  def compound(x, t):
    return current_staked_assets * (1 + ((current_apy * current_price_flm) / x))**(x*t) - transaction_fee*x # compound formula

  for key, value in ts.items():
    extremes[value] = scipy.optimize.fmin(lambda x: -compound(x, key), 0).tolist() # Find the maximum of function to find best n

  

  n_in_days = [] # How many times you should claim the FLM in a given amount of time [1 month, 3 months, 6 months, 9 months, 1 year]
  n_in_flamingo = [] # Every how many accumulated FLM you should claim it
       
  for key, value in extremes.items():
    # print(extreme)
    n_in_days.append(key / value[0])

  for i in n_in_days:
    n_in_flamingo.append(i * flm_current_rate_of_production_per_day)
  
  os.system('cls')
  
  print(extremes)
  print(transaction_fee)

  print(f'In 1 month you should every {n_in_days[0]} days \n\
          In 3 months you should every {n_in_days[1]} days \n\
          In 6 months you should every {n_in_days[2]} days \n\
          In 9 months you should every {n_in_days[3]} days \n\
          In 1 year you should every {n_in_days[4]} days \n')
  
  print(f'In 1 month you should reinvest after you have accumulated: {n_in_flamingo[0]} FLM \n\
          In 3 months you should reinvest: {n_in_flamingo[1]} FLM\n\
          In 6 months you should reinvest: {n_in_flamingo[2]} FLM\n\
          In 9 months you should reinvest: {n_in_flamingo[3]} FLM\n\
          In 1 year you should reinvest: {n_in_flamingo[4]} FLM\n')

  def round2dec(number):
    return str(round(number, 2))

  def color(number):
    return Color('{autogreen}' + round2dec(number) + '{/autogreen}') if number > 0 else Color('{autored}' + round2dec(number) + '{/autored}')

  coins = {'NEO' : data['data']['1376']['quote']['USD'], 'FLM' : data['data']['7150']['quote']['USD'], 'GAS' : data['data']['1785']['quote']['USD']} 
  #   print(data)
#   parseData = json.dumps(response.json())
 
  table_data = [
    ['', 'NEO', 'FLM', 'GAS', 'NEO / FLM', 'NEO / GAS', 'GAS / FLM'],
    ['Price', '$ ' + round2dec(coins['NEO']['price']), '$ ' + round2dec(coins['FLM']['price']), '$ ' + round2dec(coins['GAS']['price']), round2dec(coins['NEO']['price'] / coins['FLM']['price']) + ' FLM', round2dec(coins['NEO']['price'] / coins['GAS']['price']) + ' GAS', round2dec(coins['GAS']['price'] / coins['FLM']['price']) + ' FLM'],
    ['Percent Change 24h', '% ' + color(coins['NEO']['percent_change_24h']), '% ' + color(coins['FLM']['percent_change_24h']), '% ' + color(coins['GAS']['percent_change_24h']) ],
    ['Percent Change 7d', '% ' + color(coins['NEO']['percent_change_7d']), '% ' + color(coins['FLM']['percent_change_7d']), '% ' + color(coins['GAS']['percent_change_7d'])],
    ['Percent Change 30d', '% ' + color(coins['NEO']['percent_change_30d']), '% ' + color(coins['FLM']['percent_change_30d']), '% ' + color(coins['GAS']['percent_change_30d'])],
    ['Market cap', '$ ' + str(int(coins['NEO']['market_cap'])), '$ ' + str(int(coins['FLM']['market_cap'])), '$ ' + str(int(coins['GAS']['market_cap']))]
  ]

  table = AsciiTable(table_data)
  print(table.table)



#   print(f'Enter current formula: {times_to_reinvest_per_year} in a graphic calculator')

#   n = int(input('Amount of times to reinvest: '))

#   one_year_n_in_days = 365 / max_1_year[0]
#   one_month_n_in_days = 365 / max_1_month[0]
#   three_months_n_in_days = 365 / max_3_months[0]
#   six_months_n_in_days = 365 / max_6_months[0]
#   nine_months_n_in_days = 365 / max_9_months[0]

#   one_year_n_in_flamingo = one_year_n_in_days * flm_current_rate_of_production_per_day
#   one_month_n_in_flamingo = one_month_n_in_days * flm_current_rate_of_production_per_day
#   three_months_n_in_flamingo = three_months_n_in_days * flm_current_rate_of_production_per_day
#   six_months_n_in_flamingo = six_months_n_in_days * flm_current_rate_of_production_per_day
#   nine_months_n_in_flamingo = nine_months_n_in_days * flm_current_rate_of_production_per_day

#   print(one_year_n_in_flamingo)
#   print(one_month_n_in_flamingo)
#   print(three_months_n_in_flamingo)
#   print(six_months_n_in_flamingo)
#   print(nine_months_n_in_flamingo)


#   n_in_days = 365 / n
#   n_in_flamingo = n_in_days * flm_current_rate_of_production_per_day

#   print(f'With the information provided you should reinvest when you have {n_in_flamingo} FLM')

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

    # times_to_reinvest_per_month = f'1 month: {current_staked_assets} * (1 + {current_apy}/x)^(x*0.08333333) - {transaction_fee}*x\n'
#   times_to_reinvest_per_3_months = f'3 months: {current_staked_assets} * (1 + {current_apy}/x)^(x*0.25) - {transaction_fee}*x\n'
#   times_to_reinvest_per_6_months = f'6 months: {current_staked_assets} * (1 + {current_apy}/x)^(x*0.5) - {transaction_fee}*x\n'
#   times_to_reinvest_per_9_months = f'9 months: {current_staked_assets} * (1 + {current_apy}/x)^(x*0.75) - {transaction_fee}*x\n'


#   print('Amount to reinvest 1 year: ' + str(max_1_year[0]))
#   print('Amount to reinvest 1 month: ' + str(max_1_month[0]))
#   print('Amount to reinvest 3 months: ' + str(max_3_months[0]))
#   print('Amount to reinvest 6 months: ' + str(max_6_months[0]))
#   print('Amount to reinvest 9 months: ' + str(max_9_months[0]))

#   print(times_to_reinvest_per_3_months)
#   print(times_to_reinvest_per_6_months)
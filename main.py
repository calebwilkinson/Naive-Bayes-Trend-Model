import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
from SQL_Server_Access import Access_Server
from AAII_Graph import AAII_Net_Positioning
import Indicators as indi
import forward_returns as fr

cursor = Access_Server()

cursor.execute('SELECT Date,Price FROM SPX')

stochastics_data, server_data = indi.stochastics("SPX", 5)

rsi_data, data = indi.rsi("SPX", 14)

# Periods to get forward-looking returns of
periods_to_test = [1, 2, 3, 5, 7, 10]
# List to hold [(period, avg return of sub twenty percentile reading, avg return of above eighty percentile reading), (...)]
periods_fwd_returns = []
morelist = []

for period in periods_to_test:
    # Take stochastic data
    avg_twenty_return, avg_eighty_return = fr.percentile_and_forward_return(stochastics_data, server_data, period, "SPX")
    periods_fwd_returns.append([period, avg_twenty_return, avg_eighty_return])

for period in periods_to_test:
    avg_twenty_return, avg_eighty_return = fr.percentile_and_forward_return(rsi_data, data, period, "SPX")
    morelist.append([period, avg_twenty_return, avg_eighty_return])


print(periods_fwd_returns)
print(morelist)









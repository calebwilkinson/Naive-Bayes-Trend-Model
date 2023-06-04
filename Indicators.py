
from SQL_Server_Access import Access_Server
import numpy as np


def stochastics(server_data): # server_data format: list = [Date, Price, High, Low]
    np_array = np.array(server_data)
    period_low = min(np_array[:, 3])
    period_high = max(np_array[:, 2])
    close_price = server_data[-1][1] #  Most recent closing price in list.

    denominator = .00000001 if (period_high - period_low) == 0 else (period_high-period_low)
    # return(100 * ((close_price - low_of_day) / (high_of_day - low_of_day))) # Stochastics calculation
    return(100 * ((close_price - period_low) / denominator))

def rsi(server_data):
    gain, loss = 0, 0
    # First RSI calculation step
    # Calculates the first RSI using the selected period
    for row in server_data:
        if row[4] > 0:
            gain += (row[4])
        elif row[4] < 0:
            loss += abs(row[4])
    avg_gain = gain / len(server_data)

    avg_loss = (loss / len(server_data)) if loss != 0 else .00001

    # Calculate RS (relative strength) and RSI (relative strength indicator)
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def correlation(ticker1, ticker2, period):
    cursor = Access_Server()
    cursor.execute("SELECT TOP 1008 " + ticker1 + ".Date, " + ticker1 + ".[Change %], " + ticker2 + ".Date, " + ticker2 + ".[Change %] FROM " + ticker2 + " INNER JOIN " + ticker1 + " ON " + ticker2 + ".Date = " + ticker1 + ".Date Order by " + ticker1 + ".Date DESC")

    start, end = 0, period
    ticker1_data = (list(reversed(cursor.fetchall())))

    period_correlations = []
    while end <= 1008:
        ticker1 = []
        ticker2 = []

        for count, value in enumerate(ticker1_data[start:end]):
            ticker1.append(value[1])
            ticker2.append(value[3])

        corr_coef = np.corrcoef(ticker1, ticker2)
        period_correlations.append(corr_coef[0][1])
        # print("DXY and Gold has a correlation coefficient of: " + str(corr_coef[0][1]) + " for the past " + str(period) + " days.")
        start += 1
        end += 1
    return period_correlations



















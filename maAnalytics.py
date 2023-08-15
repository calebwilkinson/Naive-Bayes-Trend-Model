import SQL_Server_Access as sql
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# Checks for 20D Moving Average break. Inserts Direction of break in Ticker_20d_MA_Value Table.
def ma_break(ticker, date):
    ma_tbl_data = sql.select_on_date(ticker+'_20D', date)
    ticker_data = sql.select_on_date(ticker, date)
    # ma_tbl_data Format = | Date | Price | Twenty_MA | StdDev_1 | StdDev_2 | StdDev_3 |
    # ticker_data Format = | Date | Price | Open | High | Low | Change %

    if ma_tbl_data[1] >= ma_tbl_data[2]: # If price above 20_MA
        sql.update_col_on_date(ticker + '_20d_MA_Value', 'MA_BREAK', 'ABOVE', date)
    elif ma_tbl_data[1] < ma_tbl_data[2]: # If price below 20_MA
        sql.update_col_on_date(ticker + '_20d_MA_Value', 'MA_BREAK', 'BELOW', date)

# Calculates Two Standard Deviation, checks ticker's price relation.
def two_stdDev(ticker, date):
    ma_tbl_data = sql.select_on_date(ticker+'_20D', date)
    # ma_tbl_data Format = | Date | Price | Twenty_MA | StdDev_1 | StdDev_2 | StdDev_3 |
    ticker_data = sql.select_on_date(ticker, date)
    # ticker_data Format = | Date | Price | Open | High | Low | Change %

    up_2std = ma_tbl_data[4] + ma_tbl_data[2]
    down_2std = ma_tbl_data[2] - ma_tbl_data[4]
    check_2std_up = bool(ticker_data[3] >= up_2std >= ticker_data [4])
    check_2std_down = bool(ticker_data[3] >= down_2std >= ticker_data [4])

    if check_2std_up:
        if ma_tbl_data[1] >= up_2std: # If closing price >= +2StdDev -> Upward Acceptance
            sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'UP', date)
        else: # If closing price is less than +2StdDev -> Upward Rejection
            sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'UP', date)
    elif check_2std_down:
        if ma_tbl_data[1] <= down_2std: # If closing price is <= -2StdDev -> Downward Acceptance
            sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'DOWN', date)
        else: # Closing price is greater than -2StdDev -> Downward Rejection
            sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'DOWN', date)
    elif ma_tbl_data[1] >= up_2std:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'ABOVE', date)
    elif ma_tbl_data[1] <= down_2std:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'DOWN', date)
    else:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '2STD_BREAK', 'NONE', date)

# Gets One Standard Deviation, checks ticker's price relation.
def one_stdDev(ticker, date):
    ma_tbl_data = sql.select_on_date(ticker + '_20D', date)
    # ma_tbl_data Format = | Date | Price | Twenty_MA | StdDev_1 | StdDev_2 | StdDev_3 |
    ticker_data = sql.select_on_date(ticker, date)
    # ticker_data Format = | Date | Price | Open | High | Low | Change %

    up_1std = ma_tbl_data[2] + ma_tbl_data[3]
    down_1std = ma_tbl_data[2] - ma_tbl_data[3]
    check_1std_up = bool(ticker_data[3] >= up_1std >= ticker_data[4])
    check_1std_down = bool(ticker_data[3] >= down_1std >= ticker_data[4])

    if check_1std_up:
        if ma_tbl_data[1] >= up_1std :  # If closing price >= +2StdDev -> Upward Acceptance
            sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'UP', date)
        else:  # If closing price is less than +2StdDev -> Upward Rejection
            sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'UP', date)
    elif check_1std_down:
        if ma_tbl_data[1] <= down_1std:  # If closing price is <= -2StdDev -> Downward Acceptance
            sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'DOWN', date)
        else:  # Closing price is greater than -2StdDev -> Downward Rejection
            sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'DOWN', date)
    elif ma_tbl_data[1] >= up_1std:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'ABOVE', date)
    elif ma_tbl_data[1] <= down_1std:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'DOWN', date)
    else:
        sql.update_col_on_date(ticker + '_20d_MA_Value', '1STD_BREAK', 'NONE', date)

def get_value(sector_tickers, date, dict_name):
    global value
    overbought_score, oversold_score, neutral_score = 0, 0, 0
    period_list = [5,10,15,20]

    for period in period_list:
        for ticker, weighting in sector_tickers.items():
            rsi = sql.select_col_on_date(ticker + '_Indicators', 'RSI_' + str(period) + 'd', date)
            stoch = sql.select_col_on_date(ticker + '_Indicators', 'Stochastics_' + str(period) + 'd', date)

            try:
                x, y = rsi[0], stoch[0]
                a = x + y
            except TypeError:
                break
            if (rsi[0] >= 70) and (stoch[0] >= 80):
                overbought_score += weighting

            elif (rsi[0] <= 30) and (stoch[0] <= 20):
                oversold_score += weighting
            else:
                neutral_score += weighting

        cursor = sql.Access_Server()
        if overbought_score >= (oversold_score and neutral_score):
            cursor.execute("UPDATE Value SET " + dict_name + "_" + str(period) + "d = 'SELL' WHERE Date = ?", date)
        elif oversold_score >= (overbought_score and neutral_score):
            cursor.execute("UPDATE Value SET " + dict_name + "_" + str(period) + "d = 'BUY' WHERE Date = ?", date)
        else:
            cursor.execute("UPDATE Value SET " + dict_name + "_" + str(period) + "d = 'NEUTRAL' WHERE Date = ?;", date)
        cursor.commit()

def percentile_and_forward_return(indicator_data, server_data, period, ticker):
    twenty_perc_returns = 0
    twenty_counter = 0
    eighty_perc_returns = 0
    eighty_counter = 0
    indicator_readings = []
    high_list = []
    low_list = []

    for row in indicator_data:
        indicator_readings.append(row[1])

    # h_percentile = np.percentile(np.array(indicator_data[:][1]), 20)
    new_data = np.array(indicator_data)
    twenty_percentile = np.percentile(np.array(new_data[:, 1]), 20)
    eighty_percentile = np.percentile(np.array(new_data[:, 1]), 80)

    cursor = sql.Access_Server()

    for row in indicator_data:
        if row[1] < twenty_percentile or row[1] > eighty_percentile:
            date = row[0]
            date = str(date.strftime('%Y-%m-%d'))

            # Return the current date and price of the current row and the date and price X(period) days from now
            cursor.execute("SELECT Date, Price, Next_Date, Next_Price FROM (SELECT Date, Price, lead(Date, " + str(
                period) + ") over (order by Date) as Next_Date, lead(Price, " + str(
                period) + ") over (order by Date) as Next_Price FROM " + ticker + ") as t WHERE Date = '" + date + "'")

            next_date = list(cursor.fetchone())
            if next_date[3] is not None:
                fwd_return = ((next_date[3] - next_date[1]) / next_date[1]) * 100

                # print("from " + str(next_date[0]) + " to " + str(next_date[2]) + " the " + str(period) + " return is " + str(fwd_return))

                if row[1] < twenty_percentile:
                    twenty_perc_returns += fwd_return
                    twenty_counter += 1

                    low_list.append(fwd_return)
                if row[1] > eighty_percentile:
                    eighty_perc_returns += fwd_return
                    eighty_counter += 1

                    high_list.append(fwd_return)

    avg_twenty_return = twenty_perc_returns/twenty_counter
    avg_eighty_return = eighty_perc_returns/eighty_counter

    new_high_list = [round(data * 2) / 2 for data in high_list]

    number_of_readings = len(new_high_list)

    counter_dict = Counter(new_high_list)

    fwd_returnnnn = list(counter_dict.keys())

    values = list(counter_dict.values())
    frequency = [x/number_of_readings for x in values]

    fig = plt.figure(figsize = (10, 5))
    plt.bar(fwd_returnnnn, frequency, color = 'maroon', width= 0.4)
    plt.xlabel("Forward Return")
    plt.ylabel("Frequency")
    plt.show()
    return avg_twenty_return, avg_eighty_return

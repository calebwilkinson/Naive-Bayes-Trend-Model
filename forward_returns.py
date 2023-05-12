from SQL_Server_Access import Access_Server
import numpy as np
import datetime

def percentile_and_forward_return(indicator_data, server_data, period, ticker):
    twenty_perc_returns = 0
    twenty_counter = 0
    eighty_perc_returns = 0
    eighty_counter = 0
    indicator_readings = []

    for row in indicator_data:
        indicator_readings.append(row[1])

    twenty_percentile = np.percentile(indicator_readings, 20)
    eighty_percentile = np.percentile(indicator_readings, 80)

    cursor = Access_Server()

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
                if row[1] > eighty_percentile:
                    eighty_perc_returns += fwd_return
                    eighty_counter += 1

    avg_twenty_return = twenty_perc_returns/twenty_counter
    avg_eighty_return = eighty_perc_returns/eighty_counter

    return avg_twenty_return, avg_eighty_return

def forward_return(ticker, date, period):
    cursor = Access_Server()
    cursor.execute("SELECT Date, Price, Next_Date, Next_Price FROM (SELECT Date, Price, lead(Date, " + str(period) + ") over (order by Date) as Next_Date, lead(Price, " + str(period) + ") over (order by Date) as Next_Price FROM " + ticker + ") as t WHERE Date = '" + date + "'")


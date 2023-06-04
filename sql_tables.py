import numpy as np
import yfinance as yf
import maAnalytics as fr
import SQL_Server_Access as sql
import Indicators as indi

# CREATE TABLE FOR A NEW TICKER
def new_ticker_tbl(ticker, yf_name):
     cursor = sql.Access_Server()
     # Create SQL Table for Data
     # Table format: Date | Price | Open | High | Low | Change %
     cursor.execute("CREATE TABLE " + ticker + " ("
                    "[Date] DATETIME NOT NULL, "
                    "[Price] float NOT NULL, "
                    "[Open] float NOT NULL, "
                    "[High] float NOT NULL, "
                    "[Low] float NOT NULL, "
                    "[Change %] float,"
                    "PRIMARY KEY (Date, Price));")
     cursor.commit()
     print('Table ' + ticker + ' has been created.')

     data = yf.download(yf_name, period='max') # Downloads into pandas DataFrame
     prev_price = .1
     for index, row in data.iterrows(): # Index is Date
          change = ((row['Close']-prev_price)/prev_price)*100 # Calculate price Change % from previous close.

          cursor.execute("INSERT INTO " + ticker + " (Date, Price, [Open], High, Low, [Change %]) "
                         "VALUES (?,?,?,?,?,?)",
                         index, row['Close'], row['Open'], row['High'], row['Low'], change)
          prev_price = row['Close']
          cursor.commit()

     cursor.execute('SELECT TOP(1) Date FROM ' + ticker + ' ORDER BY Date DESC')
     date = list(cursor.fetchone())
     print('Data up to ' + date[0].strftime('%Y-%m-%d') + ' has been inserted into ' + ticker + '.')

# CREATE 20 DAY MOVING AVERAGE TABLE
def new_twenty_ma_tbl(ticker):
    cursor = sql.Access_Server()
    # Create SQL Table for Data
    # Table format: Date | Price | Twenty_MA | StdDev_1 | StdDev_2 | StdDev_3
    new_table_name = ticker+"_20D"
    cursor.execute("CREATE TABLE " + new_table_name + " ("
                   "[Date] DATETIME NOT NULL, "
                   "[Price] float NOT NULL, "
                   "[Twenty_MA] float NOT NULL, "
                   "[StdDev_1] float NOT NULL, "
                   "[StdDev_2] float NOT NULL, "
                   "[StdDev_3] float NOT NULL,"
                   "FOREIGN KEY (Date, Price) REFERENCES " + ticker + "(Date, Price));")
    cursor.commit()
    print('Table ' + new_table_name + ' has been created.')

    cursor.execute("SELECT Date,Price FROM " + ticker + " Order By Date ASC")

    server_data = list(cursor.fetchall()) # Date, Price for all dates in ascending order.

    start, end = 0, 20
    price_list = []  # Prices to be used to calculate 20 Day Moving Average

    while end <= len(server_data):
        np_array = np.array(server_data[start:end])
        twenty_sma = (sum(np_array[:, 1])) / 20 # 20 MA Calculation
        std_deviation = np.std(np_array[:, 1]) # Standard Deviation calculation

        cursor.execute("INSERT INTO " + new_table_name + " "
                       "(Date, Price, Twenty_MA, StdDev_1, StdDev_2, StdDev_3) VALUES "
                       "('" + str(server_data[end-1][0]) + "', '"
                       + str(server_data[end-1][1]) + "', "
                       + str(twenty_sma) + ", "
                       + str(std_deviation) + ", "
                       + str(std_deviation*2) + ", "
                       + str(std_deviation*3) + ");")
        cursor.commit()
        price_list.clear()
        start += 1
        end += 1

    date = server_data[-1][0]
    print('Data up to ' + date.strftime('%Y-%m-%d') + ' has been inserted into ' + new_table_name + '.')

# CREATE INDICATORS (RSI & STOCHASTICS) TABLE
def new_indi_tbl(ticker):
    global data_for_period
    cursor = sql.Access_Server()
    # Create SQL Table for Data
    new_table_name = ticker+"_Indicators"
    cursor.execute("CREATE TABLE " + new_table_name + " ("
                   "[Date] DATETIME NOT NULL UNIQUE, "
                   "[Price] float NOT NULL, "
                   "[RSI_3d] float, "
                   "[RSI_5d] float,"
                   "[RSI_10d] float,"
                   "[RSI_15d] float,"
                   "[RSI_20d] float,"
                   "[Stochastics_3d] float, "
                   "[Stochastics_5d] float,"
                   "[Stochastics_10d] float,"
                   "[Stochastics_15d] float,"
                   "[Stochastics_20d] float,"
                   "FOREIGN KEY (Date, Price) REFERENCES " + ticker + "(Date, Price));")
    cursor.commit()
    print('Table ' + new_table_name + ' has been created.')
    # Connect to SQL server

    cursor.execute("SELECT Date,Price,High,Low,[Change %] FROM " + ticker + " Order By Date ASC")

    # Convert server data to a list
    server_data = list(cursor.fetchall())
    period_list = [3,5,10,15,20]

    for period in period_list:
        for count, date in enumerate(server_data):
            out_of_index  = False
            if (count+period) <= len(server_data):
                data_for_period = server_data[count:count+period]
            else:
                out_of_index = True

            if out_of_index:
                break

            stochastics_val = indi.stochastics(data_for_period)
            rsi_val = indi.rsi(data_for_period)
            date_to_insert = data_for_period[-1]
            if period <= 3:
                cursor.execute("INSERT INTO " + new_table_name + " "
                               "(Date, Price, RSI_" + str(period) + "d, Stochastics_" + str(period) + "d)"
                               " VALUES (?,?,?,?);"
                               , date_to_insert[0], date_to_insert[1], rsi_val, stochastics_val)
                cursor.commit()
            else:
                cursor.execute("UPDATE " + new_table_name + " "
                               "SET RSI_" + str(period) + "d = ?, Stochastics_" + str(period) + "d = ? "
                               "WHERE Date = ?;", rsi_val, stochastics_val, date_to_insert[0])
                cursor.commit()
    date = server_data[-1][0]
    print('Data up to ' + date.strftime('%Y-%m-%d') + ' has been inserted into ' + new_table_name + '.')

# CREATE FORWARD RETURNS TABLE
# | Date | Price | Fwd_1d | Fwd_2d | Fwd_3d | Fwd_5d | Fwd_10d | Fwd_15d | Fwd_20d |
def new_fwd_ret_tbl(ticker):
    cursor = sql.Access_Server()
    # Create SQL Table for Data
    new_table_name = ticker+"_Fwd_Returns"
    cursor.execute("CREATE TABLE " + new_table_name + " ("
                   "[Date] DATETIME NOT NULL, "
                   "[Price] float NOT NULL, "
                   "[Fwd_1d] float, "
                   "[Fwd_2d] float, "
                   "[Fwd_3d] float, "
                   "[Fwd_5d] float,"
                   "[Fwd_10d] float,"
                   "[Fwd_15d] float,"
                   "[Fwd_20d] float,"
                   "FOREIGN KEY (Date, Price) REFERENCES " + ticker + "(Date, Price));")
    cursor.commit()
    print('Table ' + ticker + '_Fwd_Returns has been created')

    cursor.execute("SELECT Date,Price FROM " + ticker + " Order By Date ASC")
    server_data = list(cursor.fetchall())  # Date, Price for all dates in ascending order.
    period_list = [1,2,3,5,10,15,20]

    for count, data in enumerate(server_data):
        fwd_returns = []
        # Return the current date and price of the current row and the date and price X(period) days from now
        for period in period_list:
            if (count+period) < len(server_data):
                delta = ((server_data[count+period][1] - server_data[count][1]) / server_data[count][1]) * 100
                fwd_returns.append(delta)
            else:
                fwd_returns.append(None)

        cursor.execute("INSERT INTO " + new_table_name + " "
                       "(Date, Price, Fwd_1d, Fwd_2d, Fwd_3d, "
                       "Fwd_5d, Fwd_10d, Fwd_15d, Fwd_20d) VALUES (?,?,?,?,?,?,?,?,?)",
                       data[0], data[1], fwd_returns[0], fwd_returns[1], fwd_returns[2],
                       fwd_returns[3], fwd_returns[4], fwd_returns[5], fwd_returns[6])
        cursor.commit()


    date = server_data[-1][0]
    print('Data up to ' + date.strftime('%Y-%m-%d') + ' has been inserted into ' + new_table_name + '.')

def update_tickers(ticker_dict):
    for ticker, yf_name in ticker_dict.items():
        cursor = sql.Access_Server()
        cursor.execute("SELECT * FROM " + ticker + " WHERE Date = (SELECT MAX(Date) FROM " + ticker + ")") # Most recent date
        recent_date = list(cursor.fetchone())
        data = yf.download(yf_name, start= recent_date[0])  # Downloads into pandas DataFrame

        if (len(data) <= 1):
            print(ticker + ' is already up to date.')
        else:
            prev_price = 0
            for index, row in data.iterrows():  # Index is Date
                if index == recent_date[0]:
                    prev_price = row['Close']
                else:
                    change = ((row['Close'] - prev_price) / prev_price) * 100  # Calculate price Change % from previous close.
                    cursor.execute("INSERT INTO " + ticker + " (Date, Price, [Open], High, Low, [Change %]) "
                                   "VALUES (?,?,?,?,?,?)",
                                   index, row['Close'], row['Open'], row['High'], row['Low'], change)
                    prev_price = row['Close']
                    cursor.commit()
                    update_indicators(ticker)
                    update_twenty_ma(ticker)
                    update_fwd_returns(ticker)
            print(ticker + ' is now up to date.')

def update_indicators(ticker):
    period_list = [3, 5, 10, 15, 20]

    for period in period_list:
        cursor = sql.Access_Server()
        cursor.execute("SELECT TOP(" + str(period) + ") Date, Price, High, Low, [Change %] FROM " + ticker + " ORDER BY Date DESC")
        server_data = list(cursor.fetchall())
        rsi_val, stochastics_val = indi.rsi(server_data), indi.stochastics(server_data)
        if period == 3:
            cursor.execute("INSERT INTO " + ticker + "_Indicators "
                           "(Date, Price, RSI_" + str(
                           period) + "d, Stochastics_" + str(period) + "d)"
                           " VALUES (?,?,?,?);"
                           , server_data[0][0], server_data[0][1], rsi_val, stochastics_val)
            cursor.commit()
        else:
            cursor.execute("UPDATE " + ticker + "_Indicators "
                           "SET RSI_" + str(period) + "d = ?, Stochastics_" + str(
                           period) + "d = ? "
                           "WHERE Date = ?;", rsi_val, stochastics_val, server_data[0][0])
            cursor.commit()
        cursor.commit()

def update_twenty_ma(ticker):
    cursor = sql.Access_Server()
    cursor.execute("SELECT TOP(20) Date, Price FROM " + ticker + " ORDER BY Date DESC")
    price_list = np.array(list(cursor.fetchall()))
    twenty_sma = (sum(price_list[:, 1])) / 20
    std_deviation = np.std(price_list[:, 1])

    cursor.execute("INSERT INTO " + ticker + "_20d "
                   "(Date, Price, Twenty_MA, StdDev_1, StdDev_2, StdDev_3) VALUES "
                   "('" + str(price_list[0][0]) + "', '"
                   + str(price_list[0][1]) + "', "
                   + str(twenty_sma) + ", "
                   + str(std_deviation) + ", "
                   + str(std_deviation * 2) + ", "
                   + str(std_deviation * 3) + ");")
    cursor.commit()

def update_fwd_returns(ticker):
    cursor = sql.Access_Server()
    cursor.execute("SELECT TOP(21) Date, Price FROM " + ticker + " ORDER BY Date DESC")
    price_list = list(cursor.fetchall())

    period_list = [1,2,3,5,10,15,20]

    cursor.execute("INSERT INTO " + ticker + "_Fwd_Returns "
                   "(Date, Price, Fwd_1d, Fwd_2d, Fwd_3d, Fwd_5d, Fwd_10d, Fwd_15d, Fwd_20d"
                   ") VALUES (?,?,?,?,?,?,?,?,?)",
                   price_list[0][0], price_list[0][1], None, None, None, None, None, None, None)

    for period in period_list:
        delta = ((price_list[0][1]- price_list[period][1]) / price_list[0][1]) * 100
        cursor.execute("UPDATE " + ticker + "_Fwd_Returns "
                           "SET Fwd_" + str(period) + "d = ? WHERE Date = ?",
                           delta, price_list[period][0] )

    cursor.commit()

def new_value_tbl():
    cursor = sql.Access_Server()
    cursor.execute("CREATE TABLE Value ("
                   "[Date] DATETIME, "
                   "[SPX_Price] float, "
                   "[Sector_5d] varchar(255), "
                   "[Sector_10d] varchar(255), "
                   "[Sector_15d] varchar(255), "
                   "[Sector_20d] varchar(255),"
                   "[SP25_5d] varchar(255), "
                   "[SP25_10d] varchar(255), "
                   "[SP25_15d] varchar(255), "
                   "[SP25_20d] varchar(255), "
                   "[Index_5d] varchar(255), "    
                   "[Index_10d] varchar(255), "                                
                   "[Index_15d] varchar(255), "                                
                   "[Index_20d] varchar(255), " 
                   "[Currency_5d] varchar(255), "
                   "[Currency_10d] varchar(255), "
                   "[Currency_15d] varchar(255), "
                   "[Currency_20d] varchar(255), "
                   "[SP4_5d] varchar(255), "
                   "[SP4_10d] varchar(255), "
                   "[SP4_15d] varchar(255), "
                   "[SP4_20d] varchar(255));")
    cursor.commit()
    cursor.execute("INSERT INTO Value (Date, SPX_Price) SELECT Date, Price FROM SPX")
    cursor.commit()
    print('Table Value has been created. Date and Price from SPX have been inserted. ')

def new_20dma_value(ticker):
    cursor = sql.Access_Server()
    tbl_name = ticker + '_20d_MA_Value'
    cursor.execute('CREATE TABLE ' + tbl_name + ' ('
                   '[Date] DATETIME NOT NULL,'
                   '['+ ticker+ '_Price] float NOT NULL,'
                   '[20d_MA] float NOT NULL,'
                   '[MA_BREAK] varchar(255),'
                   '[1STD_BREAK] varchar(255),'
                   '[2STD_BREAK] varchar(255),'
                   'PRIMARY KEY (Date, ' + ticker + '_Price))')
    cursor.commit()
    print(ticker + '_20d_MA_Value table has been created.')

    ticker_data = sql.select_all(ticker)

    for data in ticker_data:
        date = data[0].strftime('%Y-%m-%d')
        if date == '2004-01-02':
            return
        cursor.execute("INSERT INTO " + tbl_name + " (Date, " + ticker + "_Price, [20d_MA]) SELECT Date, Price, Twenty_MA FROM [" + ticker + "_20D] WHERE Date =  '" + date + "';")
        cursor.commit()

        fr.ma_break(ticker, date)
        fr.one_stdDev(ticker, date)
        fr.two_stdDev(ticker, date)

    print('Data has been inserted')

def update_ma_table(ticker):
    ticker_data = sql.select_most_recent(ticker) # Selects most recent Date entry.
    value = sql.select_most_recent(ticker + '_20D_MA_VALUE')

    if value[0][0] == ticker_data[0][0]: # Assumes SPX is up-to-date.
        print('Tables are both up to date.')
    else:
        cursor = sql.Access_Server()
        cursor.execute("SELECT Date, Price FROM " + ticker + " WHERE Date > '" + value[0][0].strftime('%Y-%m-%d') + "' ORDER BY Date ASC")
        new_value = list(cursor.fetchall())

        for data in new_value:
            date = data[0].strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO " + ticker + "_20D_MA_Value (Date, " + ticker + "_Price, [20d_MA]) SELECT Date, Price, Twenty_MA FROM [" + ticker + "_20D] WHERE Date = '" + date + "';")
            cursor.commit()
            fr.ma_break(ticker, date)
            fr.one_stdDev(ticker, date)
            fr.two_stdDev(ticker, date)

# Script to fill blank Values table.
def value_tbl_insert(ticker_dict, dict_name):
    global start_date, end_date
    cursor = sql.Access_Server()
    cursor.execute("SELECT Date FROM Value ORDER BY Date DESC")
    server_data = cursor.fetchall()

    for date in server_data:
        fr.get_value(ticker_dict, date[0].strftime('%Y-%m-%d'), dict_name)

# Updates Value table with all missing dates and calculations.
def update_value_tbl(sector_tickers, top_25_tickers, top_4_tickers, index_tickers, currency_tickers):
    spx_data = sql.select_most_recent('SPX') # Selects most recent Date entry.
    value = sql.select_most_recent('Value')
    if value[0] == spx_data[0]: # Assumes SPX is up-to-date.
        print('Tables are both up to date.')
    else:
        cursor = sql.Access_Server()
        cursor.execute("SELECT Date, Price FROM SPX WHERE Date > '" + value[0][0].strftime('%Y-%m-%d') + "' ORDER BY Date ASC")
        new_value = list(cursor.fetchall())

        for data in new_value:
            date = data[0].strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO Value (Date, SPX_Price) SELECT Date, Price FROM SPX WHERE Date = '" + date + "';")
            cursor.commit()

            # Fill value table
            fr.get_value(sector_tickers, date, 'Sector')
            fr.get_value(top_25_tickers, date, 'SP25')
            fr.get_value(top_4_tickers, date, 'SP4')
            fr.get_value(index_tickers, date, 'Index')
            fr.get_value(currency_tickers, date, 'Currency')

        print('Value table is now up to date.')





























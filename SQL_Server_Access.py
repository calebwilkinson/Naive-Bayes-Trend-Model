import pandas as pd
import pyodbc

# Notes: Date format =  yyyy-mm-dd

# SQl Server Connection
def Access_Server():
    server = 'DESKTOP-4A1MPI2\SQLEXPRESS'
    database = 'master'
    username = 'caleb'
    password = 'Wsnoopy811'
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-4A1MPI2\SQLEXPRESS;"
                          "Database=master;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()

    return cursor

cursor = Access_Server()

# Selects all columns from ticker table.
def select_all(ticker):
    cursor.execute("SELECT * FROM " + ticker + " ORDER BY Date DESC")
    return list(cursor.fetchall())

# Selects all columns on given date.
def select_on_date(ticker, date):
    cursor.execute("SELECT * FROM " + ticker + " WHERE Date='" + date +"'")
    return list(cursor.fetchone())

# Selects specific column on given date.
def select_col_on_date(ticker, col, date):
    try:
        cursor.execute("SELECT " + col + " FROM " + ticker + " WHERE Date = '" + date + "'")
        something = list(cursor.fetchone())
        return something
    except Exception as e:
        print(e)

# Selects single row that contains most recent date.
def select_most_recent(ticker):
    cursor.execute("SELECT TOP(1) * FROM " + ticker + " ORDER BY Date DESC")
    return list(cursor.fetchall())

# Updates column on specified date.
def update_col_on_date(tbl_name, col, value, date):
    cursor.execute("UPDATE " + tbl_name + " SET [" + col + "] = '" + value + "' WHERE Date = '" + date + "'")
    cursor.commit()

# Selects all columns and rows between date1 and date2.
def select_between(ticker, date1, date2):
    cursor.execute("SELECT Date, [Change %] FROM " + ticker + " WHERE Date "
                   "BETWEEN '" + date1 + "' and '" + date2 + "'")
    return cursor.fetchall()

# Selects all RSI data for model training.
def rsi_train_select(ticker):
    date, rsi_3d, rsi_5d, rsi_10d, rsi_15d, fwd = [],[],[],[],[],[]
    cursor.execute("SELECT Date, RSI_3d, RSI_5d, "
                   "RSI_10d, RSI_15d "
                   "FROM "+ticker+"_Indicators "
                   "WHERE "+ticker+"_Indicators.Date >= '2004-01-05' and "+ticker+"_Indicators.Date <= '2022-04-20' ORDER BY DATE DESC")

    for row in cursor.fetchall():
        date.append(row[0])
        rsi_3d.append(row[1])
        rsi_5d.append(row[2])
        rsi_10d.append(row[3])
        rsi_15d.append(row[4])

    df = pd.DataFrame(
        {'RSI_3d':rsi_3d,
         'RSI_5d':rsi_5d,
         'RSI_10d':rsi_10d,
         'RSI_15d':rsi_15d}
        )
    return df

# For rsi and stochastics scatter-plot.
# Selects top 1000 rows.
def rsi_stoch_all(period):
    cursor.execute("SELECT TOP(1000) SPX_Indicators.RSI_"+str(period)+"d, spx_Indicators.Stochastics_"+str(period)+"d, "
                   "spx_fwd_returns.fwd_"+str(period)+"d FROM spx_Indicators INNER JOIN spx_fwd_returns ON "
                   "spx_Indicators.date = spx_fwd_returns.date ORDER BY spx_Indicators.Date DESC")
    return cursor.fetchall()

# Selects all stochastics data for model testing.
def stoch_test_select(ticker):
    date, stoch_3d, stoch_5d, stoch_10d, stoch_15d, fwd = [],[],[],[],[],[]
    cursor.execute("SELECT TOP(252) Date, Stochastics_3d, Stochastics_5d, "
                   "Stochastics_10d, Stochastics_15d "
                   "FROM "+ticker+"_Indicators "
                   "WHERE Date < '2023-05-12' ORDER BY DATE DESC")

    for row in cursor.fetchall():
        date.append(row[0])
        stoch_3d.append(row[1])
        stoch_5d.append(row[2])
        stoch_10d.append(row[3])
        stoch_15d.append(row[4])

    df = pd.DataFrame(
        {'stoch_3d':stoch_3d,
         'stoch_5d':stoch_5d,
         'stoch_10d':stoch_10d,
         'stoch_15d':stoch_15d,
         }
        )
    return df

# Selects all stochastics data for model training.
def stoch_train_select(ticker):
    date, stoch_3d, stoch_5d, stoch_10d, stoch_15d, fwd = [],[],[],[],[],[]
    cursor.execute("SELECT Date, Stochastics_3d, Stochastics_5d, "
                   "Stochastics_10d, Stochastics_15d "
                   "FROM "+ticker+"_Indicators "
                   "WHERE Date >= '2004-01-05' and "+ticker+"_Indicators.Date <= '2022-04-20' ORDER BY DATE DESC")

    for row in cursor.fetchall():
        date.append(row[0])
        stoch_3d.append(row[1])
        stoch_5d.append(row[2])
        stoch_10d.append(row[3])
        stoch_15d.append(row[4])

    df = pd.DataFrame(
        {'stoch_3d':stoch_3d,
         'stoch_5d':stoch_5d,
         'stoch_10d':stoch_10d,
         'stoch_15d':stoch_15d,
         }
        )
    return df

# Selects all RSI data for model testing.
def rsi_test_select(ticker):
    date, rsi_3d, rsi_5d, rsi_10d, rsi_15d, fwd = [],[],[],[],[],[]
    cursor.execute("SELECT TOP(252) Date, RSI_3d, RSI_5d, RSI_10d, RSI_15d "
                   "FROM "+ticker+"_Indicators "
                   "WHERE Date < '2023-05-12' ORDER BY DATE DESC")

    for row in cursor.fetchall():
        date.append(row[0])
        rsi_3d.append(row[1])
        rsi_5d.append(row[2])
        rsi_10d.append(row[3])
        rsi_15d.append(row[4])

    df = pd.DataFrame(
        {'RSI_3d':rsi_3d,
         'RSI_5d':rsi_5d,
         'RSI_10d':rsi_10d,
         'RSI_15d':rsi_15d}
        )
    return df

# Selects training data from the ticker_20d_ma_value table.
def training_select(ticker):
    cursor.execute("SELECT * FROM " + ticker + "_20d_MA_Value WHERE Date <= '2022-04-20' ORDER BY DATE DESC")
    return cursor.fetchall()

# Selects testing data from the ticker_20d_ma_value table.
def test_select(ticker):
    cursor.execute("SELECT TOP(252) * FROM " + ticker + "_20d_MA_Value WHERE Date < '2023-05-12' ORDER BY Date DESC")
    return cursor.fetchall()

# Selects ticker_20_MA_Value and the 3, 5, 10, and 15 day forward returns from date.
def combo_on_date(ticker, data1, data2, data3, date):
    date = date.strftime('%Y-%m-%d')
    cursor.execute("SELECT "+ticker+"_20d_MA_Value.Date, "+ticker+"_fwd_Returns.Fwd_3d, "+ticker+"_fwd_returns.Fwd_5d, "
                   ""+ticker+"_fwd_returns.Fwd_10d, "+ticker+"_fwd_returns.Fwd_15d FROM "+ticker+"_20d_ma_value INNER JOIN "
                   ""+ticker+"_fwd_returns ON("+ticker+"_20d_ma_value.date = "+ticker+"_fwd_returns.date) WHERE "
                   ""+ticker+"_20d_MA_Value.ma_break = '"+data1+"' and "+ticker+"_20d_MA_Value.[1std_break] = '"+data2+"' and "
                   ""+ticker+"_20d_MA_Value.[2std_break] = '"+data3+"' and "+ticker+"_20d_MA_Value.date = '"+date+"'")
    return cursor.fetchall()






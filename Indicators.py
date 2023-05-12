from SQL_Server_Access import Access_Server

def stochastics(ticker, period):
    # Connect to SQL server
    cursor = Access_Server()
    cursor.execute("SELECT TOP(252) Date,Price,High,Low FROM " + ticker + " Order By Date DESC")

    # Convert server data to a list
    server_data = list(reversed(cursor.fetchall()))
    start = 0
    end = period + 1
    low_of_day = 20000
    high_of_day = 0

    # List to hold calculated stochastics and corresponding date
    stochastic_readings = []

    # Gather stochastics data from the past 252 day
    while end <= 252:
        # Finds the high and lows for the selected rolling period (5 & 14 are common)
        for row in server_data[start:end]:
            if row[3] < low_of_day:
                low_of_day = row[3]
            if row[2] > high_of_day:
                high_of_day = row[2]

        # Most recent close for the selected period
        close_price = server_data[end-1][1]

        # Stochastics calculation
        stochastic_calc = 100 * ((close_price - low_of_day) / (high_of_day - low_of_day))

        stochastic_readings.append([server_data[end-1][0], stochastic_calc])

        # Reset variables and roll period up by 1 day
        start += 1
        end += 1
        low_of_day = 200000
        high_of_day = 0

    return stochastic_readings, server_data

def rsi(ticker, period):
    # Access SQL Server
    cursor = Access_Server()
    cursor.execute("SELECT TOP(252) Date,Price,[Change %]FROM " + ticker + " Order By Date DESC")

    # Server data in a list
    raw_data = list(reversed(cursor.fetchall()))

    rsi_readings = []
    gain = 0
    loss = 0

    # First RSI calculation step
    # Calculates the first RSI using the selected period
    for row in raw_data[0:period+1]:
        if row[2] > 0:
            gain += row[2]
        elif row[2] < 0:
            loss += abs(row[2])

    avg_gain = gain / period
    avg_loss = loss / period

    # Calculate RS (relative strength) and RSI (relative strength indicator)
    rs = avg_gain / avg_loss
    rsi_calc = 100 - (100 / (1 + rs))

    # Date and RSI reading into a list
    rsi_and_date = [raw_data[period-1][0], rsi_calc]
    rsi_readings.append(rsi_and_date)

    # RSI calculation for days 252-period
    for row in raw_data[period:]:
        if row[2] > 0:
            gain = row[2]
            loss = 0
        elif row[2] < 0:
            loss = row[2]
            gain = 0

        avg_gain = ((avg_gain * (period-1)) + gain) / period
        avg_loss = ((avg_loss * (period-1)) + abs(loss)) / period

        rs = avg_gain / avg_loss
        rsi_calc = 100 - (100 / (1 + rs))

        rsi_and_date = [row[0], rsi_calc]
        rsi_readings.append(rsi_and_date)

        return rsi_readings, raw_data

def 20










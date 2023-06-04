import numpy as np
import SQL_Server_Access as sql

def fwd_return(ticker):
    cursor = sql.Access_Server()
    cursor.execute("select * from " + ticker + " WHERE YEAR(Date) >= (YEAR(GETDATE()) - 1) ORDER BY Date ASC")
    server_data = list(cursor.fetchall())
    above_2std_dev = []
    for date in server_data:
        if date[1] >= (date[2] + date[4]):
            above_2std_dev.append(date)

    return above_2std_dev
# calculate standard deviations

def strength_push(ticker):
    data_list = np.array(sql.select_all(ticker + '_20D'))

    for count, data in enumerate(data_list):
        try:
            trend = bool(data_list[count+2:count+7, 1] < data_list[count+2:count+7, 2])
            trend_break = bool((data[1] > data[2]) and (data_list[count+1,1] > data_list[count+1,2]))
            one_std_dev_break = bool(data[1] >= (data[2] + data[3]))
            if trend and (trend_break or one_std_dev_break):
                print('down to up potential trend change')
                check_fwd = sql.select_on_date(ticker + '_Fwd_Returns', data[0])
                print(check_fwd)
        except IndexError:
            return

        try:
            trend = bool(data_list[count+2:count+7, 1] > data_list[count+2:count+7, 2])
            trend_break = bool((data[1] < data[2]) and (data_list[count+1,1] < data_list[count+1,2]))
            one_std_dev_break = bool(data[1] <= (data[2] - data[3]))
            if trend and (trend_break or one_std_dev_break):
                print('up to down potential trend change')
                check_fwd = sql.select_on_date(ticker + '_Fwd_Returns', data[0])
                print(check_fwd)
        except IndexError:
            return






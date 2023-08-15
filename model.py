import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from itertools import product
from sklearn.naive_bayes import GaussianNB # naive Bayes model and prediction
from sklearn.metrics import classification_report, confusion_matrix

import pickle

import SQL_Server_Access

cmap = plt.cm.inferno
import SQL_Server_Access as sql

def query_user():
    val = input('Would you like to view the UP/DOWN prediction for SPX, DJI, RUT, or NDX? reply with index: \n')
    val2 = input('Would you like a prediction over 3, 5, 10, or 15 days? ')
    xtest3, xtest5, xtest10, xtest15, date, price = new_date(val)
    v3, v5, v10, v15 = new_model_data(xtest3,xtest5,xtest10,xtest15, val)

    if int(val2) == 3:
       print(val + " is expected to be up in 3 days!") if v3[0] == 1 else print(val + " is expected to be down in 3 days!")
    elif int(val2) == 5:
       print(val + " is expected to be up in 5 days!") if v3[0] == 1 else print(val + " is expected to be down in 5 days!")
    elif int(val2) == 10:
       print(val + " is expected to be up in 10 days!") if v3[0] == 1 else print(val + " is expected to be down in 10 days!")
    elif int(val2) == 15:
        print(val + " is expected to be up in 15 days!") if v3[0] == 1 else print(val + " is expected to be down in 15 days!")


def train_two_std(ticker):
    data_list = sql.training_select(ticker)
    std2_3d, std2_5d, std2_10d, std2_15d = [], [], [], []
    val = []
    for count, data in enumerate(data_list):
        up_cntr, dwn_cntr = 0, 0

        for x in data_list[count:count + 5]:
            if 'UP' in x[5]:
                up_cntr += 1
            elif 'DOWN' in x[5]:
                dwn_cntr += 1

        cursor = sql.Access_Server()
        cursor.execute("SELECT Fwd_3d, Fwd_5d, Fwd_10d, Fwd_15d FROM SPX_Fwd_Returns WHERE Date = ?", data[0])
        returns = cursor.fetchall()
        std2_3d.append(returns[0][0])
        std2_5d.append(returns[0][1])
        std2_10d.append(returns[0][2])
        std2_15d.append(returns[0][3])

        if up_cntr >= 3:
            val.append(1)
        elif dwn_cntr >= 3:
            val.append(0)
        else:
            val.append(0.5)

    df3 = pd.DataFrame({'Reading': val, '3d_Ret': std2_3d})
    df5 = pd.DataFrame({'Reading': val, '5d Ret': std2_5d})
    df10 = pd.DataFrame({'Reading': val, '10d Ret': std2_10d})
    df15 = pd.DataFrame({'Reading': val, '15d Ret': std2_15d})

    return df3, df5, df10, df15

def test_two_std(ticker):
    data_list = sql.test_select(ticker)
    std2_3d, std2_5d, std2_10d, std2_15d = [], [], [], []
    val = []
    for count, data in enumerate(data_list):
        up_cntr, dwn_cntr = 0, 0

        for x in data_list[count:count + 5]:
            if 'UP' in x[5]:
                up_cntr += 1
            elif 'DOWN' in x[5]:
                dwn_cntr += 1

        cursor = sql.Access_Server()
        cursor.execute("SELECT Fwd_3d, Fwd_5d, Fwd_10d, Fwd_15d FROM SPX_Fwd_Returns WHERE Date = ?", data[0])
        returns = cursor.fetchall()
        std2_3d.append(returns[0][0])
        std2_5d.append(returns[0][1])
        std2_10d.append(returns[0][2])
        std2_15d.append(returns[0][3])

        if up_cntr >= 3:
            val.append(1)
        elif dwn_cntr >= 3:
            val.append(0)
        else:
            val.append(0.5)

    df3 = pd.DataFrame({'Reading': val, '3d_Ret': std2_3d})
    df5 = pd.DataFrame({'Reading': val, '5d Ret': std2_5d})
    df10 = pd.DataFrame({'Reading': val, '10d Ret': std2_10d})
    df15 = pd.DataFrame({'Reading': val, '15d Ret': std2_15d})

    return df3, df5, df10, df15

def train_currency():
    cursor = sql.Access_Server()
    cursor.execute("SELECT * FROM Value WHERE Date <= '2022-04-20' ORDER BY DATE DESC")
    data_list = cursor.fetchall()

    val_l = []
    for data in data_list:
        currency_check = [data[16], data[17]]
        if all(val == 'BUY' for val in currency_check):
            value = 1
        elif all(val == 'SELL' for val in currency_check):
            value = 0
        else:
            value = 0.5
        val_l.append(value)

    return pd.DataFrame({'CurrVal': val_l})

def test_currency():
    cursor = sql.Access_Server()
    cursor.execute("SELECT TOP(252) * FROM Value WHERE Date <= '2023-05-12' ORDER BY DATE DESC")
    data_list = cursor.fetchall()

    val_l = []
    for data in data_list:
        currency_check = [data[16], data[17]]
        if all(val == 'BUY' for val in currency_check):
            value = 1
        elif all(val == 'SELL' for val in currency_check):
            value = 0
        else:
            value = 0.5
        val_l.append(value)

    return pd.DataFrame({'CurrVal': val_l})

def test_ma_combo(ticker):
    readings = ['ABOVE', 'BELOW', 'DOWN', 'UP', 'NONE']
    comb_list = []
    comb_dict = {}

    for l, w, h in product(readings, repeat=3):
        comb_list.append([l, w, h])

    del comb_list[100:]
    for count, comb in enumerate(comb_list):
        comb_dict[count] = comb
    # Date | Price | MA_BREAK | 1std_BREAK | 2std_break
    data_list = sql.test_select(ticker)
    fwd_3, fwd_5, fwd_10, fwd_15 = [],[],[],[]
    pos_or_neg3, pos_or_neg5, pos_or_neg10, pos_or_neg15 = [],[],[],[]

    for data in data_list:
        cl = [data[3], data[4], data[5]]
        comb_num = (list(comb_dict.keys())[list(comb_dict.values()).index(cl)])
        combo_list = sql.combo_on_date(ticker, data[3], data[4], data[5], data[0])

        for combo in combo_list:
            fwd_3.append(comb_num)
            fwd_5.append(comb_num)
            fwd_10.append(comb_num)
            fwd_15.append(comb_num)

            pos_or_neg3.append(1) if combo[1] >= 0 else pos_or_neg3.append(0)
            pos_or_neg5.append(1) if combo[2] >= 0 else pos_or_neg5.append(0)
            pos_or_neg10.append(1) if combo[3] >= 0 else pos_or_neg10.append(0)
            pos_or_neg15.append(1) if combo[4] >= 0 else pos_or_neg15.append(0)

    df3 = pd.DataFrame({'MACombo':fwd_3, 'ActRet':pos_or_neg3})
    df5 = pd.DataFrame({'MACombo':fwd_5, 'ActRet':pos_or_neg5})
    df10 = pd.DataFrame({'MACombo':fwd_10, 'ActRet':pos_or_neg10})
    df15 = pd.DataFrame({'MACombo':fwd_15, 'ActRet':pos_or_neg15})


    return df3, df5, df10, df15

def train_ma_combo(ticker):
    readings = ['ABOVE', 'BELOW', 'DOWN', 'UP', 'NONE']
    comb_list = []
    comb_dict = {}

    for l, w, h in product(readings, repeat=3):
        comb_list.append([l, w, h])

    del comb_list[100:]
    for count, comb in enumerate(comb_list):
        comb_dict[count] = comb
    # Date | Price | MA_BREAK | 1std_BREAK | 2std_break
    data_list = sql.training_select(ticker)
    fwd_3, fwd_5, fwd_10, fwd_15 = [],[],[],[]
    pos_or_neg3, pos_or_neg5, pos_or_neg10, pos_or_neg15 = [],[],[],[]

    for data in data_list:
        cl = [data[3], data[4], data[5]]
        comb_num = (list(comb_dict.keys())[list(comb_dict.values()).index(cl)])

        combo_list = sql.combo_on_date(ticker, data[3], data[4], data[5], data[0])

        for combo in combo_list:
            fwd_3.append(comb_num)
            fwd_5.append(comb_num)
            fwd_10.append(comb_num)
            fwd_15.append(comb_num)

            pos_or_neg3.append(1) if combo[1] >= 0 else pos_or_neg3.append(0)
            pos_or_neg5.append(1) if combo[2] >= 0 else pos_or_neg5.append(0)
            pos_or_neg10.append(1) if combo[3] >= 0 else pos_or_neg10.append(0)
            pos_or_neg15.append(1) if combo[4] >= 0 else pos_or_neg15.append(0)


    df3 = pd.DataFrame({'MACombo':fwd_3, 'ActRet':pos_or_neg3})
    df5 = pd.DataFrame({'MACombo':fwd_5, 'ActRet':pos_or_neg5})
    df10 = pd.DataFrame({'MACombo':fwd_10, 'ActRet':pos_or_neg10})
    df15 = pd.DataFrame({'MACombo':fwd_15, 'ActRet':pos_or_neg15})

    return df3, df5, df10, df15

def train_rsi(ticker): # Returns dataframe containing Date, RSI_5d, RSI_15d
    zf = sql.rsi_train_select(ticker)
    return zf

def test_rsi(ticker): # Returns dataframe containing Date, RSI_5d, RSI_15d
    af = SQL_Server_Access.rsi_test_select(ticker)

    return af

def train_stoch(ticker): # Returns dataframe containing Date, RSI_5d, RSI_15d
    zf = sql.stoch_train_select(ticker)
    return zf

def test_stoch(ticker): # Returns dataframe containing Date, RSI_5d, RSI_15d
    af = SQL_Server_Access.stoch_test_select(ticker)

    return af

def new_date(ticker):

    cursor = sql.Access_Server()
    cursor.execute("SELECT TOP(1) * FROM "+ticker+"_Indicators ORDER BY DATE DESC")
    RSI_3d, RSI_5d, RSI_10d, RSI_15d, stoch_3d, stoch_5d, stoch_10d, stoch_15d = 0,0,0,0,0,0,0,0
    global date
    price = 0
    for row in cursor.fetchall():
        date = row[0]
        price = row[1]
        RSI_3d = row[2]
        RSI_5d = row[3]
        RSI_10d = row[4]
        RSI_15d = row[5]
        stoch_3d = row[7]
        stoch_5d = row[8]
        stoch_10d = row[9]
        stoch_15d = row[10]

    cursor.execute("SELECT TOP(1) * FROM Value ORDER BY Date DESC")
    data_list = cursor.fetchall()
    curr_val = 0
    # Get recent currency value
    for data in data_list:
        currency_check = [data[16], data[17]]
        if all(val == 'BUY' for val in currency_check):
            curr_val = 1
        elif all(val == 'SELL' for val in currency_check):
            curr_val = 0
        else:
            curr_val = 0.5

    #2std Dev checker
    cursor.execute("SELECT TOP(5) * FROM "+ticker+"_20d_ma_value ORDER BY Date DESC")
    data_list = cursor.fetchall()
    up_cntr, dwn_cntr = 0, 0
    for count, data in enumerate(data_list):
        if 'UP' in data[5]:
            up_cntr += 1
        elif 'DOWN' in data[5]:
            dwn_cntr += 1

    if up_cntr >= 3:
        std2_val = 1
    elif dwn_cntr >= 3:
        std2_val = 0
    else:
        std2_val = 0.5

    readings = ['ABOVE', 'BELOW', 'DOWN', 'UP', 'NONE']
    comb_list = []
    comb_dict = {}

    for l, w, h in product(readings, repeat=3):
        comb_list.append([l, w, h])

    del comb_list[100:]
    for count, comb in enumerate(comb_list):
        comb_dict[count] = comb

    cursor.execute("SELECT TOP(1) * FROM " + ticker + "_20d_ma_value ORDER BY Date DESC")
    read_list = cursor.fetchall()

    cl = [read_list[0][3], read_list[0][4], read_list[0][5]]
    comb_num = (list(comb_dict.keys())[list(comb_dict.values()).index(cl)])

    new_test3 = np.array([std2_val, RSI_3d, stoch_3d, comb_num, curr_val])
    new_test5 = np.array([std2_val, RSI_5d, stoch_5d, comb_num, curr_val])
    new_test10 = np.array([std2_val, RSI_10d, stoch_10d, comb_num, curr_val])
    new_test15 = np.array([std2_val, RSI_15d, stoch_15d, comb_num, curr_val])

    return new_test3, new_test5, new_test10, new_test15, date, price

def train_test(ticker):
    df3, df5, df10, df15 = train_two_std(ticker)
    af = train_rsi(ticker)
    hf3, hf5, hf10, hf15 = train_ma_combo(ticker)
    df = train_currency()
    bf = train_stoch(ticker)

    tf3, tf5, tf10, tf15 = test_two_std(ticker)
    qf = test_rsi(ticker)
    rf3, rf5, rf10, rf15 = test_ma_combo(ticker)
    zf = test_currency()
    yf = test_stoch(ticker)

    priors = (0.5, 0.5)
    gnb = GaussianNB(priors = priors)
    x3 = [df3['Reading'], af['RSI_3d'], bf['stoch_3d'], hf3['MACombo'], df['CurrVal']]
    x5 = [df5['Reading'], af['RSI_5d'], bf['stoch_5d'], hf5['MACombo'], df['CurrVal']]
    x10 = [df10['Reading'], af['RSI_10d'], bf['stoch_10d'], hf10['MACombo'], df['CurrVal']]
    x15 = [df15['Reading'], af['RSI_15d'], bf['stoch_15d'], hf15['MACombo'], df['CurrVal']]

    X_train3 = (pd.concat(x3, axis=1, keys=['Reading', 'RSI_3d', 'stoch_3d', 'MACombo', 'CurrVal'])).values
    X_train5 = (pd.concat(x5, axis=1, keys=['Reading', 'RSI_5d', 'stoch_5d', 'MACombo', 'CurrVal'])).values
    X_train10 = (pd.concat(x10, axis=1, keys=['Reading', 'RSI_10d', 'stoch_10d', 'MACombo', 'CurrVal'])).values
    X_train15 = (pd.concat(x15, axis=1, keys=['Reading', 'RSI_15d', 'stoch_15d', 'MACombo', 'CurrVal'])).values

    GaussianNB_fit3 = gnb.fit(X_train3, hf3['ActRet'])
    GaussianNB_fit5 = gnb.fit(X_train5, hf5['ActRet'])
    GaussianNB_fit10 = gnb.fit(X_train10, hf10['ActRet'])
    GaussianNB_fit15 = gnb.fit(X_train15, hf15['ActRet'])

    t3 = [tf3['Reading'], qf['RSI_3d'], yf['stoch_3d'], rf3['MACombo'], zf['CurrVal']]
    t5 = [tf5['Reading'], qf['RSI_5d'], yf['stoch_5d'], rf5['MACombo'], zf['CurrVal']]
    t10 = [tf10['Reading'], qf['RSI_10d'], yf['stoch_10d'], rf10['MACombo'], zf['CurrVal']]
    t15 = [tf15['Reading'], qf['RSI_15d'], yf['stoch_15d'], rf15['MACombo'], zf['CurrVal']]

    X_test3 = (pd.concat(t3, axis=1, keys=['Reading', 'RSI_3d', 'stoch_3d', 'MACombo', 'CurrVal'])).values
    X_test5 = (pd.concat(t5, axis=1, keys=['Reading', 'RSI_5d', 'stoch_5d', 'MACombo', 'CurrVal'])).values
    X_test10 = (pd.concat(t10, axis=1, keys=['Reading', 'RSI_10d', 'stoch_10d', 'MACombo', 'CurrVal'])).values
    X_test15 = (pd.concat(t15, axis=1, keys=['Reading', 'RSI_15d', 'stoch_15d', 'MACombo', 'CurrVal'])).values

    y_pred3 = GaussianNB_fit3.predict(X_test3)  # predict over the testing data
    y_pred5 = GaussianNB_fit5.predict(X_test5)
    y_pred10 = GaussianNB_fit10.predict(X_test10)
    y_pred15 = GaussianNB_fit15.predict(X_test15)

    print(classification_report(rf3['ActRet'].values, y_pred3, labels=[0, 1]))
    print(classification_report(rf5['ActRet'].values, y_pred5, labels=[0, 1]))
    print(classification_report(rf10['ActRet'].values, y_pred10, labels=[0, 1]))
    print(classification_report(rf15['ActRet'].values, y_pred15, labels=[0, 1]))

    print(confusion_matrix(rf3['ActRet'].values, y_pred3))
    print(confusion_matrix(rf3['ActRet'].values, y_pred5))
    print(confusion_matrix(rf3['ActRet'].values, y_pred10))
    print(confusion_matrix(rf3['ActRet'].values, y_pred15))

    # save model fitted with test data
    save_fit_3 = gnb.fit(X_test3, rf3['ActRet'])
    save_fit_5 = gnb.fit(X_test5, rf5['ActRet'])
    save_fit_10 = gnb.fit(X_test10, rf10['ActRet'])
    save_fit_15 = gnb.fit(X_test15, rf15['ActRet'])

    with open('nb_3_' + ticker +'.pkl', 'wb') as fid:
        pickle.dump(save_fit_3, fid)

    with open('nb_5_' + ticker + '.pkl', 'wb') as fid:
        pickle.dump(save_fit_5, fid)

    with open('nb_10_' + ticker + '.pkl', 'wb') as fid:
        pickle.dump(save_fit_10, fid)

    with open('nb_15_' + ticker + '.pkl', 'wb') as fid:
       pickle.dump(save_fit_15, fid)

def new_model_data(xtest3, xtest5, xtest10, xtest15, ticker):
    with open('model/nb_3_'+ticker+'.pkl', 'rb') as fid:
        gnb_loaded3 = pickle.load(fid)

    with open('model/nb_5_'+ticker+'.pkl', 'rb') as fid:
        gnb_loaded5 = pickle.load(fid)

    with open('model/nb_10_'+ticker+'.pkl', 'rb') as fid:
        gnb_loaded10 = pickle.load(fid)

    with open('model/nb_15_'+ticker+'.pkl', 'rb') as fid:
        gnb_loaded15 = pickle.load(fid)

    y_pred3 = gnb_loaded3.predict([xtest3])
    y_pred5 = gnb_loaded5.predict([xtest5])
    y_pred10 = gnb_loaded10.predict([xtest10])
    y_pred15 = gnb_loaded15.predict([xtest15])

    return y_pred3, y_pred5, y_pred10, y_pred15

# tickers = ['SPX', 'RUT', 'NDX', 'DJI']
# for ticker in tickers:
#
# train_test('DJI')
# rsi_scatter(ef3, ef5, ef10, ef15)

# xtest3, xtest5, xtest10, xtest15, date, price = new_date('SPX')
# pred3, pred5, pred10, pred15 = new_model_data(xtest3, xtest5, xtest10, xtest15)
#dj
# print(pred3, pred5, pred10, pred15)















































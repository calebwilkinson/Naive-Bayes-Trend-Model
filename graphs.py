import numpy as np
from matplotlib import pyplot as plt
cmap = plt.cm.inferno
import pandas as pd
from matplotlib import pyplot as plt
import SQL_Server_Access as sql

def testing_data():
    cursor = sql.Access_Server()
    cursor.execute("SELECT TOP(252) * FROM spx_20d_ma_value ORDER BY Date DESC")
    data_list = cursor.fetchall()
    two_std_returns(data_list, 'UP')

def training_data():
    cursor = sql.Access_Server()
    cursor.execute("SELECT * FROM spx_20d_ma_value WHERE Date < '2022-01-01'")
    data_list = cursor.fetchall()
    two_std_returns(data_list, 'UP')

# 2STD UP, SECTORS = SELL, CURRENCY = BUY
def two_std_returns(data_list, direction):
    std2_3d = []
    std2_5d = []
    std2_10d = []
    std2_15d = []
    for count, data in enumerate(data_list):
        up_cntr = 0

        for x in data_list[count:count+5]:
            if direction in x[4]:
                up_cntr +=1

        if up_cntr >= 3:
            cursor = sql.Access_Server()
            cursor.execute("SELECT Fwd_3d, Fwd_5d, Fwd_10d, Fwd_15d FROM SPX_Fwd_Returns WHERE Date = ?", data[0])
            returns = cursor.fetchall()
            std2_3d.append(returns[0][0])
            std2_5d.append(returns[0][1])
            std2_10d.append(returns[0][2])
            std2_15d.append(returns[0][3])

    df3 = pd.DataFrame(std2_3d, columns=['3d Return'])
    df5 = pd.DataFrame(std2_5d, columns=['5d Return'])
    df10 = pd.DataFrame(std2_10d, columns=['10d Return'])
    df15 = pd.DataFrame(std2_15d, columns=['15d Return'])
    print(df3.describe().transpose())

    plt.subplot(231)
    plt.hist(df3['3d Return'], alpha = 0.8, color = 'darkorange', edgecolor='black', bins = 20)
    plt.title('3 day Forward Returns',size=5)


    plt.subplot(232)
    plt.hist(df5['5d Return'], alpha = 0.8, color = 'darkorange', edgecolor='black', bins = 20)
    plt.title('5 day Forward Returns',size=5)

    plt.subplot(233)
    plt.hist(df10['10d Return'], alpha=0.8, color='darkorange', edgecolor='black', bins=20)
    plt.title('10 day Forward Returns', size=5)

    plt.subplot(234)
    plt.hist(df15['15d Return'], alpha=0.8, color='darkorange', edgecolor='black', bins=20)
    plt.title('15 day Forward Returns', size=5)

    plt.show()

# Histogram of Combination occurrences
def combo_hist(df3, df5, df10, df15):
    plt.subplot(231)
    plt.hist(df3['MA Combo'], color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=8)

    plt.subplot(232)
    plt.hist(df5['MA Combo'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=8)

    plt.subplot(233)
    plt.hist(df10['MA Combo'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=8)

    plt.subplot(234)
    plt.hist(df15['MA Combo'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=8)

    plt.show()

def rsi_scatter(period):
    data_list = np.array(sql.rsi_stoch_all(period))
    rsi = data_list[period:,0]
    stoch = data_list[period:,1]
    ret = data_list[period:,2]
    returns = np.where(ret>=0, 1, 0)

    im = plt.scatter(rsi, stoch, s=None, c=ret, marker=None, cmap=cmap, norm=None,
                     vmin=None, vmax=None, alpha=0.8, linewidths=0.3, edgecolors="black")
    plt.title('Past 1000 days of '+str(period)+' period RSI and Stochastics ')
    plt.xlabel('RSI')
    plt.ylabel('Stochastics')
    cbar = plt.colorbar(im, orientation='vertical')
    cbar.set_label("Returns", rotation=270, labelpad=20)

    # plt.subplots_adjust(left=0.0, bottom=0.0, right=2.0, top=1.2, wspace=0.2, hspace=0.2)

    plt.show()

def rsi_hist(df3, df5, df10, df15):
    plt.subplot(231)
    plt.hist(df3['RSI_15d'], color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=12)

    plt.subplot(232)
    plt.hist(df5['RSI_15d'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=12)

    plt.subplot(233)
    plt.hist(df10['RSI_15d'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=8)

    plt.subplot(234)
    plt.hist(df15['RSI_15d'], alpha=0.8, color='darkorange', edgecolor='black', bins=10)
    plt.title('Unique Combo Occurrences', size=12)

    plt.show()

# rsi_scatter(15)
# training_data()
def plot_corr(dataframe,size=10):                               # plots a graphical correlation matrix
    corr = dataframe.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    im = ax.matshow(corr,vmin = -1.0, vmax = 1.0,cmap=cmap)
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.colorbar(im, orientation = 'vertical')
    plt.title('3 day, 5 day, 10 day, 15 day Stochastics Correlation')

def stoch_matrix():
        my_data = sql.stoch_train_select('SPX')
        corr_matrix = np.corrcoef(my_data, rowvar = False)  # correlation matrix without the categorical value
        plot_corr(my_data,10)
        plt.show()# using our correlation matrix visualization function




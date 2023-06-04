import pandas as pd
from matplotlib import pyplot as plt
import SQL_Server_Access as sql

def list_of_returns(ticker):

    data = sql.select_between(ticker, '2018-01-01', '2022-05-31')
    ticker_ret = []

    for date in data:
        ticker_ret.append(date[1])

    return ticker_ret

def plot_corr(dataframe, size=14):  # plots a graphical correlation matrix
    corr = dataframe.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    im = ax.matshow(corr, vmin=-1.0, vmax=1.0)
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);
    plt.colorbar(im, orientation='vertical')
    plt.title('Correlation Matrix')


    # get rolling 5 day period of forward returns into dataframe

def value_testing(reading):
    cursor  = sql.Access_Server()
    cursor.execute("SELECT * FROM Value WHERE Date < '2022-01-01'")
    data_list = cursor.fetchall()

    ret_3d = []
    ret_5d = []
    ret_10d = []
    ret_15d = []
    for data in data_list:
        check_list = [data[4], data[5], data[8], data[9], data[12], data[13], data[20], data[21]]
        if all(val == reading for val in check_list):
            cursor.execute("SELECT Fwd_3d, Fwd_5d, Fwd_10d, Fwd_15d FROM SPX_Fwd_Returns WHERE Date = ?", data[0])
            returns = cursor.fetchall()
            ret_3d.append(returns[0][0])
            ret_5d.append(returns[0][1])
            ret_10d.append(returns[0][2])
            ret_15d.append(returns[0][3])

    df3 = pd.DataFrame(ret_3d, columns=['3d Return'])
    df5 = pd.DataFrame(ret_5d, columns=['5d Return'])
    df10 = pd.DataFrame(ret_10d, columns=['10d Return'])
    df15 = pd.DataFrame(ret_15d, columns=['15d Return'])

    return df3, df5, df10, df15

def scatter_plot(d1, d2):
    plt.subplot(121)
    im = plt.scatter(d1, d2, s=None, marker=None, cmap=map, norm=None,
                     vmin=None, vmax=None, alpha=0.8, linewidths=0.3, edgecolors="black")
    plt.title('Training Production vs. Brittleness and Porosity');
    plt.xlabel('Porosity (%)')
    plt.ylabel('Brittleness (%)')
    cbar = plt.colorbar(im, orientation='vertical')
    cbar.set_label("Production", rotation=270, labelpad=20)

   # plt.subplot(122)
   # im = plt.scatter(X_test["Por"], X_test["Brittle"], s=None, c=y_test['cprod'], marker=None, cmap=cmap, norm=None,
   #                  vmin=None, vmax=None, alpha=0.8, linewidths=0.3, edgecolors="black")
   # plt.title('Testing Production vs. Brittleness and Porosity');
   # plt.xlabel('Porosity (%)');
   # plt.ylabel('Brittleness (%)')
   # cbar = plt.colorbar(im, orientation='vertical')
   # cbar.set_label("Production", rotation=270, labelpad=20)
   #
   # plt.subplots_adjust(left=0.0, bottom=0.0, right=2.0, top=1.2, wspace=0.2, hspace=0.2)

    plt.show()






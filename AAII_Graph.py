import matplotlib.pyplot as plt
from matplotlib import ticker
from SQL_Server_Access import Access_Server

def AAII_Net_Positioning():
    # Access server and Select ALL the data from wanted columns
    cursor = Access_Server()
    cursor.execute('SELECT * FROM SPX')

    spx_x = []
    spx_y = []
    for row in cursor:
        spx_x.append(row[0])
        spx_y.append(row[1])

    cursor2 = Access_Server()
    cursor2.execute('SELECT Date, Net_Position_Weighted FROM Net_Positioning')
    net_position_x = []
    net_position_y = []
    for row in cursor2:
        net_position_x.append(row[0])
        # Change from decimal to percent
        net_position_y.append(row[1] * 100)

    fig, ax = plt.subplots()
    ax.twinx()

    # Get rid of scientific notation and set ticks
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.gca().yaxis.set_minor_formatter(ticker.NullFormatter())
    plt.yticks([650, 1000, 1500, 2000, 3000, 4000, 5000])

    # plot SPX
    plt.plot(spx_x, spx_y)

    # Plot net position data as a bar chart.
    ax.bar(net_position_x, net_position_y, width=10, color='r')
    plt.title('SPX and Net Speculative Positioning as a % of Open Interest')
    plt.show()

AAII_Net_Positioning()
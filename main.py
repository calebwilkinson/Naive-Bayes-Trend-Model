import model
import sql_tables as st

all_tickers = {'NDX':'^NDX',
               'RUT':'^RUT',
               'SPX':'^SPX',
               'DJI':'^DJI',
               'GOLD':'GC=F',
               'CRUDE_OIL':'CL=F',
               'DXY':'DX-Y.NYB',
               'EURUSD':'EURUSD=X',
               'USDJPY':'JPY=X',
               'N225':'^N225',
               'FTSE100':'^FTSE',
               'DAX':'^GDAXI',
               'AAPL':'AAPL',
               'GOOGL':'GOOGL',
               'AMZN':'AMZN',
               'NVDA':'NVDA',
               'BRK_B':'BRK-B',
               'MSFT':'MSFT',
               'UNH':'UNH',
               'XOM':'XOM',
               'JNJ':'JNJ',
               'TSLA':'TSLA',
               'JPM':'JPM',
               'XLK':'XLK',    # Technology  # Top Sector ETFs
               'XLV':'XLV',    # Health Care
               'XLF':'XLF',    # Financials
               'XLRE':'XLRE',  # Real Estate
               'XLE':'XLE',    # Energy
               'XLB':'XLB',    # Materials
               'XHB':'XHB',    # Consumer Discretionary
               'XAR':'XAR',    # Industrials
               'XLU':'XLU',    # Utilities
               'XLP':'XLP',    # Consumer Staples
               'XLC':'XLC',    # Telecommunication
               'PG':'PG',
               'V':'V',
               'LLY':'LLY',
               'MA':'MA',
               'HD':'HD',
               'MRK':'MRK',
               'CVX':'CVX',
               'ABBV':'ABBV',
               'PEP':'PEP',
               'AVGO':'AVGO',
               'KO':'KO',
               'COST':'COST',
               'META':'META',
               'EUR':'EUR=X',
               'GBP':'GBP=X',
               'CNY':'CNY=X',
               'CAD':'CAD=X',
               'CHF':'CHF=X'
            }

sector_tickers = {'XLK':28,
                  'XLV':14,
                  'XLF':12,
                  'XLRE':2,
                  'XLE':5,
                  'XLB':2,
                  'XHB':10,
                  'XAR':8,
                  'XLU':3,
                  'XLP':7,
                  'XLC':9} # Last updated April 28, 2023

top_25_tickers = {'AAPL':5,
                  'MSFT':4,
                  'AMZN':2.5,
                  'NVDA':2,
                  'GOOGL':3.5,
                  'BRK_B':2,
                  'META':2,
                  'UNH':1.5,
                  'XOM':1.5,
                  'JNJ':1.5,
                  'TSLA':1.5,
                  'JPM':1.5,
                  'PG':1.5,
                  'V':1,
                  'LLY':1,
                  'MA':1,
                  'HD':1,
                  'MRK':1,
                  'CVX':1,
                  'ABBV':1,
                  'PEP':1,
                  'AVGO':1,
                  'KO':1,
                  'COST':1} # Last updated May 2, 2023 # GOOG consolidated to 1

top_4_tickers = {'AAPL': 15,
                 'MSFT': 14 ,
                 'AMZN': 12 ,
                 'GOOGL': 13}

index_tickers = {'NDX':25,
                 'RUT':25,
                 'SPX':25,
                 'DJI':25,
                 'DAX':25,
                 'FTSE100':25,
                 'N225':25}

currency_tickers = {'EUR':15,
                    'GBP':15,
                    'CNY':15,
                    'CAD':15,
                    'CHF':15,
                    'DXY':15,
                    'USDJPY':15}

# Once a day (granted the US markets were open) run this function.
def update_all_data():
    st.update_tickers(all_tickers)
    st.update_value_tbl(sector_tickers, top_25_tickers, top_4_tickers, index_tickers, currency_tickers)
    st.update_ma_table('SPX')
    st.update_ma_table('NDX')
    st.update_ma_table('RUT')
    st.update_ma_table('DJI')

# model.query_user()

# update_all_data()

















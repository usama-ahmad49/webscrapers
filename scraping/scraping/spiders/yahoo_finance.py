from yahoo_fin import options
from pandas import DataFrame
import yahoo_fin.stock_info as si
import csv
import html5lib

csvHeader_dow=['ticker', 'EPS Est.','EPS Actual','Current Qtr.','Next Qtr.','Current Year','Next Year','Next 5 Years (per annum)','totalLiab','totalStockholderEquity','totalAssets',
           'retainedEarnings','goodWill','cash','totalCurrentLiabilities','shortLongTermDebt','propertyPlantEquipment','netTangibleAssets','longTermDebt','totalCashFromOperatingActivities','dividendsPaid',
           'capitalExpenditures','1y Target Est','52 Week Range','Beta (5Y Monthly)','EPS (TTM)','Earnings Date','Ex-Dividend Date',
           'Forward Dividend & Yield','Market Cap','PE Ratio (TTM)','Enterprise Value 3','Forward P/E 1']
csvHeader_nsdaq=['ticker', 'EPS Est.','EPS Actual','Current Qtr.','Next Qtr.','Current Year','Next Year','Next 5 Years (per annum)','totalLiab','totalStockholderEquity','totalAssets',
           'retainedEarnings','goodWill','cash','totalCurrentLiabilities','shortLongTermDebt','propertyPlantEquipment','netTangibleAssets','longTermDebt','totalCashFromOperatingActivities','dividendsPaid',
           'capitalExpenditures','1y Target Est','52 Week Range','Beta (5Y Monthly)','EPS (TTM)','Earnings Date','Ex-Dividend Date',
           'Forward Dividend & Yield','Market Cap','PE Ratio (TTM)','Enterprise Value 3','Forward P/E 1']
csvHeader_sp500=['ticker', 'EPS Est.','EPS Actual','Current Qtr.','Next Qtr.','Current Year','Next Year','Next 5 Years (per annum)','totalLiab','totalStockholderEquity','totalAssets',
           'retainedEarnings','goodWill','cash','totalCurrentLiabilities','shortLongTermDebt','propertyPlantEquipment','netTangibleAssets','longTermDebt','totalCashFromOperatingActivities','dividendsPaid',
           'capitalExpenditures','1y Target Est','52 Week Range','Beta (5Y Monthly)','EPS (TTM)','Earnings Date','Ex-Dividend Date',
           'Forward Dividend & Yield','Market Cap','PE Ratio (TTM)','Enterprise Value 3','Forward P/E 1']

csvfile1 = open('yahoo_finance(DOW).csv','w',newline='')
writer1 = csv.DictWriter(csvfile1, fieldnames=csvHeader_dow)
writer1.writeheader()
csvfile2 = open('yahoo_finance(NSDAQ).csv','w',newline='')
writer2 = csv.DictWriter(csvfile2, fieldnames=csvHeader_nsdaq)
writer2.writeheader()
csvfile3 = open('yahoo_finance(SP500).csv','w',newline='')
writer3 = csv.DictWriter(csvfile3, fieldnames=csvHeader_sp500)
writer3.writeheader()

tickers = si.tickers_dow()
for tiker in tickers:
    print('getting ticker: {}'.format(tiker))
    item = dict()
    item['ticker'] = tiker
    try:
        df = si.get_analysts_info(tiker)
    except:
        try:
            df = si.get_analysts_info(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))
    # df['Earnings Estimate'].to_csv(r'E:\Project\pricescraperlk\scraping\scraping\yahoo-fin\EPSEst.csv', index=False,header=True)
    try:
        item['Next 5 Years (per annum)'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next 5 Years (per annum)'] = ''
    try:
        item['Next Year'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next Year'] = ''
    try:
        item['Next Qtr.'] = df['Growth Estimates'].iloc[[1]].get(tiker)[1]
    except:
        item['Next Qtr.'] = ''
    try:
        item['Current Year'] = df['Growth Estimates'].iloc[[2]].get(tiker)[2]
    except:
        item['Current Year'] = ''
    try:
        item['Current Qtr.'] = df['Growth Estimates'].iloc[[0]].get(tiker)[0]
    except:
        item['Current Qtr.'] = ''
    try:
        item['EPS Est.'] = df['Earnings History'].iloc[0].tolist()[-1]
    except:
        item['EPS Est.'] = ''
    try:
        item['EPS Actual'] = df['Earnings History'].iloc[1].tolist()[-1]
    except:
        item['EPS Actual'] = ''
    try:
        df = si.get_balance_sheet(tiker)
    except:
        try:
            df = si.get_balance_sheet(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    try:
        item['totalLiab'] = df.loc['totalLiab'].tolist()[-1]
    except:
        item['totalLiab'] = ''
    try:
        item['totalStockholderEquity'] = df.loc['totalStockholderEquity'].tolist()[0]
    except:
        item['totalStockholderEquity'] = ''
    try:
        item['totalAssets'] = df.loc['totalAssets'].tolist()[0]
    except:
        item['totalAssets'] = ''
    try:
        item['retainedEarnings'] = df.loc['retainedEarnings'].tolist()[0]
    except:
        item['retainedEarnings'] = ''
    try:
        item['goodWill'] = df.loc['goodWill'].tolist()[0]
    except:
        item['goodWill'] = ''
    try:
        item['cash'] = df.loc['cash'].tolist()[0]
    except:
        item['cash'] = ''
    try:
        item['totalCurrentLiabilities'] = df.loc['totalCurrentLiabilities'].tolist()[0]
    except:
        item['totalCurrentLiabilities'] = ''
    try:
        item['shortLongTermDebt'] = df.loc['shortLongTermDebt'].tolist()[0]
    except:
        item['shortLongTermDebt'] = ''
    try:
        item['propertyPlantEquipment'] = df.loc['propertyPlantEquipment'].tolist()[0]
    except:
        item['propertyPlantEquipment'] = ''
    try:
        item['netTangibleAssets'] = df.loc['netTangibleAssets'].tolist()[0]
    except:
        item['netTangibleAssets'] = ''
    try:
        item['longTermDebt'] = df.loc['longTermDebt'].tolist()[0]
    except:
        item['longTermDebt'] = ''
    try:
        df = si.get_cash_flow(tiker)
    except:
        try:
            df = si.get_cash_flow(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    try:
        item['totalCashFromOperatingActivities'] = df.loc['totalCashFromOperatingActivities'].tolist()[0]
    except:
        item['totalCashFromOperatingActivities'] = ''
    try:
        item['dividendsPaid'] = df.loc['dividendsPaid'].tolist()[0]
    except:
        item['dividendsPaid'] = ''
    try:
        item['capitalExpenditures'] = df.loc['capitalExpenditures'].tolist()[0]
    except:
        item['capitalExpenditures'] = ''
    try:
        df = si.get_quote_table(tiker)
    except:
        try:
            df = si.get_quote_table(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))


    try:
        item['1y Target Est'] = df['1y Target Est']
    except:
        item['1y Target Est'] = ''
    try:
        item['52 Week Range'] = df['52 Week Range']
    except:
        item['52 Week Range'] = ''
    try:
        item['Beta (5Y Monthly)'] = df['Beta (5Y Monthly)']
    except:
        item['Beta (5Y Monthly)'] = ''
    try:
        item['EPS (TTM)'] = df['EPS (TTM)']
    except:
        item['EPS (TTM)'] = ''
    try:
        item['Earnings Date'] = df['Earnings Date']
    except:
        item['Earnings Date'] = ''
    try:
        item['Ex-Dividend Date'] = df['Ex-Dividend Date']
    except:
        item['Ex-Dividend Date'] = ''
    try:
        item['Forward Dividend & Yield'] = df['Forward Dividend & Yield']
    except:
        item['Forward Dividend & Yield'] = ''
    try:
        item['Market Cap'] = df['Market Cap']
    except:
        item['Market Cap'] = ''
    try:
        item['PE Ratio (TTM)'] = df['PE Ratio (TTM)']
    except:
        item['PE Ratio (TTM)'] = ''
    try:
        df = si.get_stats_valuation(tiker)
        try:
            item['Enterprise Value 3'] = df.loc[1].tolist()[1]
        except:
            item['Enterprise Value 3'] = ''
        try:
            item['Forward P/E 1'] = df.loc[3].tolist()[1]
        except:
            item['Forward P/E 1'] = ''
    except Exception as e:
        print('failed to load ticker: {}'.format(tiker))
        print('Exception: {}'.format(str(e)))


    writer1.writerow(item)
    csvfile1.flush()

tickers = si.tickers_nasdaq()
for tiker in tickers:
    print('getting ticker: {}'.format(tiker))
    item = dict()
    item['ticker'] = tiker
    try:
        df = si.get_analysts_info(tiker)
    except:
        try:
            df = si.get_analysts_info(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    # df['Earnings Estimate'].to_csv(r'E:\Project\pricescraperlk\scraping\scraping\yahoo-fin\EPSEst.csv', index=False,header=True)
    try:
        item['Next 5 Years (per annum)'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next 5 Years (per annum)'] = ''
    try:
        item['Next Year'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next Year'] = ''
    try:
        item['Next Qtr.'] = df['Growth Estimates'].iloc[[1]].get(tiker)[1]
    except:
        item['Next Qtr.'] = ''
    try:
        item['Current Year'] = df['Growth Estimates'].iloc[[2]].get(tiker)[2]
    except:
        item['Current Year'] = ''
    try:
        item['Current Qtr.'] = df['Growth Estimates'].iloc[[0]].get(tiker)[0]
    except:
        item['Current Qtr.'] = ''
    try:
        item['EPS Est.'] = df['Earnings History'].iloc[0].tolist()[-1]
    except:
        item['EPS Est.'] = ''
    try:
        item['EPS Actual'] = df['Earnings History'].iloc[1].tolist()[-1]
    except:
        item['EPS Actual'] = ''
    try:
        df = si.get_balance_sheet(tiker)
    except:
        try:
            df = si.get_balance_sheet(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))
    try:
        item['totalLiab'] = df.loc['totalLiab'].tolist()[-1]
    except:
        item['totalLiab'] = ''
    try:
        item['totalStockholderEquity'] = df.loc['totalStockholderEquity'].tolist()[0]
    except:
        item['totalStockholderEquity'] = ''
    try:
        item['totalAssets'] = df.loc['totalAssets'].tolist()[0]
    except:
        item['totalAssets'] = ''
    try:
        item['retainedEarnings'] = df.loc['retainedEarnings'].tolist()[0]
    except:
        item['retainedEarnings'] = ''
    try:
        item['goodWill'] = df.loc['goodWill'].tolist()[0]
    except:
        item['goodWill'] = ''
    try:
        item['cash'] = df.loc['cash'].tolist()[0]
    except:
        item['cash'] = ''
    try:
        item['totalCurrentLiabilities'] = df.loc['totalCurrentLiabilities'].tolist()[0]
    except:
        item['totalCurrentLiabilities'] = ''
    try:
        item['shortLongTermDebt'] = df.loc['shortLongTermDebt'].tolist()[0]
    except:
        item['shortLongTermDebt'] = ''
    try:
        item['propertyPlantEquipment'] = df.loc['propertyPlantEquipment'].tolist()[0]
    except:
        item['propertyPlantEquipment'] = ''
    try:
        item['netTangibleAssets'] = df.loc['netTangibleAssets'].tolist()[0]
    except:
        item['netTangibleAssets'] = ''
    try:
        item['longTermDebt'] = df.loc['longTermDebt'].tolist()[0]
    except:
        item['longTermDebt'] = ''
    try:
        df = si.get_cash_flow(tiker)
    except:
        try:
            df = si.get_cash_flow(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))
    try:
        item['totalCashFromOperatingActivities'] = df.loc['totalCashFromOperatingActivities'].tolist()[0]
    except:
        item['totalCashFromOperatingActivities'] = ''
    try:
        item['dividendsPaid'] = df.loc['dividendsPaid'].tolist()[0]
    except:
        item['dividendsPaid'] = ''
    try:
        item['capitalExpenditures'] = df.loc['capitalExpenditures'].tolist()[0]
    except:
        item['capitalExpenditures'] = ''
    try:
        df = si.get_quote_table(tiker)
    except:
        try:
            df = si.get_quote_table(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    try:
        item['1y Target Est'] = df['1y Target Est']
    except:
        item['1y Target Est'] = ''
    try:
        item['52 Week Range'] = df['52 Week Range']
    except:
        item['52 Week Range'] = ''
    try:
        item['Beta (5Y Monthly)'] = df['Beta (5Y Monthly)']
    except:
        item['Beta (5Y Monthly)'] = ''
    try:
        item['EPS (TTM)'] = df['EPS (TTM)']
    except:
        item['EPS (TTM)'] = ''
    try:
        item['Earnings Date'] = df['Earnings Date']
    except:
        item['Earnings Date'] = ''
    try:
        item['Ex-Dividend Date'] = df['Ex-Dividend Date']
    except:
        item['Ex-Dividend Date'] = ''
    try:
        item['Forward Dividend & Yield'] = df['Forward Dividend & Yield']
    except:
        item['Forward Dividend & Yield'] = ''
    try:
        item['Market Cap'] = df['Market Cap']
    except:
        item['Market Cap'] = ''
    try:
        item['PE Ratio (TTM)'] = df['PE Ratio (TTM)']
    except:
        item['PE Ratio (TTM)'] = ''
    try:
        df = si.get_stats_valuation(tiker)
        try:
            item['Enterprise Value 3'] = df.loc[1].tolist()[1]
        except:
            item['Enterprise Value 3'] = ''
        try:
            item['Forward P/E 1'] = df.loc[3].tolist()[1]
        except:
            item['Forward P/E 1'] = ''
    except Exception as e:
        print('failed to load ticker: {}'.format(tiker))
        print('Exception: {}'.format(str(e)))



    writer2.writerow(item)
    csvfile2.flush()

tickers = si.tickers_sp500()
for tiker in tickers:
    print('getting ticker: {}'.format(tiker))
    item = dict()
    item['ticker'] = tiker
    try:
        df = si.get_analysts_info(tiker)
    except:
        try:
            df = si.get_analysts_info(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    # df['Earnings Estimate'].to_csv(r'E:\Project\pricescraperlk\scraping\scraping\yahoo-fin\EPSEst.csv', index=False,header=True)
    try:
        item['Next 5 Years (per annum)'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next 5 Years (per annum)'] = ''
    try:
        item['Next Year'] = df['Growth Estimates'].iloc[[4]].get(tiker)[4]
    except:
        item['Next Year'] = ''
    try:
        item['Next Qtr.'] = df['Growth Estimates'].iloc[[1]].get(tiker)[1]
    except:
        item['Next Qtr.'] = ''
    try:
        item['Current Year'] = df['Growth Estimates'].iloc[[2]].get(tiker)[2]
    except:
        item['Current Year'] = ''
    try:
        item['Current Qtr.'] = df['Growth Estimates'].iloc[[0]].get(tiker)[0]
    except:
        item['Current Qtr.'] = ''
    try:
        item['EPS Est.'] = df['Earnings History'].iloc[0].tolist()[-1]
    except:
        item['EPS Est.'] = ''
    try:
        item['EPS Actual'] = df['Earnings History'].iloc[1].tolist()[-1]
    except:
        item['EPS Actual'] = ''
    try:
        df = si.get_balance_sheet(tiker)
    except:
        try:
            df = si.get_balance_sheet(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    try:
        item['totalLiab'] = df.loc['totalLiab'].tolist()[-1]
    except:
        item['totalLiab'] = ''
    try:
        item['totalStockholderEquity'] = df.loc['totalStockholderEquity'].tolist()[0]
    except:
        item['totalStockholderEquity'] = ''
    try:
        item['totalAssets'] = df.loc['totalAssets'].tolist()[0]
    except:
        item['totalAssets'] = ''
    try:
        item['retainedEarnings'] = df.loc['retainedEarnings'].tolist()[0]
    except:
        item['retainedEarnings'] = ''
    try:
        item['goodWill'] = df.loc['goodWill'].tolist()[0]
    except:
        item['goodWill'] = ''
    try:
        item['cash'] = df.loc['cash'].tolist()[0]
    except:
        item['cash'] = ''
    try:
        item['totalCurrentLiabilities'] = df.loc['totalCurrentLiabilities'].tolist()[0]
    except:
        item['totalCurrentLiabilities'] = ''
    try:
        item['shortLongTermDebt'] = df.loc['shortLongTermDebt'].tolist()[0]
    except:
        item['shortLongTermDebt'] = ''
    try:
        item['propertyPlantEquipment'] = df.loc['propertyPlantEquipment'].tolist()[0]
    except:
        item['propertyPlantEquipment'] = ''
    try:
        item['netTangibleAssets'] = df.loc['netTangibleAssets'].tolist()[0]
    except:
        item['netTangibleAssets'] = ''
    try:
        item['longTermDebt'] = df.loc['longTermDebt'].tolist()[0]
    except:
        item['longTermDebt'] = ''
    try:
        df = si.get_cash_flow(tiker)
    except:
        try:
            df = si.get_cash_flow(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))

    try:
        item['totalCashFromOperatingActivities'] = df.loc['totalCashFromOperatingActivities'].tolist()[0]
    except:
        item['totalCashFromOperatingActivities'] = ''
    try:
        item['dividendsPaid'] = df.loc['dividendsPaid'].tolist()[0]
    except:
        item['dividendsPaid'] = ''
    try:
        item['capitalExpenditures'] = df.loc['capitalExpenditures'].tolist()[0]
    except:
        item['capitalExpenditures'] = ''
    try:
        df = si.get_quote_table(tiker)
    except:
        try:
            df = si.get_quote_table(tiker)
        except Exception as e:
            print('failed to load ticker: {}'.format(tiker))
            print('Exception: {}'.format(str(e)))


    try:
        item['1y Target Est'] = df['1y Target Est']
    except:
        item['1y Target Est'] = ''
    try:
        item['52 Week Range'] = df['52 Week Range']
    except:
        item['52 Week Range'] = ''
    try:
        item['Beta (5Y Monthly)'] = df['Beta (5Y Monthly)']
    except:
        item['Beta (5Y Monthly)'] = ''
    try:
        item['EPS (TTM)'] = df['EPS (TTM)']
    except:
        item['EPS (TTM)'] = ''
    try:
        item['Earnings Date'] = df['Earnings Date']
    except:
        item['Earnings Date'] = ''
    try:
        item['Ex-Dividend Date'] = df['Ex-Dividend Date']
    except:
        item['Ex-Dividend Date'] = ''
    try:
        item['Forward Dividend & Yield'] = df['Forward Dividend & Yield']
    except:
        item['Forward Dividend & Yield'] = ''
    try:
        item['Market Cap'] = df['Market Cap']
    except:
        item['Market Cap'] = ''
    try:
        item['PE Ratio (TTM)'] = df['PE Ratio (TTM)']
    except:
        item['PE Ratio (TTM)'] = ''
    try:
        df = si.get_stats_valuation(tiker)
        try:
            item['Enterprise Value 3'] = df.loc[1].tolist()[1]
        except:
            item['Enterprise Value 3'] = ''
        try:
            item['Forward P/E 1'] = df.loc[3].tolist()[1]
        except:
            item['Forward P/E 1'] = ''
    except Exception as e:
        print('failed to load ticker: {}'.format(tiker))
        print('Exception: {}'.format(str(e)))

    writer3.writerow(item)
    csvfile3.flush()
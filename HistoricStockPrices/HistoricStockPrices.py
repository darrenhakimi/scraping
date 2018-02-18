import pandas_datareader.data as web
import pandas as pd
import datetime
import csv

with open('input.csv', 'r') as csv_file:
    df = pd.read_csv(csv_file)
    ticker_list = df['ticker']
    ticker_list.tolist()
    
    start = datetime.datetime.strptime(df['start_date'].tolist()[0], '%Y-%m-%d')
    end = datetime.datetime.strptime(df['end_date'].tolist()[0], '%Y-%m-%d')

start = datetime.datetime(2018, 2, 1)
end = datetime.datetime(2018, 2, 13)

itrdate = start
day = datetime.timedelta(days=1)
myoutput = []
ticker_date_range_list = ['ticker']

mydaterange = pd.bdate_range(start, end)
mydaterangelist = pd.Series(mydaterange.format()).tolist()

ticker_date_range_list.extend(mydaterangelist)
myoutput.append(ticker_date_range_list)

for ticker in ticker_list:
    scrape = web.DataReader(ticker, 'google', start, end)['Close']
    mylist = [ticker]

    mylist.extend(scrape.tolist())
    myoutput.append(mylist)

with open("output.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(myoutput)


import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import talib
import alpaca_trade_api as tradeapi

api = tradeapi.REST('PK3HK1FANI4LF632XXME','iITCsTwcC5xfwJWLHUsw1GcIAtuO6eLTypNOHffZ','https://paper-api.alpaca.markets')

barTimeframe = "1H" # 1Min, 5Min, 15Min, 1H, 1D
assetsToDownload = ["SPY","MSFT","AAPL","NFLX"]
startDate = "2017-01-01T00:00:00.000Z" # Start date for the market data in ISO8601 format

# Tracks position in list of symbols to download
iteratorPos = 0 
assetListLen = len(assetsToDownload)

while iteratorPos < assetListLen:
	symbol = assetsToDownload[iteratorPos]
	
	returned_data = api.get_bars(symbol,barTimeframe,start_dt=startDate).bars
	
	timeList = []
	openList = []
	highList = []
	lowList = []
	closeList = []
	volumeList = []

	# Reads, formats and stores the new bars
	for bar in returned_data:
		timeList.append(datetime.strptime(bar.time,'%Y-%m-%dT%H:%M:%SZ'))
		openList.append(bar.open)
		highList.append(bar.high)
		lowList.append(bar.low)
		closeList.append(bar.close)
		volumeList.append(bar.volume)
	
	# Processes all data into numpy arrays for use by talib
	timeList = np.array(timeList)
	openList = np.array(openList,dtype=np.float64)
	highList = np.array(highList,dtype=np.float64)
	lowList = np.array(lowList,dtype=np.float64)
	closeList = np.array(closeList,dtype=np.float64)
	volumeList = np.array(volumeList,dtype=np.float64)

	# Calculated trading indicators
	SMA20 = talib.SMA(closeList,20)
	SMA50 = talib.SMA(closeList,50)

	
	# Defines the plot for each trading symbol
	f, ax = plt.subplots()
	f.suptitle(symbol)
	
	# Plots market data and indicators
	ax.plot(timeList,closeList,label=symbol,color="black")
	ax.plot(timeList,SMA20,label="SMA20",color="green")
	ax.plot(timeList,SMA50,label="SMA50",color="red")
	
	# Fills the green region if SMA20 > SMA50 and red if SMA20 < SMA50
	ax.fill_between(timeList, SMA50, SMA20, where=SMA20 >= SMA50, facecolor='green', alpha=0.5, interpolate=True)
	ax.fill_between(timeList, SMA50, SMA20, where=SMA20 <= SMA50, facecolor='red', alpha=0.5, interpolate=True)
	
	# Adds the legend to the right of the chart
	ax.legend(loc='center left', bbox_to_anchor=(1.0,0.5))
	
	iteratorPos += 1

plt.show()
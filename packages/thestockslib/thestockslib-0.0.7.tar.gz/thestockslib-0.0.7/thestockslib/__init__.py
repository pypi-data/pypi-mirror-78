import os
import datetime
import requests
import yfinance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from PIL import Image
from fbprophet import Prophet
from yahoo_fin import stock_info as si
from alpha_vantage.timeseries import TimeSeries

import sys
if sys.version_info[0] < 3: from StringIO import StringIO
else: from io import StringIO

class ConsideredAverage(Enum):
	OPEN_CLOSE = 1
	HIGH_LOW = 2

class TheStock():
	ticker = None
	tickerobject = None
	dateformat = None
	consideredaverage = ConsideredAverage.OPEN_CLOSE
	historicaldata = None
	actionstoperiods = {}

	def __init__(self, t, df='%Y-%m-%d', ca=ConsideredAverage.OPEN_CLOSE):
		self.dateformat = df
		self.ticker = t
		self.tickerobject = yfinance.Ticker(self.ticker)
		self.consideredaverage = ca
		self.historicaldata = self.tickerobject.history(period="max").to_records()

	def addactiontoperiod(self, a, p): self.actionstoperiods[str(a)] = int(p)

	def convertdatetime(self, d): return pd.to_datetime(str(d)).strftime(self.dateformat)

	def getliveprice(self, round_decimals=2): return round(si.get_live_price(self.ticker), round_decimals)

	def gethistoricalprice(self, d, round_decimals=2):
		datepassed = False # used to manage weekends
		for h in self.historicaldata:
			if datepassed or self.convertdatetime(h[0]) == d:
				p = None
				# average between open and close
				if self.consideredaverage == ConsideredAverage.OPEN_CLOSE: p = (h[4] + h[1]) / 2
				# average between high and low
				if self.consideredaverage == ConsideredAverage.HIGH_LOW: p = (h[2] + h[3]) / 2
				# returning result
				if p is None: datepassed = True
				else: return round(p, round_decimals)
		return None

	def getyahooperformanceoutlook(self):
		baseurl = "https://finance.yahoo.com/quote/"+str(self.ticker)
		r = requests.get(baseurl)
		text = r.text.replace('>', '>\n')
		text = text.split('\n')
		res_html = []
		for el in text:
			if not "<svg" in el: continue
			if not "Va(m)! pill" in el: continue
			res_html.append(el)
		res = []
		for el in res_html:
			if "#ff4d52" in el: res.append('down')
			if "#1ac567" in el: res.append('up')
			if "#464e56" in el: res.append('neutral')
		return res

	def getrevolutsymbols():
		REVOLUT_URL = 'https://raw.githubusercontent.com/nmapx/revolut-stocks-list/master/LIST.md'
		r = []
		req = requests.get(REVOLUT_URL)
		shouldconsider = False
		for l in req.text.split('\n'):
			if not shouldconsider and '---' in l:
				shouldconsider = True
				continue
			if not shouldconsider: continue
			try:
				els = l.split('|')
				ticker = els[1].strip()
				details = els[2].strip()
				#print(ticker+' -> '+details)
				r.append(ticker)
			except: pass
		return r

	def simulatepurchases(self, s):
		purchases = []
		data = self.tickerobject.recommendations.to_records()
		for d in data:
			if d[1] != s: continue
			referringdate = self.convertdatetime(d[0])
			if not d[2].lower() in self.actionstoperiods: continue
			p = self.gethistoricalprice(referringdate)
			purchases.append({'ticker':self.ticker, 'purchase_date':self.convertdatetime(d[0]), 'suggester':d[1], 'action':d[2], 'purchase_price':p})
		return purchases

	def simulatesells(self, p):
		for pp in p:
			purchasedate = datetime.datetime.strptime(pp.get('purchase_date'), self.dateformat)
			purchaseprice = pp.get('purchase_price')
			selldate = purchasedate + datetime.timedelta(days=self.actionstoperiods[pp.get('action').lower()])
			sellprice = self.gethistoricalprice(self.convertdatetime(selldate))
			pp['kept_days'] = self.actionstoperiods['buy']
			pp['sell_date'] = selldate.strftime(self.dateformat)
			pp['sell_price'] = sellprice
			profit = None
			try: profit = sellprice - purchaseprice
			except: pass
			pp['profit_per_stock'] = profit
		return p

	def getsuggestionreliabilitydata(self, suggester, suggestion, transactionprice=0.0):
		hist = self.tickerobject.history(period="max").to_records()
		purchases = self.simulatepurchases(suggester)
		print(">>> Simulated "+str(len(purchases))+" purchases")
		purchases = self.simulatesells(purchases)
		# getting recommendations list by suggester
		recommendations = None
		for p in purchases:
			if p.get('suggester') != suggester: continue
			if recommendations is None: recommendations = {'right':[], 'wrong':[]}
			if p.get('profit_per_stock') is None: continue
			r = 'wrong' if p.get('profit_per_stock') <= transactionprice else 'right'
			recommendations[r].append(p)
		# checking if some recommendations are found
		if recommendations is None: return None
		# computing reccomendations of the suggester
		right = len(recommendations.get('right'))
		wrong = len(recommendations.get('wrong'))
		p = 0
		if right+wrong > 0: p = round(float(right)/float(right+wrong), 2)
		suggester_data = {'suggester':suggester, 'numbers': {'right':right, 'wrong':wrong, 'reliability':p}, 'details':recommendations}
		# other
		return suggester_data

	def getsuggestionreliability(self, suggester, suggestion, transactionprice=0.0):
		reliability_obj = self.getsuggestionreliability(suggester, suggestion, transactionprice)
		computedtransactions = int(reliability_obj.get('numbers').get('right')) + int(reliability_obj.get('numbers').get('wrong'))
		return reliability_obj.get('numbers').get('reliability')

	def combineimages(l, vertical=False, outputname_pre=''):
		images = [Image.open(x) for x in l]
		widths, heights = zip(*(i.size for i in images))

		final_width = sum(widths)
		final_height = max(heights)
		if vertical:
			final_width = max(widths)
			final_height = sum(heights)

		new_im = Image.new('RGB', (final_width, final_height), (255, 255, 255))

		offset = 0
		for im in images:
			position = (offset, 0)
			if vertical: position = (0, offset)
			new_im.paste(im, position)
			i = 0
			if vertical: i = 1
			offset += im.size[i]

		new_im.save(outputname_pre+'output.png')

	def removeimages(outputname_pre=''):
		l = ['fig1.png', 'fig2.png', 'fig3.png', 'tmp.png', 'output.png']
		for i in l:
			try: os.remove(outputname_pre+i)
			except: pass

	def generategraphs(self, fcast_time, apikey, outputname_pre=''):
		ts = TimeSeries(key=apikey, output_format='pandas')
		stockdata, meta_data = ts.get_daily(symbol=self.ticker, outputsize='full')
		stockdata.head()
		# rename
		stockdata.rename(columns={'4. close': 'y', 'date': 'ds'},inplace=True)
		stockdata.index.name = 'ds'
		# ...
		stock = stockdata['y'].to_csv()
		s = {'ds':[], 'y':[]}
		for x in stock.split('\n'):
			try:
				ds = pd.to_datetime(x.split(',')[0])
				y = float(x.split(',')[1])
				s.get('ds').append(ds)
				s.get('y').append(y)
			except: pass
		# ...
		header = 'ds,y\n' # on mac
		data = StringIO(stock)
		# ...
		ss = pd.read_csv(data, sep=",")
		# ...
		try: ss['ds'] = pd.to_datetime(ss['ds'])
		except:
			data = StringIO(header+stock)
			ss = pd.read_csv(data, sep=",")
			ss['ds'] = pd.to_datetime(ss['ds'])
		ss['y']=ss['y'].astype(float)
		# ...
		df_prophet = Prophet(changepoint_prior_scale=0.15, daily_seasonality=True)
		df_prophet.fit(ss)
		# ...
		df_forecast = df_prophet.make_future_dataframe(periods=fcast_time, freq='D')
		#df_forecast.tail(10)
		# ...
		# Do forecasting
		df_forecast = df_prophet.predict(df_forecast)
		# ...
		#df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
		#Do the plot
		fig1 = df_prophet.plot(df_forecast, xlabel='Date', ylabel=self.ticker+' Price')
		fig1.gca().set_title(self.ticker+' prediction (all history)', size=20)
		fig1.subplots_adjust(top=0.95)
		fig1.savefig(outputname_pre+'fig1.png')
		#Do the plot
		fig2 = df_prophet.plot(df_forecast, xlabel='Date', ylabel=self.ticker+' Price')
		fig2.gca().set_xlim([df_forecast['ds'][(len(df_forecast)-1)-10*fcast_time], df_forecast['ds'][len(df_forecast)-1]])
		fig2.gca().set_title(self.ticker+' prediction (recent)', size=20)
		fig2.subplots_adjust(top=0.95)
		fig2.savefig(outputname_pre+'fig2.png')
		#Do the plot
		fig3 = df_prophet.plot_components(df_forecast)
		fig3.subplots_adjust(top=0.95)
		fig3.suptitle(self.ticker+' trend', size=20)
		#fig3.set_title(self.ticker)
		fig3.savefig(outputname_pre+'fig3.png')
		TheStock.combineimages([outputname_pre+'fig1.png', outputname_pre+'fig2.png'], True, outputname_pre=outputname_pre+'tmp')
		TheStock.combineimages([outputname_pre+'tmp'+'output.png', outputname_pre+'fig3.png'], outputname_pre=outputname_pre)
		# ...
		#plt.show()

	def getyahoorecommendationstring(r):
		if int(float(r)) < 1: return str(r)
		if int(float(r)) > 5: return str(r)
		indexes = [1, 2, 3, 4, 5]
		values = ['Strong buy', 'Buy', 'Hold', 'Under-perform', 'Sell']
		if float(r) % 1 == 0 and int(float(r)) in indexes: return str(r)+' ('+str(values[int(float(r))-1])+'('+str(indexes[int(float(r))-1])+'))'
		a = str(values[int(float(r))-1])+'('+str(indexes[int(float(r))-1])+')'
		b = str(values[int(float(r))])+'('+str(indexes[int(float(r))])+')'
		return str(r)+' (between '+a+' and '+b+')'

	def getyahoorecommendation(self):
		lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
		rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
			'modules=upgradeDowngradeHistory,recommendationTrend,' \
			'financialData,earningsHistory,earningsTrend,industryTrend&' \
			'corsDomain=finance.yahoo.com'

		url =  lhs_url + self.ticker + rhs_url
		r = requests.get(url)
		if not r.ok: recommendation = 6
		try:
			result = r.json()['quoteSummary']['result'][0]
			recommendation = result['financialData']['recommendationMean']['fmt']
		except: recommendation = 6
		current_price = float(result['financialData']['currentPrice']['raw'])
		recommendation = TheStock.getyahoorecommendationstring(recommendation)
		return {'recommendation': str(recommendation), 'current_price':str(current_price)}

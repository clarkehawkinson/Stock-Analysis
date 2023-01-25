import yfinance as yf
import numpy as np

threeMonth = yf.Ticker('^irx')
riskFreeReturn = (threeMonth.info['previousClose']/100)

stock = yf.Ticker("c")
# print(stock.info)
dividends = np.array(stock.dividends)
y0_dividends = dividends[-1]*4
y1_dividends = dividends[-5]*4
y2_dividends = dividends[-9]*4
y3_dividends = dividends[-13]*4
divHist=np.array([(y0_dividends, y1_dividends, y2_dividends, y3_dividends)])

# divvYoY is simple dividend growth  .051 = 5.1%
divYoY = (divHist[(0,0)]-divHist[(0,1)])/divHist[(0,1)]+(divHist[(0,1)]-divHist[(0,2)])/divHist[(0,2)]+(divHist[(0,3)]-divHist[(0,2)])/divHist[(0,3)]

earn = np.array(stock.earnings_trend)
ttm_eps = stock.info["trailingEps"]
fwd_eps = stock.info["forwardEps"]
beta = stock.info['beta']
sharesOutstanding = stock.info['sharesOutstanding']
past5yearEarn = np.array(earn[5,2])
next5yearEarn = np.array(earn[4,2])
average10Earn = (past5yearEarn+next5yearEarn)/2
# print(pd.DataFrame(earn))
# print(stock.info)
FcF = stock.info['freeCashflow']

print("Current Price       $",stock.info['regularMarketPrice'])
print("Current Annual Div. $",y0_dividends)
print("Dividend YoY Growth ",round(divYoY*100,2),"%")
print("Payout Ratio","       ",round(stock.info['payoutRatio']*100,2),"%")
print("Profit Margins","     ", round(stock.info['profitMargins']*100,2),"%")
print("Operating Margins","  ", round(stock.info['operatingMargins']*100,2),"%")
print("Dividend Yield","     ", round(stock.info['dividendYield']*100,2),"%")
print("Price to Book","      ", round(stock.info['priceToBook'],2))

# DCF projection on past 5 year growth and next 5 year estimates.
if(average10Earn>0):    
    if(FcF!="None"):
        print("YASSSSS")
        projectedFreeCash = np.zeros((10))
        projectedFreeCash[0] = FcF
        i = 1
        while i <10:
            j = i-1
            projectedFreeCash[i] = projectedFreeCash[j]*(1+average10Earn)
            i+=1
        freeCashMultiple = stock.info['marketCap']/FcF
        terminalCash = np.array([freeCashMultiple*projectedFreeCash[-1]])
        projectedFreeCash = np.append(projectedFreeCash, terminalCash)
        discountValue = np.zeros(11)
        i = 0
        while i <11:
            discountValue[i] = projectedFreeCash[i]/(1.15**i)
            i+=1
        print("% Market Cap/DCF    ", 100*(round((stock.info['marketCap']/np.sum(discountValue))-1,4)),"%")
    else:
        print("no cash")
else:
    print("no pos earn")

# Graham Number

# grahamNumber = sqrt(22.5*ttm_eps*)

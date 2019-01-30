
import json
import random
import twstock
from datetime import datetime
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(force=True)

    res = makeWebhookResult(req)

    return make_response(jsonify(res))


def makeWebhookResult(req):

    if req.get("queryResult").get("action") != "askStockInfo":
        return {}

    result = req.get("queryResult")
    parameters = result.get("parameters")
    zone = parameters.get("StockCode")
    code = zone.split(" ")[0]
    speech = "noData"

    if parameters.get("StockCode") == "":
        speech = "請提正確供個股代碼或名稱"
    elif code not in twstock.twse:
        speech = "抱歉，查無此股票哦"
    elif parameters.get("QueryWay")=="realtime":
        #RealTime data
        stock = twstock.realtime.get(code)

        if stock['success'] == True:
            speech =  zone + "相關資訊如下 : "+"\n收盤價:"+stock['realtime']['latest_trade_price']+"\n開盤價:"+stock['realtime']['open']+"\n最高價:"+stock['realtime']['high']+"\n最低價:"+stock['realtime']['low']
        else:
            speech = "暫時查無資料，請稍後重新查詢"

    else:
        #History data
        stock = twstock.Stock(code)
        if parameters.get("date")=="":
            dateArr = stock.date
            priceArr = stock.price
            openArr = stock.open
            lowArr = stock.low
            highArr = stock.high

            day = -1
            if parameters.get("Time") =="lastDay":
                day = datetime.today().day-1

            if day != -1:

                speech =  zone + "昨日"+dateArr[30].strftime("%Y-%m-%d")+"價格如下 : "
                speech += "\n收盤價:"+str(priceArr[30])+"\n開盤價:"+str(openArr[30])+"\n最高價:"+str(highArr[30])+"\n最低價:"+str(lowArr[30])
            else:

                speech =  zone + "近31日價格如下 : "
                for i in range(len(stock.price)):
                    speech += "\n"+dateArr[i].strftime("%Y-%m-%d")+"\n收盤價:"+str(priceArr[i])+"\n開盤價:"+str(openArr[i])+"\n最高價:"+str(highArr[i])+"\n最低價:"+str(lowArr[i])
                        
        else:
            d = datetime.strptime(parameters.get("date"),"%Y-%m-%dT%H:%M:%S%z")

            if parameters.get("Time") =="thisYear":
                year = datetime.today().year
            elif parameters.get("Time") =="lastYear" or d.replace(tzinfo=None) > datetime.now():
                year = datetime.today().year-1
            else:
                year = d.year

            if parameters.get("Time") =="thisMonth":
                month = datetime.today().month
            elif parameters.get("Time") =="lastMonth":
                month = datetime.today().month-1
            else:
                month = d.month

            day = -1
            if parameters.get("Time") =="lastDay":
                day = datetime.today().day-1
            elif d.day != 1:
                day = d.day

            stockf = stock.fetch(year,month)

            if day != -1:
                findDate = False
                for i in stockf:
                    if i[0].day == day:
                        findDate = True
                        speech =  zone +" 於"+i[0].strftime("%Y-%m-%d")+"價格如下 : "
                        speech += "\n收盤價:"+str(i[6])+"\n開盤價:"+str(i[3])+"\n最高價:"+str(i[4])+"\n最低價:"+str(i[5])

                if not findDate :
                    speech = d.strftime("%Y-%m-%d")+"無資料"
            else:
                speech =  zone + "自{0}年{1}月起31日內價格如下 : "
                speech = speech.format(year,month)
                for i in stockf:
                    speech += "\n"+i[0].strftime("%Y-%m-%d")+"\n收盤價:"+str(i[6])+"\n開盤價:"+str(i[3])+"\n最高價:"+str(i[4])+"\n最低價:"+str(i[5])
    
                
    return{'fulfillmentText': speech}
    
if __name__ == '__main__':
    PORT = 8080

    app.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
#coding:utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
from db import MongoManager
import datetime, time



def send_all_data():
    if str(datetime.datetime.now().hour) == "09" and str(datetime.datetime.now().minute) == "30":
        return True
    elif str(datetime.datetime.now().hour) == "12" and str(datetime.datetime.now().minute) == "00":
        return True
    elif str(datetime.datetime.now().hour) == "18" and str(datetime.datetime.now().minute) == "30":
        return True
    else:
        return False






send_or_not = send_all_data()
btc_cost=3409
ltc_cost=3353
db=MongoManager()
def str_to_int(price):
    return int(price.strip().strip('NT$').replace(',', ''))

line_bot_api = LineBotApi('gGUGkb70kvemgvz/uvecLc5/F1ki5U6MzT5KGwe+ajIJfwAuQJCGRzQFKdLAEnIsTrC0vd/bnRjtXj9y50Au36GlsL24NAJJIuIB7NDW/1xCjQyUzz1Pg0wWORfnC/bZ8O/rddXaAOMJl8362znLCgdB04t89/1O/w1cDnyilFU=')
info = {"name": "", "prev_price":"","price":"","status":"","dollars":"","rate":"","income":""}
wd = webdriver.Chrome("/Users/kkbox/downloads/Chromedriver")
url = 'https://www.maicoin.com/zh-TW'

wd.get(url)

html_page = wd.page_source
soup = BeautifulSoup(html_page, "html.parser")
span = soup.find("span", id="latest_btc_price")
span2 = soup.find("span", id="latest_ltc_price")
latest_btc_price = str_to_int(span.text.replace('\n',''))
latest_ltc_price = str_to_int(span2.text.replace('\n',''))
wd.quit()


btc_info = {"name": "BTC", "price": latest_btc_price}
ltc_info = {"name": "LTC", "price": latest_ltc_price}


db_btc_price = int(db.BTC_existed(btc_info))
db_ltc_price = int(db.BTC_existed(ltc_info))
def send(text):
    line_bot_api.push_message('U33b1c8b7537763d4426fe8364e3e76c8', TextSendMessage(text=str(text)))

def caculate(data):


    if data['name'] == "BTC" :
        info['name'] = data['name']
        info['price'] = data['price']
        info['prev_price']= db_btc_price
        info['income'] = round((latest_btc_price * 0.01) - btc_cost, 2)
        if latest_btc_price - db_btc_price >= 0:
            info['status'] = "rise"
            info['dollars'] = latest_btc_price-db_btc_price
            info['rate'] = round(float(latest_btc_price-db_btc_price)/float(db_btc_price),6)
        else:
            info['status'] = "fall"
            info['dollars'] = db_btc_price-latest_btc_price
            info['rate'] = round(float(db_btc_price-latest_btc_price)/float(db_btc_price),6)

            text = "name :" + `info['name']` + '\n' + "prev_price :" + `info['prev_price']` +'\n' + "price :" + `info['price']` + '\n' + "status :" + `info[
                'status']` + '\n' + "dollars :" + `info['dollars']` + '\n' + "rate :" + `info[
                'rate']` + '\n' + "income :" + `info['income']`
            warning(text, info['income'] ,info['rate'])




    else:
        info['name'] = data['name']
        info['price'] = data['price']
        info['prev_price'] = db_ltc_price
        info['income'] = round(latest_ltc_price - ltc_cost, 2)
        if latest_ltc_price - db_ltc_price >= 0:
            info['status'] = "rise"
            info['dollars'] =latest_ltc_price - db_ltc_price
            info['rate'] = round(float(latest_ltc_price - db_ltc_price) / float(db_ltc_price), 6)
        else:
            info['status'] = "fall"
            info['dollars'] =db_ltc_price - latest_ltc_price
            info['rate'] = round(float(db_ltc_price - latest_ltc_price) / float(db_ltc_price), 6)

    text = "name :" + `info['name']` + '\n' + "prev_price :" + `info['prev_price']` + '\n' + "price :" + `info[
        'price']` + '\n' + "status :" + `info[
        'status']` + '\n' + "dollars :" + `info['dollars']` + '\n' + "rate :" + `info[
        'rate']` + '\n' + "income :" + `info['income']`
    if send_or_not:
        send(text)

def warning(text,income,rate):
    if int(income) < 1200 :
        warning = "income < 1200 ！!" + text
        send(warning)
    elif float(rate) > 0.03:
        warning = "Descent Rate > 0.03 ！!" + text
        send(warning)



caculate(btc_info)
caculate(ltc_info)


db.update_score(btc_info)
db.update_score(ltc_info)





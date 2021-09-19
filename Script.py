from win10toast import ToastNotifier
from pygame import mixer
import schedule
import requests
import json

URL = "https://api.coindesk.com/v1/bpi/currentprice/{}.json"
MESSAGE = "Bitcoin Price Decreased"
CURRENT_PRICE = 0.0
CURRENCY = "INR"
TOASTER = ToastNotifier()

def get_current_price():
    response = requests.get(URL.format(CURRENCY))
    res = json.loads(response.text)
    rate = float(res["bpi"][CURRENCY]["rate_float"])
    return round(rate,2)

def show_notification(toast_title, toast_message, toast_duration=10):
    TOASTER.show_toast(
        title=toast_title,
        msg=toast_message,
        duration=toast_duration,
        icon_path="bitcoin.ico"
    )

def play_sound():
    mixer.init()
    mixer.music.load('Gilfoyle.mp3')
    mixer.music.play()

def check_current_price():
    rate = get_current_price()
    global CURRENT_PRICE
    if rate < CURRENT_PRICE:
        play_sound()
        msg = "Current Price is: ₹{}".format(rate)
        show_notification(MESSAGE,msg)
        CURRENT_PRICE = rate

CURRENT_PRICE = get_current_price()
schedule.every(1).minute.do(check_current_price)
while True:
    schedule.run_pending()

#!/usr/bin/env python
import datetime
import pytz
import sys
import time
import traceback
import json

from googlefinance import getQuotes
from nimbus import Nimbus
from yahoo_finance import Share

# Globals
NIMBUS = Nimbus("config.cfg")


def trading_hours():
    start = datetime.time(9, 30, 0)
    end = datetime.time(16, 1, 0)
    eastern = pytz.timezone('US/Eastern')
    return start <= datetime.datetime.now(eastern).time() <= end


def percentage(part, whole):
    change = 0
    if part < whole:
        return 0
    elif part > whole:
        change = part - whole
    percent = 100 * float(change)/float(whole)
    return percent


def update_stock(dial, stock):
    stk = Share(stock)
    prev_close_price = float(stk.get_prev_close())
    stk_data = json.loads(json.dumps(getQuotes(stock), indent=2))[0]
    stk_price = float(stk_data['LastTradePrice'])
    NIMBUS.set_dial_value(dial, percentage(stk_price, prev_close_price),
                          "%s:%.2f" % (stock[:2], stk_price))


def handler(event, context):
    if trading_hours():
        update_stock(0, 'OAS')
        update_stock(1, 'UGAZ')
    else:
        print "After hours"


if __name__ == "__main__":
    while 1:
        try:
            ret = handler(0, 0)
        except KeyboardInterrupt:
            ret = 0
            break
        except:
            traceback.print_exc(file=sys.stdout)
            continue

    sys.exit(ret)

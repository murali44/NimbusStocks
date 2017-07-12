#!/usr/bin/env python
import sys
import traceback

from googlefinance import Stock
from nimbus import Nimbus

# Globals
NIMBUS = Nimbus("config.cfg")

def update_stock(dial, stock):
    stk = Stock(stock)
    price = stk.price
    percent = stk.percentagechange
    NIMBUS.set_dial_value(dial, int(float(percent)), "%s:%.2f" % (stock[:2], float(price)))
    return price

def handler(event, context):
    oas = update_stock(0, 'OAS')
    ugaz = update_stock(1, 'UGAZ')

    # Update S&P500 Index
    sp500 = Stock('.INX')
    percent_change = sp500.percentagechange
    if percent_change > 0:
        percent = 25
    elif percent_change < 0:
        percent = 75
    NIMBUS.set_dial_value(2, int(float(percent)), "%s:%.2f" % ('S&P', float(percent_change)))

    # Show portfolio total.
    total = (float(oas) * 1401) + (float(ugaz) * 36) + 21 #cash
    NIMBUS.set_dial_value(3, 1, "%s" % (total))


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

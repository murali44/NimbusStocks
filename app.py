#!/usr/bin/env python
import sys
import traceback
import os
import json
import datetime
import plaid
import calendar
import time

from googlefinance import Stock
from nimbus import Nimbus

# Globals
NIMBUS = Nimbus("config.cfg")

def daily_spending():
    PLAID_CLIENT_ID = os.environ['PLAID_CLIENT_ID']
    PLAID_SECRET = os.environ['PLAID_SECRET']
    PLAID_PUBLIC_KEY = os.environ['PLAID_PUBLIC_KEY']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    PLAID_ENV = os.environ['PLAID_ENV']
    BUDGET = 850


    client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                    public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

    public_token = None

    today = datetime.datetime.now()
    start_date = "{:%Y-%m-%d}".format(today.replace(day=1))
    end_date = "{:%Y-%m-%d}".format(today)

    try:
        response = client.Transactions.get(ACCESS_TOKEN, start_date, end_date)
        transactions = response['transactions']
        print "*****All Transactions*************"
        print transactions
        print "**********************************"

        # the transactions in the response are paginated, so make multiple calls while increasing the offset to
        # retrieve all transactions
        while len(transactions) < response['total_transactions']:
            offset = len(transactions)
            response = client.Transactions.get(ACCESS_TOKEN, start_date, end_date, offset)
            transactions.extend(response['transactions'])
    except plaid.errors.PlaidError as e:
        print jsonify({'error': {'error_code': e.code, 'error_message': str(e)}})

    amount = 0
    for i in range(len(transactions)):
        if('Payment' not in transactions[i]['category']):
            amount = amount + transactions[i]['amount']

    days = calendar.monthrange(today.year,today.month)[1]
    remainging_days = days - today.day + 1

    daily_budget = (BUDGET - amount)/remainging_days
    bugget_percent = amount / (BUDGET/100)
    print "amount: %s" % amount
    print "remainging_days: %s" % remainging_days
    print "daily_budget: %s:" % daily_budget
    print "bugget_percent: %s" % bugget_percent
    NIMBUS.set_dial_value(0, int(bugget_percent), "%s" % (daily_budget))

def update_stock(dial, stock):
    stk = Stock(stock)
    price = stk.price
    percent = stk.percentagechange
    # NIMBUS.set_dial_value(dial, int(float(percent)), "%s:%.2f" % (stock[:2], float(price)))
    return price

def handler(event, context):
    # Dial 0
    daily_spending()

    # Dial 1; Update S&P500 Index
    sp500 = Stock('.INX')
    percent_change = sp500.percentagechange
    NIMBUS.set_dial_value(1, 0, "%s:%.2f" % ('S&P', float(percent_change)))

    # Dial 2
    NIMBUS.set_dial_value(2, 1, "-")

    # Dial 3; Show portfolio total.
    oas = update_stock(0, 'OAS')
    ugaz = update_stock(1, 'UGAZ')
    total = (float(oas) * 1401) + (float(ugaz) * 36) + 21 #cash
    NIMBUS.set_dial_value(3, 1, "%s" % (total))

    


if __name__ == "__main__":
    while 1:
        try:
            ret = handler(0, 0)
            time.sleep(3)
        except KeyboardInterrupt:
            ret = 0
            break
        except:
            traceback.print_exc(file=sys.stdout)
            continue

    sys.exit(ret)

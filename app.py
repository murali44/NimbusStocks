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
LOG_LEVEL = os.environ.get('LOG_LEVEL')


def daily_budget():
    PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
    PLAID_SECRET = os.environ.get('PLAID_SECRET')
    PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    PLAID_ENV = os.environ.get('PLAID_ENV')
    BUDGET = 850


    client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                    public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

    today = datetime.datetime.now()
    start_date = "{:%Y-%m-%d}".format(today.replace(day=1))
    end_date = "{:%Y-%m-%d}".format(today)

    try:
        response = client.Transactions.get(ACCESS_TOKEN, start_date, end_date)
        transactions = response['transactions']

        # the transactions in the response are paginated, so make multiple calls while increasing the offset to
        # retrieve all transactions
        while len(transactions) < response['total_transactions']:
            offset = len(transactions)
            response = client.Transactions.get(ACCESS_TOKEN, start_date, end_date, offset)
            transactions.extend(response['transactions'])
    except plaid.errors.PlaidError as e:
        print "error_code:" % e.code
        print "error_message:" % str(e)
        NIMBUS.set_dial_value(0, 0,"error")
        return

    amount = 0
    for i in range(len(transactions)):
        if((transactions[i]['category'] == None) or ('Payment' not in transactions[i]['category'])):
            amount = amount + transactions[i]['amount']
            log("%s: %s" % (transactions[i]['name'], transactions[i]['amount']))

    days = calendar.monthrange(today.year,today.month)[1]
    remainging_days = days - today.day + 1

    budget = (BUDGET - amount)/remainging_days
    bugget_percent = amount / (BUDGET/100)
    log("amount: %s" % amount)
    log("remainging_days: %s" % remainging_days)
    log("budget: %s" % budget)
    log("bugget_percent: %s" % bugget_percent)
    NIMBUS.set_dial_value(0, int(bugget_percent), "%.2f" % (budget))
    # Alexa skill response
    alexa_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': str(int(budget)) + ' dollars.',
            },
            "card": {
                "type": "Simple",
                "title": "Daily Budget for " + datetime.date.today().strftime("%B %d, %Y"),
                "content": str(int(budget)) + ' dollars.'
            }
        }
    }
    return alexa_response


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    log("intent: %s" % intent)
    log("intent name: %s" % intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "GetDailyBudget":
        return daily_budget()
    else:
        raise ValueError("Invalid intent")


def handler(event, context):
    if ('request' in event) and (event['request']['type'] == "IntentRequest"):
        return on_intent(event['request'], event['session'])
    else:
        # Dial 0
        daily_budget()
        # Dial 1; Update S&P500 Index
        sp500 = Stock('.INX')
        percent_change = sp500.percentagechange
        NIMBUS.set_dial_value(1, 0, "%s:%s" % ('S&P', percent_change))
        # Dial 2
        NIMBUS.set_dial_value(2, 0, "-")
        # Dial 3;
        NIMBUS.set_dial_value(3, 0, "-")
    
def log(message):
    if LOG_LEVEL and LOG_LEVEL == 'TRUE':
        print message


if __name__ == "__main__":
    while 1:
        try:
            ret = handler({}, 0)
            time.sleep(3)
        except KeyboardInterrupt:
            ret = 0
            break
        except:
            traceback.print_exc(file=sys.stdout)
            continue

    sys.exit(ret)

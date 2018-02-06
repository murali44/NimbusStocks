#!/bin/bash

echo preparing..
find . -name "*.pyc" -type f -delete
rm -rf ~/NimbusStocksEnv
rm -f ~/NimbusStocks.zip

echo adding code
zip -q -rg ~/NimbusStocks.zip *

echo adding dependencies
virtualenv -q ~/NimbusStocksEnv
source ~/NimbusStocksEnv/bin/activate
pip install -q -r requirements.txt
pushd $VIRTUAL_ENV/lib/python2.7/site-packages > /dev/null #make silent
zip -q -r9 ~/NimbusStocks.zip *

echo deploying lambda
aws lambda update-function-code --function-name NimbusStocks --zip-file fileb://~/NimbusStocks.zip --region us-west-2 --profile muralia

echo cleaning up
popd > /dev/null #make silent
rm -rf ~/NimbusStocksEnv
rm -f ~/NimbusStocks.zip

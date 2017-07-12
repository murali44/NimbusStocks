#!/bin/bash

find . -name "*.pyc" -type f -delete
rm -rf ~/NimbusStocksEnv

rm ~/NimbusStocks.zip
virtualenv ~/NimbusStocksEnv
source ~/NimbusStocksEnv/bin/activate

zip -rg ~/NimbusStocks.zip *

pip install -r requirements.txt
pushd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 ~/NimbusStocks.zip *

popd
rm -rf ~/NimbusStocksEnv

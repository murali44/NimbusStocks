######Updates stock info on a Wink Nimbus using AWS Lambda functions

![NimbusGif](https://github.com/murali44/image_repo/blob/master/WinkNimbus.gif)


######Installation
____________


git clone --recursive git@github.com:murali44/NimbusStocks.git

cd NimbusStocks

######Create a deployment package
___________________________

virtualenv nimbusstock_env

source nimbusstock_env

zip -rg ~/NimbusStocks.zip *

pip install -r requirements.txt

cd $VIRTUAL_ENV/lib/python2.7/site-packages

zip -r9 ~/NimbusStocks.zip *


######Deploy to AWS Lambda
____________________

Create an execution role. For more info see: http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html 





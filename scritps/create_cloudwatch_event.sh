#!/bin/bash

lambda="http://localhost:4574"
events=http://localhost:4587


echo "
     ##############################################################
     #######           Criando CloudWatch Event           #########
     ##############################################################
     "


aws --endpoint-url=$events events put-rule --name 'DailyRuleReport' --schedule-expression 'rate(1 day)'
aws --endpoint-url=$lambda lambda add-permission --function-name report --statement-id StartReport --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:us-west-2:111111111111:rule/DailyRuleReport
aws --endpoint-url=$events events put-targets --rule DailyRuleReport --targets '{"Id" : "1", "Arn": "arn:aws:lambda:us-east-1:000000000000:function:report"}'
 
aws --endpoint-url=$events events put-rule --name 'ScrapyInfoProduto' --schedule-expression 'rate(1 day)'
aws --endpoint-url=$lambda lambda add-permission --function-name getinfo --statement-id StartScrapyInfoProduto --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:us-west-2:111111111111:rule/ScrapyInfoProduto
aws --endpoint-url=$events events put-targets --rule ScrapyInfoProduto --targets '{"Id" : "1", "Arn": "arn:aws:lambda:us-east-1:000000000000:function:getinfo"}'
``

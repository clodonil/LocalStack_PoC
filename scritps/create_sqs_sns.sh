#!/bin/bash

# EndPoint do SQS
sqs=http://localhost:4576
sns=http://localhost:4575
ssm=http://localhost:4583


SNS_TOPIC="notification"
SQS_QUEUE="fila-de-compra"


aws configure set cli_follow_urlparam false

echo "
     ##############################################################
     #######            Criando SNS e  SQS                #########
     ##############################################################
     "



TOPIC_ARN=$(aws --endpoint-url=$sns sns create-topic --name $SNS_TOPIC --output text --query 'TopicArn')
QUEUE=$(aws --endpoint-url=$sqs sqs create-queue --queue-name $SQS_QUEUE --output text )

echo "TOPIC_ARN: $TOPIC_ARN"
echo "TOPIC_QUEUE: $QUEUE"


echo "
     ##############################################################
     #######         Salvando Dados no SSM                #########
     ##############################################################
     "


aws --endpoint-url=$ssm ssm put-parameter --name "SNS" --type "String" --value $TOPIC_ARN --overwrite
aws --endpoint-url=$ssm ssm put-parameter --name "SQS" --type "String" --value $QUEUE --overwrite
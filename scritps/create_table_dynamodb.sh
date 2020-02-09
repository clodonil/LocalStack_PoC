#!/bin/bash

dynamodb="http://localhost:4569"


echo "
     ########################################################
     #######  Criando tabela Dynamodb  Localmente   #########
     ########################################################
     "


TB_PRODUTOS=$(aws --endpoint-url=$dynamodb dynamodb create-table --table-name produtos  \
                  --attribute-definitions AttributeName=email,AttributeType=S AttributeName=produto,AttributeType=S \
                  --key-schema AttributeName=email,KeyType=HASH AttributeName=produto,KeyType=RANGE \
                  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
                  --output text --query 'TableDescription.[TableName,TableArn]')



TB_INFO=$(aws --endpoint-url=$dynamodb dynamodb create-table --table-name infos  \
              --attribute-definitions AttributeName=email,AttributeType=S AttributeName=url,AttributeType=S  \
              --key-schema AttributeName=email,KeyType=HASH AttributeName=url,KeyType=RANGE  \
              --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
              --output text --query 'TableDescription.[TableName,TableArn]')



tablename=$(echo $TB_PRODUTOS | awk {'print $1'})
tablearn=$(echo $TB_PRODUTOS | awk {'print $2'})

echo "Tablename: $tablename"
echo "TableArn: $tablearn"




tablename=$(echo $TB_INFO | awk {'print $1'})
tablearn=$(echo $TB_INFO | awk {'print $2'})

echo "Tablename: $tablename"
echo "TableArn: $tablearn"


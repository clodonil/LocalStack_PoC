#!/bin/bash

dynamodb="http://localhost:4569"


echo "
     ########################################################
     #######  Criando tabela Dynamodb  Localmente   #########
     ########################################################
     "


aws --endpoint-url=$dynamodb dynamodb create-table --table-name produtos  \
      --attribute-definitions AttributeName=email,AttributeType=S AttributeName=produto,AttributeType=S \
      --key-schema AttributeName=email,KeyType=HASH AttributeName=produto,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5



aws --endpoint-url=$dynamodb dynamodb create-table --table-name infos  \
      --attribute-definitions AttributeName=email,AttributeType=S AttributeName=url,AttributeType=S  \
      --key-schema AttributeName=email,KeyType=HASH AttributeName=url,KeyType=RANGE  \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
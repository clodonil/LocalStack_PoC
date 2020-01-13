#!/bin/bash

dynamodb="http://localhost:4569"


echo "
     ########################################################
     #######  Criando tabela Dynamodb  Localmente   #########
     ########################################################
     "


aws --endpoint-url=$dynamodb dynamodb create-table --table-name produtos  \
      --attribute-definitions AttributeName=email,AttributeType=N AttributeName=nome_produto,AttributeType=S \
      --key-schema AttributeName=email,KeyType=HASH AttributeName=nome_produto,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5



aws --endpoint-url=$dynamodb dynamodb create-table --table-name infos  \
      --attribute-definitions AttributeName=id,AttributeType=N AttributeName=url,AttributeType=S  \
      --key-schema AttributeName=id,KeyType=HASH AttributeName=url,KeyType=RANGE  \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

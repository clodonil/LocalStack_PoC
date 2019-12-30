#!/bin/bash

dynamodb="http://localhost:4569"

aws --endpoint-url=$dynamodb dynamodb create-table --table-name produtos  \
      --attribute-definitions AttributeName=id,AttributeType=N AttributeName=email,AttributeType=S \
      --key-schema AttributeName=id,KeyType=HASH AttributeName=email,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5



aws --endpoint-url=$dynamodb dynamodb create-table --table-name infos  \
      --attribute-definitions AttributeName=id,AttributeType=N AttributeName=url,AttributeType=S  \
      --key-schema AttributeName=id,KeyType=HASH AttributeName=url,KeyType=RANGE  \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

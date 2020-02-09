#!/bin/bash


./create_s3_site.sh
./create_table_dynamodb.sh
./deploy_lambda_local.sh
./create_sqs_sns.sh
#!/bin/bash


s3="http://localhost:4572"



echo "
     ##############################################################
     #######  Criando Bucket S3 para o site do frontEnd   #########
     ##############################################################
     "



aws --endpoint-url=$s3 s3 mb s3://frontend
aws --endpoint-url=$s3 s3 website s3://frontend --index-document index.html --error-document error.html
cd frontend
aws --endpoint-url=$s3 s3 cp .  s3://frontend/  --acl public-read --recursive


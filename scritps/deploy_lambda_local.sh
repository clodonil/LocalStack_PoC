#!/bin/bash

dir="/home/clodonil/Workspace/LocalStack_PoC/"
lambda="http://localhost:4574"

echo "
     #############################################
     #######  Deploy Lambda Localmente   #########
     #############################################
     "

echo "
     #############################################
     #######    Lambda ->  Busca Produto  #########
     #############################################
     "


cd $dir/lambda_busca_prod
mkdir package
pip install --target ./package/ -r requirements.txt > /dev/null
cp busca_produto.py package/
cd package
zip -r9 function.zip . > /dev/null
cd ..
mv package/function.zip .

LAMBDA_BUSCA_PRODUTO=$(aws --endpoint-url=$lambda lambda create-function --function-name busca_produto \
    --zip-file fileb://function.zip --handler busca_produto.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ \
     --output json --query [FunctionName,FunctionArn,Role])

rm -rf package
rm -rf *.zip


name=$(echo $LAMBDA_BUSCA_PRODUTO | awk {'print $1'})
arn=$(echo $LAMBDA_BUSCA_PRODUTO | awk {'print $2'})
role=$(echo $LAMBDA_BUSCA_PRODUTO | awk {'print $3'})


echo "lambdaName: $name"
echo "FunctionArn: $arn"
echo "FunctionRole: $role"


echo "
     #############################################
     #######    Lambda ->  getInfo  #########
     #############################################
     "


cd $dir/lambda_getinfo
mkdir package
pip install --target ./package -r requirements.txt > /dev/null
cp getinfo.py package/
cd package
zip -r9 function.zip . > /dev/null
cd ..
mv package/function.zip .

LAMBDA_GETINFO=$(aws --endpoint-url=$lambda lambda create-function --function-name getinfo \
    --zip-file fileb://function.zip --handler getinfo.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ \
     --output json --query [FunctionName,FunctionArn,Role])

rm -rf package
rm -rf *.zip

name=$(echo $LAMBDA_GETINFO | awk {'print $1'})
arn=$(echo $LAMBDA_GETINFO | awk {'print $2'})
role=$(echo $LAMBDA_GETINFO | awk {'print $3'})


echo "lambdaName: $name"
echo "FunctionArn: $arn"
echo "FunctionRole: $role"

echo "
     #############################################
     #######    Lambda ->  Comprar       #########
     #############################################
     "


cd $dir/lambda_comprar
mkdir package
pip install --target ./package -r requirements.txt > /dev/null
cp comprar.py package/
cd package
zip -r9 function.zip . > /dev/null
cd ..
mv package/function.zip .

LAMBDA_COMPRAR=$(aws --endpoint-url=$lambda lambda create-function --function-name comprar \
    --zip-file fileb://function.zip --handler comprar.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ \
     --output json --query [FunctionName,FunctionArn,Role])

rm -rf package
rm -rf *.zip

name=$(echo $LAMBDA_COMPRAR | awk {'print $1'})
arn=$(echo $LAMBDA_COMPRAR | awk {'print $2'})
role=$(echo $LAMBDA_COMPRAR | awk {'print $3'})


echo "lambdaName: $name"
echo "FunctionArn: $arn"
echo "FunctionRole: $role"
echo "
     #############################################
     #######    Lambda ->  Report       #########
     #############################################
     "


cd $dir/lambda_report
mkdir package
pip install --target ./package -r requirements.txt > /dev/null
cp report.py package/
cd package
zip -r9 function.zip . > /dev/null
cd ..
mv package/function.zip .

LAMBDA_REPORT=$(aws --endpoint-url=$lambda lambda create-function --function-name report \
    --zip-file fileb://function.zip --handler report.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ \
     --output text --query [FunctionName,FunctionArn,Role])

rm -rf package
rm -rf *.zip

name=$(echo $LAMBDA_REPORT | awk {'print $1'})
arn=$(echo $LAMBDA_REPORT | awk {'print $2'})
role=$(echo $LAMBDA_REPORT | awk {'print $3'})


echo "lambdaName: $name"
echo "FunctionArn: $arn"
echo "FunctionRole: $role"
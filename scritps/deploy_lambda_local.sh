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

aws --endpoint-url=$lambda lambda create-function --function-name busca_produto \
    --zip-file fileb://function.zip --handler busca_produto.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ

rm -rf package
rm -rf *.zip

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

aws --endpoint-url=$lambda lambda create-function --function-name getinfo \
    --zip-file fileb://function.zip --handler getinfo.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ

rm -rf package
rm -rf *.zip

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

aws --endpoint-url=$lambda lambda create-function --function-name comprar \
    --zip-file fileb://function.zip --handler comprar.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ
rm -rf package
rm -rf *.zip

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

aws --endpoint-url=$lambda lambda create-function --function-name report \
    --zip-file fileb://function.zip --handler report.handler --runtime python3.7 \
     --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ
rm -rf package
rm -rf *.zip

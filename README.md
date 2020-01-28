# Desenvolvendo para AWS usando SandBox Local

É muito comum nas empresas que adotam a cloud pública como AWS, pensarem em modelo para disponibilizarem aos desenvolveres recursos para testarem e homologarem as aplicações desenvolvidas.

Algumas empresas utilizam como estrategia disponibiliza a mesmo conta produtiva para teste e homologacao , separando os ambientes por vpc ou cluster utilizando chamadas API.  Seguindo a 2 lei de newton, esse ambiente em constante mudanca tende a degradar, e com o passar do tempo a segregacao dos ambientes nao sao respeitados. Esses modelo trás grandes ricos de desastre.

Outras empresas liberar uma conta AWS como SandBox para os desenvolvedores realizarem as chamadas de API. Pode parecer ser uma boa ideia, entretanto alguns riscos estão envolvidos nesse processo. Tais como:

1) Apesar da conta ser usado para SandBox, é uma conta normal na AWS, portanto pode surgir shadowIt, tornando o ambiente de SandBox em ambiente produtivo; Esse risco é maior quando não é usado infraestrutura como código.

2) Qualquer recurso instanciado é cobrado, portanto o risco de perder o controle da conta é grande; Uma chave de acesso vazada pode causar prejuízos enormes.

3) Risco de usar dados produtivos no ambiente de SandBox.

Considerando que uma adoção de cloud Pública envolve também adotar métodologias como Infra estrutura como código, não faz muito sentido liberar um console AWS para os desenvolvedores. O modelo ideal é o desenvolver construir a sua infraestrutura como código interagindo diretamente com as API do provider mocado localmente.

Para ganhar agilidade no desenvolvimento, o ideal é realizar toda a construção localmente, isso é, na máquina do desenvolvedor.

O computador local do desenvolver é o seu  SandBox. Ele pode construir e destruir o ambiente quantas vezes forem necessário, sem afetar outros projetos e sem custos já assumidos.

Dessa forma os desenvolvedores passam a conhecer os recursos principais da AWS atraves de chamadas de API local e  escrever a infraestrutura em código utilizando terraform ou cloudformation.

Validado localmente aplicação, a solução completa que envolve código e infraestrutura podem ser enviada para AWS e realizada o deploy através de uma pipeline.

Para validar localmente, vamos utilizar o localstack. Se você não conhece o localstack, preparei um tutorial com os principais recursos.

O localstack instância localmente os principais serviços AWS, possibilitando assim a criação de um SandBox local para desenvolvimento e aprendizagem.

Dessa forma o desenvolvedor constrói toda a infra localmente e desenvolve local realizando as chamadas para as API do localstack. Nesse momento não é necessário nenhuma conta da AWS. Tudo é realizado localmente.

Localstack utiliza a mesma interface de API que são utilizados nos recursos AWS. O desenvolvedor não tem nenhum prejuízo.

Após ter uma versão usável, o código e enviado o git, que inicia a pipeline.
A pipeline vai realizar as seguintes etapas:

1. Realizar o build da app;
2. Validar o cloudformation criado
3. Validar o teste de integração usando o localstack
4. Aplicar na conta AWS

# PoC usando o localstack

Para experimentar esse modelo, vamos propor o desenvolvimento de uma aplicação com os recursos AWS.

Aplicação é bastante simples, basicamente monitora o preço de um produto no site do Mercado Livre e após ficar abaixo de uma valor simula a compra.

O usuário acessa uma url e cadastra o nome do produto e o preço desejado. Recebe diariamente um reporte dos melhores preços.

Os recursos da AWS que serão utilizados:

* `S3`: Hospedagem do frontend do site e para armazenar a imagem do produto;
* `Lambda`: Para scrapy no mercado livre e OLX e montagem do email;
* `Dynamodb`: Persistir o histórico de preços;
* `SQS`: Fila para acionar o lambda;
* `SNS`: Envio do reporte; e
* `Cloudwatch`: schedule para lambda.

Vamos seguir o seguinte fluxo de desenvolvimento.

## Desenvolvimento local usando o LocalStack como SandBox

No computador local, usando o `Docker` inicializamos o `LocalStack` com o seguinte comando.

```bash
$ docker run -it  -p 4567-4599:4567-4599 -p 8080:8080 localstack/localstack
```

para facilitar a chamada dos EndPoint, criamos as seguintes variáveis de ambiente dos recursos que vamos utilizar durante o projeto.

```bash
# EndPoint do S3
export s3=http://localhost:4572

#EndPoint do Lambda
export lambda=http://localhost:4574

# EndPoint do SQS
export sqs=http://localhost:4576

# EndPoint do SNS
export sns=http://localhost:4575

# EndPoint do CloudWatch
export cloudwatch=http://localhost:4581

# EndPoint do Dynamodb
export dynamodb=http://localhost:4569

```

Também vamos precisar do `AWS CLI` instalado e configurado.

Para instalar vamos usar o seguinte comando:

```bash
$ pip install awscli
```

E para configurar vamos execucar o comando configure e nos campos `ACCESS KEY` e `SECRET ACCESS KEY` pode preencher com qualquer conteúdo. Não vamos usar essas chaves.


```
$ aws configure
     AWS Access Key ID [None]: xxxxxx
     AWS Secret Access Key [None]: xxxxxx
     Default region name [None]: us-east-1
     Default output format [None]: json
```


## FrontEnd - S3

Vamos começar o desenvolvimento com o frontend em html + Javascript que vai ficar hospedado no `S3`. O site está no diretório chamado frontend.

Para validar localmente o desenvolvimento do site, vamos criar um `Bucket` e subir o conteúdo do site. Neste primeiro momento, vamos criar usuando os comandos do `AWS CLI`, mais futuramente vamos criar o `CloudFormation` com toda a infraestrutura necessária.


Criando o Bucket com o nome `frontend`:

```
$ aws --endpoint-url=$s3 s3 mb s3://frontend
```

Vamos definir que esse site vai receber conteúdo de website:

```
$ aws --endpoint-url=$s3 s3 website s3://frontend --index-document index.html --error-document error.html
```

E para finalizar vamos copiar os arquivos do site para o bucket:

```
$ aws --endpoint-url=$s3 s3 cp .  s3://frontend/  --acl public-read --recursive
```

Vamos validar esse primeiro passo acessando o frontend..


http://localhost:4572/frontend/index.html

!(img/frontend.png)[Dashboard]

E também vamos acessar o site:

!(img/frontend.jpg)[FrontEnd]


## Lambda e DynamoDB

Nessa parte do desenvolvimento vamos criar as tabelas do DynamoDB e a conexão com os programas executadas pelas funções `lambda`.

A primeira tabela vamos chamar de `produtos`. Essa tabela vai receber o `input` realizado pelo site com o nome do produto que vai ser pesquisado e o preço desejado para compra e será complementado com os dados pesquisados.

Nessa fase vamos criar a tabela usando o `AWS CLI`, mais futuramente vamos criar o `CloudFormation` para deploy na AWS.

```
$ aws --endpoint-url=$dynamodb dynamodb create-table --table-name produtos  \
      --attribute-definitions AttributeName=email,AttributeType=S AttributeName=produto,AttributeType=S \
      --key-schema AttributeName=email,KeyType=HASH AttributeName=produto,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

Vamos realizar a primeira carga na tabela, simulando a entrada pelo site.

```
$ python dynamodb/popula_produtos.py
```

A segunda tabela vamos chamar de `infos`. Essa tabela terá ligação com a primeira tabela através do `id`, e vamos armazenar os links pesquisados e informações sobre o produto.

Nessa fase vamos criar a tabela usando o `AWS CLI`, mais futuramente vamos criar o `CloudFormation` para deploy na AWS.

```
$ aws --endpoint-url=$dynamodb dynamodb create-table --table-name infos  \
      --attribute-definitions AttributeName=email,AttributeType=S AttributeName=url,AttributeType=S  \
      --key-schema AttributeName=id,KeyType=HASH AttributeName=url,KeyType=RANGE  \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

Para popular a segunda tabela vamos desenvolver um função `lambda` que raspa os dados do Mercado Livre e salva no Dynamodb. 

Esse primeiro `lambda` só busca as URL dos produtos. 

> Em uma aplicação real, as URL pesquisadas deveriam ser aprovadas pelo usuário. Não faremos isso.

No diretório `lambda_busca_prod` temos toda a estrutura do função `lambda`, não vou entrar em detalhes da programação. Mais estamos usando `python` com `boto3`.

Para fazer o deploy da função `lambda` vamos criar um pacote com todos as dependências.

Vamos seguir o seguintes passos:

> Para deploy na AWS vamos utilizar uma pipeline.

1. Crie o diretório package:
  ```
  $ mkdir package
  ```

2. Instale todos as dependência utilizada:
  ```
  $ pip install --targget ./package -r requirements.txt
  ```

3. Copie o programa para o diretório package:
  ```
  cp busca_produto.py package/
  ```

4. Crie o pacote com o zip:
  ```
  $ zip -r9 function.zip package/.
  ```

Agora podemos realizar o deploy do `lambda` utilizando o `AWS CLI`.

```
aws --endpoint-url=$lambda lambda create-function --function-name busca_produto --zip-file fileb://function.zip --handler busca_produto.handler --runtime python3.7 --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ

{
    "FunctionName": "busca_produto",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:busca_produto",
    "Runtime": "python3.7",
    "Role": "arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ",
    "Handler": "busca_produto.handler",
    "CodeSize": 15274279,
    "Description": "",
    "Timeout": 3,
    "LastModified": "2019-12-30T14:40:53.051+0000",
    "CodeSha256": "MFsm0m7DBlU7Fq8gaPOPPVbJUGe8GCGiUY7Jr2XY/9w=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "06b9be26-b015-46ea-9726-ab6bd89e000d"
}
```

Como o deploy realizada da função `lambda` podemos realizar uma chamada para executação e certificar que a `lambda` funciona corretamente.

```
$ aws --endpoint-url=$lambda lambda invoke --function-name busca_produto --payload '{}' saida.txt
```

Após a execução da `lambda`podemos olhar no `dynamodb` e certificar que os dados foram gravados corretamente.

```
$ aws --endpoint-url=$dynamodb dynamodb scan --table-name produtos  --return-consumed-capacity TOTAL
$ aws --endpoint-url=$dynamodb dynamodb scan --table-name infos  --return-consumed-capacity TOTAL
```

Agora vamos criar uma segunda função em `lambda` que vai pegar as urls cadastradas e obter as informaçãoes como preço do produto.

Essa função em `lamdba` vai seguir as seguintes etapas:

1. Obter a lista ativos na tabela `produtos` do dynamodb;
2. Obter as urls ativas na tabela `infos`; 
3. Obter as informações do produto;
4. Gravar na tabela info as informações obtidas;
5. Atualizar a tabela `produto` com o preço min e max.

Essa lambda está no diretório `lambda_getinfo`, utilizamos o mesmo procedimento da primeira `lambda` para realizar o deploy.

A terceira função `lambda` gera um relatório com os preços dos produtos. Essa função `lambda` esta no diretório  `lambda_report`.

E a ultima função `lambda` simula a compra do produto se estiver abaixo ou igual ao preço desejado. Essa função está no diretório `lambda_report`.

Nessa fase realizamos o deploy de todas as funções `lambda`. No diretório `script/deploy_lambda_local.sh` estão todos os comandos utilizados.

Podemos olhar o dashboard do localstack.

![]()

# SNS

TOPIC_ARN=$(aws sns create-topic \
  --name service-proxy-topic \
  --output text \
  --query 'TopicArn')

2. AWS 


Pontos Positivos:

Durante o desenvolvimento, ficou muito fácil limpar todo o ambiente e começar novamente.
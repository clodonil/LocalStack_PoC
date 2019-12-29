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

PoC usando o localstack

Para expreementar esse modelo, vamos propor o desenvolvimento de uma aplicação com os recursos AWS.

Aplicação é bastante simples, basicamente monitora o preço de um produto no site da OLX e Mercado Livre.

O usuário acessa uma url e cadastra o nome do produto. Recebe diariamente um reporte dos melhores preços.

Os recursos da AWS que serão utilizados:
• S3: Hospedagem do frontend do site e para armazenar a imagem do produto.
• Lambda: Para scrapy no mercado livre e OLX e montagem do email.
• Dynamodb: Persistir o histórico de preços
• SQS: Fila para acionar o lambda
• SNS: Envio do reporte
• Cloudwatch: schedule para lambda.
Vamos seguir o seguinte fluxo de desenvolvimento.

1. Localmente:


2. AWS 

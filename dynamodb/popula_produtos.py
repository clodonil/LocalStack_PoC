import boto3

client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
table = client.Table('produtos')
    
dados = {
    "id" : 2,
    "email" : "clodonil@nisled.org",
    "detail" :
      {
      "produto":"Bola de Futebol",
      "status": "true",
      "preco_compra": "19",
      "min_preco": {"preco":"0"},
      "max_preco": {"preco":"0"}
      }
    
    
}

print(dados)
retorno=table.put_item(Item=dados)

print(retorno)


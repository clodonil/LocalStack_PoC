# -*- coding: utf-8 -*-
'''
classe: Scrapy
descrição: Exercicio para buscar todos os links de um site
autor: Clodonil Honorio Trigo
email: clodonil@nisled.org
data: 29 de Dezembro de 2019
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from boto3.dynamodb.conditions import Key, Attr
import time
import datetime
import logging
import boto3


class ScrapyML:
      def __init__(self):
          # links
          self.links = []
          self.domain = ""
          self.list_link = []
          self.list_prod = []
          self.max_link = 10

      def get_page(self,url):    
          '''
             Metodo que conecta na pagina
          '''
          #Domain
          self.domain = urlparse(url).netloc

          #conecta na pagina     
          fonte = requests.get(url)

          #Verifica se o status é de sucesso
          if fonte.status_code == 200:
              return  BeautifulSoup(fonte.text,"lxml")
          else:
              #Apresenta a mensagem de erro
              return(False)

      
      def busca_tag(self, page,tag):
          return page.find_all(tag)


      def clear(self, tag):
           '''
              Limpar lixo da tag
           '''
           return tag.replace("\n","").replace("\t","")


      def get_info(self,url):
          prod = self.get_page(url)
          
          
          t_preco   = prod.find('span', attrs={'class':'price-tag-fraction'})
          t_img     = prod.find('a', attrs={'class' : 'gallery-trigger gallery-item--landscape' })
          t_titulo  = prod.find('h1', attrs={'class' : 'item-title__primary' })
          timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
          
          if t_img != None:
              img = t_img.img.get('src')
          else:
              img = "None"  

          info = {
              'titulo': t_titulo.text.replace('\n','').replace('\t',''),              
              'preco' : t_preco.text,
              'img' : img,
              'timestamp' : timestamp
          }
            
          return info
              

def dynamodb_query(table, query):

    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    if query == 'full':
       retorno = table.scan()
    else:
       retorno = table.query(KeyConditionExpression=Key('email').eq(query))   

    return retorno['Items']


def dynamodb_save(table,head,dados):
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)

    retorno=table.update_item(Key=head,
                             UpdateExpression="set detail = :a",
                             ExpressionAttributeValues={':a': dados['detail']},
                             ReturnValues="UPDATED_NEW")


    if retorno['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def ssm_get(key):
    client = boto3.client('ssm', region_name='us-east-1', endpoint_url='http://localhost:4583')
    parameter = client.get_parameter(Name=key, WithDecryption=False)
    return parameter['Parameter']['Value']
    

def lista_compra(msg):
    sqs = boto3.resource('sqs',region_name='sa-east-1', endpoint_url='http://localhost:4576')
    ssm_queue = ssm_get('SQS')
    queue = sqs.get_queue_by_name(QueueName=ssm_queue)

       response = queue.send_message(MessageBody=msg)    

def handler(event, context):
     lista_produtos = dynamodb_query('produtos', 'full')
     for lista in lista_produtos:         
         if lista['detail']['status'] == 'true':
            preco_compra = lista['detail']['preco_compra'] 
            lista_url = dynamodb_query('infos',lista['email'])
            for item in lista_url:
                ml = ScrapyML()                
                infos = ml.get_info(item['url'])                                
                item['detail'].append(infos)
                
                head = {'email': item['email'], 'url': item['url']}

                #Enviar para a lista de compra
                if float(infos['preco']) <= float(preco_compra):
                   lista_compra(lista)

                
                if dynamodb_save('infos', head, item):
                    # Salvando o menor preco
                    if 'menor_preco' in lista['detail']:
                       if float(lista['detail']['menor_preco']['preco']) > float(infos['preco']):
                          lista['detail']['menor_preco'] = {'preco': infos['preco'],'url' : item['url']}
                    else:
                       lista['detail']['menor_preco'] = {'preco': infos['preco'],'url' : item['url']}

                    # Salvando o maior preco
                    if 'maior_preco' in lista['detail']:
                        if float(lista['detail']['maior_preco']['preco']) < float(infos['preco']):
                          lista['detail']['maior_preco'] = {'preco': infos['preco'],'url' : item['url']}
                    else:
                        lista['detail']['maior_preco'] = {'preco': infos['preco'],'url' : item['url']}
            print(lista)
            head = {'email': lista['email'], 'produto' : lista['produto']}
            dynamodb_save('produtos', head,lista)

            #Enviar para a lista de compra
            #if float(infos['preco']) <= float(preco_compra):
            #    lista_compra(lista)


handler('vdfsdfds','dsfsdfsd')
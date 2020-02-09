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


      def comprar(self,url,min_preco, preco_compra ):
          info = {'status': 'false'}
          prod = self.get_page(url)
          t_preco   = prod.find('span', attrs={'class':'price-tag-fraction'})
          timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
          
          if int(t_preco.text) <= int(min_preco):
             info = {
                'status' :'true',
                'message': "Compra realizada com sucesso!!!",              
                'preco' : t_preco.text,
                'timestamp' : timestamp,
                'economia' : ''
             }
            
          return info
              

def dynamodb_query(table, query):

    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    if query == 'full':
       retorno = table.scan()
    else:
       retorno = table.query(KeyConditionExpression=Key('id').eq(query))   

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



def handler(event, context):
     lista_produtos = dynamodb_query('produtos', 'full')
     for lista in lista_produtos:         
         if lista['detail']['status'] == 'true':
                ml = ScrapyML()
                min_preco = lista['detail']['menor_preco']['preco']                
                preco_compra = lista['detail']['preco_compra']
                if float(preco_compra) >= float(min_preco):
                   url = lista['detail']['menor_preco']['url'] 
                   info = ml.comprar(url,min_preco, preco_compra)
                   if info['status'] == 'true':
                      lista['detail']['status'] = 'false'
                      head = {'produto': lista['produto'], 'email' : lista['email']}
                      dynamodb_save('produtos', head,lista)  
                      print(info)
            
                   

handler('vdfsdfds','dsfsdfsd')
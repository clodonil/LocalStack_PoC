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
       retorno = table.query(KeyConditionExpression=Key('id').eq(query))   

    return retorno['Items']


def dynamodb_save(table,head,dados):
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)

    print(head)
    print(dados['detail'])
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
            lista_url = dynamodb_query('infos',lista['id'])
            for item in lista_url:
                ml = ScrapyML()                
                infos = ml.get_info(item['url'])                                
                item['detail'].append(infos)
            
                head = {'id': int(item['id']), 'url': item['url']}
                if dynamodb_save('infos', head, item):
                    if int(lista['detail']['min_preco']['preco']) != 0:
                       if int(lista['detail']['min_preco']['preco']) > int(infos['preco']):
                          lista['detail']['min_preco'] = {'preco': infos['preco'],'url' : item['url']}
                    else:
                       lista['detail']['min_preco'] = {'preco': infos['preco'],'url' : item['url']}

                    if int(lista['detail']['max_preco']['preco']) != 0:
                        if int(lista['detail']['max_preco']['preco']) < int(infos['preco']):
                          lista['detail']['max_preco'] = {'preco': infos['preco'],'url' : item['url']}
                    else:
                        lista['detail']['max_preco'] = {'preco': infos['preco'],'url' : item['url']}
            print(lista)
            head = {'id': lista['id'], 'email' : lista['email']}
            dynamodb_save('produtos', head,lista)  


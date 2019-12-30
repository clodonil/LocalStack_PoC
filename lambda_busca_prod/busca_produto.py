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

      def busca_links(self,page):
          ''' 
              Metodo para buscar o links da pagina e verifica se pertece ao mesmo dominio
          '''
          
          proximo = False
          for link in page.find_all('a', attrs={'class':'item__info-title'}):
              hlink = link.get('href')
              if len(link.text) > 0:
                 if not hlink in self.links:
                    if len(self.list_prod) < self.max_link:
                       if len(hlink) < 255:
                          self.list_prod.append(hlink) 
         

          if len(self.list_prod) < self.max_link:
             __next = page.find('li', attrs={'class':'andes-pagination__button andes-pagination__button--next'})
          
             print(__next)
             next_url = __next.a.get('href')
          
             if next_url != "#":
                proximo = next_url
   
          return proximo

      def clear(self, tag):
           '''
              Limpar lixo da tag
           '''
           return tag.replace("\n","").replace("\t","")

      def check_domain(self,url):
           if self.domain == urlparse(url).netloc:
               return True
           else:
               return False

      def run(self, site):
          '''
             Metodo para iniciar acao da classe
          '''
          #Domain
          self.domain = urlparse(site).netloc
          self.list_link.append([site])
          self.links.append(site)
          
          # busca link dos produtos
          while self.list_link:
               url = self.list_link.pop()                         
               next_page = self.busca_links(self.get_page(url[0]))                  
               if next_page:
                  self.list_link.append([next_page]) 

          return self.list_prod
          


def Dy_Get_Produto():
    table = 'produtos'
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    retorno = table.scan()
    print(retorno)
    return retorno['Items']


def dynamodb_save(table,id,url):
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    
    retorno= {'ResponseMetadata': {'HTTPStatusCode' : 300    }}
    keys = {'id': id, 'url': url, 'detail': []}
    try:
        retorno=table.put_item(Item=keys)
    except botocore.exceptions.ClientError as e:
        loggin.info(e)
        
    if retorno['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info(f"Salva: {url}")
        return True
    else:
        logging.info(f"Erro: {url}")
        return False



def handler(event, context):
    print("executando a lambda")
    for lista in Dy_Get_Produto(): 
        print(lista)
        if lista['detail']['status'] == 'true':
           produto = lista['detail']['produto'].lower().replace(" ","-")
           url="http://lista.mercadolivre.com.br/{0}#D[A:{0}]".format(produto)
           site_connect =ScrapyML()
           links = site_connect.run(url)
           print(links)             
           for link in links:
              dynamodb_save('infos',lista['id'],link)
                

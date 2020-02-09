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
import json


def dynamodb_query(table, query):
    
    retorno = {}
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    if query == 'full':
       retorno = table.scan()
       retorno = retorno['Items']
    else:
       email = query['email']
       produto = query['produto']
       try:
          retorno = table.query(KeyConditionExpression=Key('email').eq(email))
          retorno = retorno['Items']
       except Exception as e:
           logging.error(e) 

    
    return retorno

def notify_sns(arn,message):
    client = boto3.client('sns', endpoint_url='http://localhost:4575')
    response = client.publish(TargetArn=arn,Message=json.dumps(message))
    print(response)

def handler(event, context):
     lista_produtos = dynamodb_query('produtos', 'full')
     for lista in lista_produtos:         
         if lista['detail']['status'] == 'true':                
                query = {'email': lista['email'], 'produto': lista['produto']}
                info = dynamodb_query('infos',query)
                
                preco = 0
                itens = 0
                for item in info:
                    for scan in item['detail']:
                        preco += int(scan['preco'])
                        itens += 1
                   
                medio =  preco / itens

                
                min_preco = lista['detail']['menor_preco']['preco']
                max_preco = lista['detail']['menor_preco']['preco']                
                preco_compra = lista['detail']['preco_compra']

                report = {
                    'produto' : lista['produto'],
                    'PrecoDesejado': lista['detail']['preco_compra'],
                    'menor_preco' : lista['detail']['menor_preco']['preco'],
                    'maior_preco' : lista['detail']['maior_preco']['preco'],
                    'itens_pesquisados' : itens,
                    'preco_medio' : medio
                }            

                arn = 'arn:aws:sns:us-east-1:000000000000:notificacao-compra'
                notify_sns(arn, report)
                
                print(report)




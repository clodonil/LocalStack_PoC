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

def dynamodb_query(table, query):
    
    client = boto3.resource('dynamodb',region_name='sa-east-1', endpoint_url='http://localhost:4569')
    table = client.Table(table)
    if query == 'full':
       retorno = table.scan()
    else:
       retorno = table.query(KeyConditionExpression=Key('id').eq(query))   

    return retorno['Items']


def handler(event, context):
     lista_produtos = dynamodb_query('produtos', 'full')
     for lista in lista_produtos:         
         if lista['detail']['status'] == 'true':
                info = dynamodb_query('infos',lista['id'])
 
                preco = 0
                itens = 0
                for item in info:
                    for scan in item['detail']:
                        preco += int(scan['preco'])
                        itens += 1
                   
                medio =  preco / itens

                min_preco = lista['detail']['min_preco']['preco']
                max_preco = lista['detail']['min_preco']['preco']                
                preco_compra = lista['detail']['preco_compra']

                report = {
                    'produto' : lista['detail']['produto'],
                    'PrecoDesejado': lista['detail']['preco_compra'],
                    'menor_preco' : lista['detail']['min_preco']['preco'],
                    'maior_preco' : lista['detail']['max_preco']['preco'],
                    'itens_pesquisados' : itens,
                    'preco_medio' : medio
                }            

                print(report)


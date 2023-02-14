# -*- coding: utf-8 -*-
"""
Created on Tues Feb 14 09:57 2023

@author: gustavoerven
Código para baixar arquivos da LAI do endereço https://falabr.cgu.gov.br/publico/DownloadDados/DownloadDadosLai.aspx.

ACESSO:
AAAAMMDD_relatorio_pedidos_AAAA.csv
AAAAMMDD _solicitantes_AAAA.csv


RECURSOS/RECLAMAÇÕES:
AAAAMMDD_relatorio_recursos_reclamacoes_AAAA.csv
AAAAMMDD _solicitantes_AAAA.csv

Ambos compactados em ZIP.

URL BASE PARA PEDIDOS DE ACESSO: https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/Pedidos_fff_YYYY.zip

URL BASE PARA RECURSOS/RECLAMAÇÕES: https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/Recursos_Reclamacoes_fff_YYYY.zip

fff:csv ou xml, YYYY: ano

"""

import requests
from datetime import date
import shutil
import os
import time
import argparse

ANO_INICIO=2012
PREFIXO_ACESSO = "Pedidos"
PREFIXO_RECURSO = "Recursos_Reclamacoes"
NOME_ARQUIVO_BASE = "{prefixo}_{formato_arquivo}_{ano}.zip"
URL_BASE = "https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/{nome_arquivo}"

def busca_lai_por_anos(anos, tipo_dados='acesso', localizacao='./', formato_arquivo='csv'):
    """
    anos: Lista de anos para download.
    tipo_dados: Se o arquivo é de acesso ou recurso
    localizacao: Onde salvar os arquivos
    formato_arquivo: formatos xml|csv
    """
    if tipo_dados.lower() == "acesso":
        prefix = PREFIXO_ACESSO
    else:
        prefix = PREFIXO_RECURSO

    for year in anos:
        nome_arquivo  = NOME_ARQUIVO_BASE.format(prefixo=prefix, formato_arquivo=formato_arquivo, ano=str(year))
        url = URL_BASE.format(nome_arquivo=nome_arquivo)
        try:
            response = requests.get(url, stream=True)
            with open(os.path.join(localizacao, nome_arquivo), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            print(f"Arquivo {nome_arquivo} baixado de {url}")
        except Exception as e:
            print(e)
            print(f"Error baixando arquivo {nome_arquivo} da url {url}")

        time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exemplo", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--ano-inicio", help="Ano de início para download")
    parser.add_argument("-t", "--tipo-dado", help="Tipo de dado: acesso|recurso")
    parser.add_argument("-l", "--localizacao", help="Local para salvar o arquivo")
    parser.add_argument("-f", "--formato-arquivo", help="Formato do arquivo desejado: csv|xml")
    args = parser.parse_args()
    config = vars(args)

    try:
        ano_inicio = int(config['ano_inicio'])
    except:
        ano_inicio = int(date.today().strftime("%Y"))

    if config['tipo_dado'] != None:
        tipo_dado = config['tipo_dado']
    else:
        tipo_dado = 'acesso'

    if config['localizacao'] != None:
        localizacao = config['localizacao']
    else:
        localizacao = '../../data/'

    if config['formato_arquivo'] != None:
        formato_arquivo = config['formato_arquivo']
    else:
        formato_arquivo = 'csv'

    anos = range(ano_inicio, int(date.today().strftime("%Y"))+1)

    busca_lai_por_anos(anos, tipo_dado, localizacao, formato_arquivo)

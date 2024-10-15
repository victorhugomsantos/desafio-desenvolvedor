from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.core.files.storage import default_storage
from django.db.models import Q
from .models import ArquivoUpload, ConteudoArquivo
from .serializers import ArquivoUploadSerializer, ConteudoArquivoSerializer
import hashlib
import pandas as pd
import os

# Função auxiliar para calcular o hash do arquivo
def calcular_hash(arquivo):
    hash_md5 = hashlib.md5()
    for chunk in arquivo.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Endpoint para upload de arquivo
class UploadArquivoView(APIView):
    def post(self, request):
        arquivo = request.FILES.get('arquivo')
        
        if not arquivo:
            return Response({"erro": "Arquivo não enviado"}, status=status.HTTP_400_BAD_REQUEST)
        
        hash_arquivo = calcular_hash(arquivo)
        
        # Verifica se o arquivo já foi enviado antes
        if ArquivoUpload.objects.filter(hash_arquivo=hash_arquivo).exists():
            return Response({"erro": "Arquivo já foi enviado"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Salvar o arquivo no sistema de arquivos
        caminho_arquivo = default_storage.save(arquivo.name, arquivo)
        nome_arquivo = os.path.basename(caminho_arquivo)
        
        # Cria o registro no banco de dados
        novo_arquivo = ArquivoUpload.objects.create(
            nome_arquivo=nome_arquivo,
            hash_arquivo=hash_arquivo
        )
        
        # Lê o conteúdo do arquivo CSV ou Excel
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo)
        elif arquivo.name.endswith('.xlsx'):
            df = pd.read_excel(caminho_arquivo)
        else:
            return Response({"erro": "Formato de arquivo inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verifique se as colunas esperadas existem
        #colunas_esperadas = {'RptDt', 'TckrSymb', 'MktNm', 'SctyCtgyNm', 'ISIN', 'CrpnNm'}
       # if not colunas_esperadas.issubset(df.columns):
         #   return Response({"erro": "Colunas do arquivo estão incorretas"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Salvar o conteúdo do arquivo na base de dados
        for _, linha in df.iterrows():
            ConteudoArquivo.objects.create(
                arquivo=novo_arquivo,
                rpt_dt=linha['RptDt'],
                tckr_symb=linha['TckrSymb'],
                mkt_nm=linha['MktNm'],
                scty_ctgy_nm=linha['SctyCtgyNm'],
                isin=linha['ISIN'],
                crpn_nm=linha['CrpnNm']
            )
        
        return Response({"mensagem": "Arquivo enviado com sucesso"}, status=status.HTTP_201_CREATED)

# Endpoint para histórico de upload
class HistoricoUploadView(APIView):
    def get(self, request):
        nome_arquivo = request.query_params.get('nome_arquivo')
        data_referencia = request.query_params.get('data_referencia')
        
        uploads = ArquivoUpload.objects.all()
        
        # Filtros
        if nome_arquivo:
            uploads = uploads.filter(nome_arquivo__icontains=nome_arquivo)
        
        if data_referencia:
            # Ajuste o nome do campo para o correto
            uploads = uploads.filter(data_upload__date=data_referencia)
        
        serializer = ArquivoUploadSerializer(uploads, many=True)
        return Response(serializer.data)

# Endpoint para buscar conteúdo do arquivo
from rest_framework.pagination import PageNumberPagination

class BuscarConteudoArquivoView(APIView, PageNumberPagination):
    page_size = 20  # Define tamanho da paginação

    def get(self, request):
        tckr_symb = request.query_params.get('TckrSymb')
        rpt_dt = request.query_params.get('RptDt')
        
        conteudos = ConteudoArquivo.objects.all()
        
        if tckr_symb and rpt_dt:
            conteudos = conteudos.filter(tckr_symb=tckr_symb, rpt_dt=rpt_dt)
        
        # Paginação
        resultado_paginado = self.paginate_queryset(conteudos, request, view=self)
        serializer = ConteudoArquivoSerializer(resultado_paginado, many=True)
        
        return self.get_paginated_response(serializer.data)


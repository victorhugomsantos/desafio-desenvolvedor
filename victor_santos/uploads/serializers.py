from rest_framework import serializers
from .models import ArquivoUpload, ConteudoArquivo

class ArquivoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoUpload
        fields = ['id', 'nome_arquivo', 'data_envio']

class ConteudoArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConteudoArquivo
        fields = ['rpt_dt', 'tckr_symb', 'mkt_nm', 'scty_ctgy_nm', 'isin', 'crpn_nm']

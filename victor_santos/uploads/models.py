from django.db import models

class ArquivoUpload(models.Model):
    nome_arquivo = models.CharField(max_length=255)
    data_envio = models.DateTimeField(auto_now_add=True)
    hash_arquivo = models.CharField(max_length=64, unique=True)  # hash para nome ser unico

    def __str__(self):
        return self.nome_arquivo


class ConteudoArquivo(models.Model):
    arquivo = models.ForeignKey(ArquivoUpload, on_delete=models.CASCADE)
    rpt_dt = models.DateField()
    tckr_symb = models.CharField(max_length=50)
    mkt_nm = models.CharField(max_length=50)
    scty_ctgy_nm = models.CharField(max_length=50)
    isin = models.CharField(max_length=50)
    crpn_nm = models.CharField(max_length=255)

def __str__(self):
        return self.nome_arquivo

class HistoricoUpload(models.Model):
    nome_arquivo = models.CharField(max_length=255, unique=True)
    data_upload = models.DateTimeField(auto_now_add=True)

	
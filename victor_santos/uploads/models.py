from django.db import models

class HistoricoUpload(models.Model):
    nome_arquivo = models.CharField(max_length=255, unique=True)
    data_upload = models.DateTimeField(auto_now_add=True)

class ConteudoArquivo(models.Model):
    rpt_dt = models.DateField()
    tckr_symb = models.CharField(max_length=50)
    mkt_nm = models.CharField(max_length=50)
    scty_ctgy_nm = models.CharField(max_length=50)
    isin = models.CharField(max_length=12)
    crpn_nm = models.CharField(max_length=255)
    historico = models.ForeignKey(HistoricoUpload, on_delete=models.CASCADE)


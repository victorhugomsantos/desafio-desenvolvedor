from django.urls import path
from .views import UploadArquivoView, HistoricoUploadView, BuscarConteudoView

urlpatterns = [
    path('upload/', UploadArquivoView.as_view(), name='upload-arquivo'),
    path('historico/', HistoricoUploadView.as_view(), name='historico-upload'),
    path('buscar/', BuscarConteudoView.as_view(), name='buscar-conteudo')
   
]


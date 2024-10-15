# Generated by Django 5.1.2 on 2024-10-15 18:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_arquivo', models.CharField(max_length=255)),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('hash_arquivo', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_arquivo', models.CharField(max_length=255, unique=True)),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConteudoArquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpt_dt', models.DateField()),
                ('tckr_symb', models.CharField(max_length=50)),
                ('mkt_nm', models.CharField(max_length=50)),
                ('scty_ctgy_nm', models.CharField(max_length=50)),
                ('isin', models.CharField(max_length=50)),
                ('crpn_nm', models.CharField(max_length=255)),
                ('arquivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploads.arquivoupload')),
            ],
        ),
    ]

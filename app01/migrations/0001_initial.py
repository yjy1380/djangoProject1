# Generated by Django 4.2.3 on 2023-08-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='miRNA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miRNAname', models.CharField(max_length=24, verbose_name='miRNA name')),
                ('EvidenceCode', models.CharField(max_length=24, verbose_name='Evidence Code')),
                ('Diseasename', models.CharField(max_length=36, verbose_name='Disease name')),
                ('PMID', models.IntegerField(verbose_name='PMID')),
                ('Description', models.CharField(max_length=1024, verbose_name='Description')),
                ('Causality', models.CharField(max_length=1024, verbose_name='Causality')),
            ],
        ),
    ]
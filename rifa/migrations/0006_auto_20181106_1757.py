# Generated by Django 2.1.2 on 2018-11-06 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rifa', '0005_auto_20181106_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffle',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rifa.Category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='choosed_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número sorteado'),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='desc',
            field=models.CharField(max_length=500, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='qtd_num',
            field=models.IntegerField(verbose_name='Quantidade de números'),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='value',
            field=models.FloatField(verbose_name='Valor unitário'),
        ),
    ]

# Generated by Django 3.2.6 on 2022-11-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_departamento_api_defesas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('base_de_dados', models.JSONField(null=True)),
                ('dados_do_mapa', models.JSONField(null=True)),
            ],
        ),
    ]

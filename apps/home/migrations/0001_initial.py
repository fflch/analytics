from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(max_length=10)),
                ('api_docentes', models.JSONField()),
                ('api_programas', models.JSONField()),
                ('api_programas_docente', models.JSONField()),
                ('api_pesquisa', models.JSONField()),
                ('api_pesquisa_parametros', models.JSONField()),
                ('api_programas_docente_limpo', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docente_id', models.CharField(max_length=255)),
                ('api_docente', models.JSONField()),
                ('api_programas', models.JSONField()),
            ],
        ),
    ]
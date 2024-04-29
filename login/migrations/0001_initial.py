# Generated by Django 5.0.4 on 2024-04-28 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('cedula', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('celular', models.CharField(blank=True, max_length=10, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('contrasena', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fisioterapeuta',
            fields=[
                ('cedula', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('celular', models.CharField(blank=True, max_length=10, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('contrasena', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('cedula', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('celular', models.CharField(blank=True, max_length=10, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('contrasena', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoEjercicio',
            fields=[
                ('tipoEjercicioID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoLesion',
            fields=[
                ('lesionID', models.AutoField(primary_key=True, serialize=False)),
                ('nombreLesion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Terapia',
            fields=[
                ('terapiaID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('fecha', models.DateField(null=True)),
                ('cedulaFisioterapeuta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.fisioterapeuta')),
                ('cedulaPaciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Resultados',
            fields=[
                ('resultadoID', models.AutoField(primary_key=True, serialize=False)),
                ('cantidadPos', models.IntegerField(default=0)),
                ('cantidadNeg', models.IntegerField(default=0)),
                ('terapiaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.terapia')),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('movimientoID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('terapiaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.terapia')),
            ],
        ),
        migrations.CreateModel(
            name='AsignarTerapias',
            fields=[
                ('AgigID', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('terapiaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.terapia')),
            ],
        ),
        migrations.CreateModel(
            name='Ejercicios',
            fields=[
                ('ejercicioID', models.AutoField(primary_key=True, serialize=False)),
                ('porcentaje', models.FloatField()),
                ('movimientoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.movimiento')),
                ('tipoEjercicioID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.tipoejercicio')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPaciente',
            fields=[
                ('historialID', models.AutoField(primary_key=True, serialize=False)),
                ('cedulaPaciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.paciente')),
                ('lesionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.tipolesion')),
            ],
        ),
    ]

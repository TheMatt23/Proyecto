# Generated by Django 5.0.4 on 2024-04-25 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_remove_movimientosejercicios_ejercicioid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('ejercicioID', models.AutoField(primary_key=True, serialize=False)),
                ('porcentaje', models.FloatField()),
                ('movimientoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.movimiento')),
                ('tipoEjercicioID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.tipoejercicio')),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-03-16 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlStock', '0019_delete_historialfactura'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateTimeField()),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('domicilio', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('condicion_venta', models.CharField(default='efectivo', max_length=100)),
                ('condicion_fiscal', models.CharField(default='Arg.Consumidor Final', max_length=100)),
                ('fecha_vencimiento_pago', models.DateField()),
                ('cuit_dni', models.CharField(max_length=100)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controlStock.producto')),
            ],
        ),
    ]

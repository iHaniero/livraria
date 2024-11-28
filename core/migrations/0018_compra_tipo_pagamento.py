# Generated by Django 5.1.3 on 2024-11-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_compra_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="compra",
            name="tipo_pagamento",
            field=models.IntegerField(
                choices=[
                    (1, "Cartão de Crédito"),
                    (2, "Cartão de Débito"),
                    (3, "PIX"),
                    (4, "Boleto"),
                    (5, "Transferência Bancária"),
                    (6, "Dinheiro"),
                    (7, "Outro"),
                ],
                default=1,
            ),
        ),
    ]
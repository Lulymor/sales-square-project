# Generated by Django 4.2 on 2023-04-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_qtd_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemordered',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
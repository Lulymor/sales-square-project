# Generated by Django 4.2 on 2023-04-20 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qtd_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

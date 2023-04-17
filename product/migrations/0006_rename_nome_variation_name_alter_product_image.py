# Generated by Django 4.2 on 2023-04-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='nome',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/'),
        ),
    ]
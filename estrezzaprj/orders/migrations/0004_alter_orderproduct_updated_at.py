# Generated by Django 4.2.2 on 2023-07-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
# Generated by Django 4.2.2 on 2023-07-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('orders', '0002_remove_orderproduct_color_remove_orderproduct_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]

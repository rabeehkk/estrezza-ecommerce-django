# Generated by Django 4.2.2 on 2023-07-06 08:50

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, max_length=100, null=True, populate_from='product_name', unique=True),
        ),
    ]

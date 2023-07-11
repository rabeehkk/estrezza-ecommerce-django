# Generated by Django 4.2.2 on 2023-07-06 08:50

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, max_length=100, null=True, populate_from='category_name', unique=True),
        ),
    ]
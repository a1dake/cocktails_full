# Generated by Django 4.2.3 on 2024-07-11 10:43

import base.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=base.fields.ChoiceArrayField(base_field=models.CharField(choices=[('Customer', 'Customer'), ('Manager', 'Manager'), ('Administrator', 'Administrator')], default='Customer'), default=list, size=None, verbose_name='Роли'),
        ),
    ]

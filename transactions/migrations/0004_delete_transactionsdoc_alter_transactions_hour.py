# Generated by Django 4.1.5 on 2023-01-26 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transactionsdoc'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransactionsDoc',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='hour',
            field=models.TimeField(),
        ),
    ]
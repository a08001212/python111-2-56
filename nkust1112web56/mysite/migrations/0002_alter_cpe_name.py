# Generated by Django 4.2.1 on 2023-06-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpe',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]

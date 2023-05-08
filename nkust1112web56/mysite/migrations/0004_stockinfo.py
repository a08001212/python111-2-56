# Generated by Django 4.1.7 on 2023-05-08 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_phonemaker_phonemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('mprice', models.FloatField()),
            ],
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-20 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_pay',
            field=models.IntegerField(default=0),
        ),
    ]
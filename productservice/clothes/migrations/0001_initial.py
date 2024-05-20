# Generated by Django 5.0.6 on 2024-05-19 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0002_alter_book_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField()),
                ('createAt', models.DateField(auto_now_add=True)),
                ('description', models.CharField(default='', max_length=255)),
                ('brand', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=100)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.category')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.product')),
            ],
            options={
                'verbose_name': 'clothes',
                'verbose_name_plural': 'clothes',
                'db_table': 'clothes',
            },
        ),
    ]
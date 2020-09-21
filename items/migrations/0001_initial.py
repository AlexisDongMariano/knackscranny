# Generated by Django 3.1 on 2020-09-20 00:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='default.png', upload_to='item_pics')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.category')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='regular', max_length=100)),
                ('alias', models.CharField(blank=True, max_length=150, unique=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('inventory', models.PositiveIntegerField(blank=True, default=0)),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
        ),
        migrations.CreateModel(
            name='VariationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=100)),
                ('alias', models.CharField(blank=True, max_length=150, unique=True)),
                ('image', models.ImageField(default='default_variation.png', upload_to='item_variation_pics')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.variation')),
            ],
        ),
    ]
# Generated by Django 3.1 on 2020-09-20 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='name',
            new_name='code',
        ),
    ]
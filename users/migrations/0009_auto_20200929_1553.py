# Generated by Django 3.1 on 2020-09-29 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='default_profile.png', upload_to='profile_pics'),
        ),
    ]

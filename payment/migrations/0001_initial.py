# Generated by Django 3.1 on 2020-09-11 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payment_method', models.CharField(choices=[('S', 'Stripe'), ('P', 'Paypal')], max_length=1)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

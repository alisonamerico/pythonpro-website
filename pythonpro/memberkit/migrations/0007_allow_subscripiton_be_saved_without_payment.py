# Generated by Django 3.2.4 on 2021-06-10 02:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_pagarme', '0005_change_primary_key_to_big_integer'),
        ('memberkit', '0006_include_cohort_subscription_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                       to='django_pagarme.pagarmepayment'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-12-12 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0008_auto_20191212_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biddedamount',
            name='pincode',
        ),
    ]
# Generated by Django 2.1.7 on 2019-12-04 08:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bidding', '0002_auto_20191204_1219'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='biddedamount',
            unique_together={('name', 'product')},
        ),
    ]

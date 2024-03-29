# Generated by Django 2.1.7 on 2019-12-12 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0009_remove_biddedamount_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='pending_orders',
            name='mail',
            field=models.EmailField(default='manojmanyala@gmail.com', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pending_orders',
            name='status',
            field=models.CharField(choices=[('Order Received', 'Order Received'), ('Order Shipped', 'Order Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Done', 'Done')], default='Order Received', max_length=100),
        ),
    ]

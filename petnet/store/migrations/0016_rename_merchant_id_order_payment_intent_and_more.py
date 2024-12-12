# Generated by Django 5.0.8 on 2024-08-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_product_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='merchant_id',
            new_name='payment_intent',
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('draft', 'Draft'), ('deleted', 'Deleted'), ('waitingapproval', 'Waiting approval')], default='active', max_length=50),
        ),
    ]

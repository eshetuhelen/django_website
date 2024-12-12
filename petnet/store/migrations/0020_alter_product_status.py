# Generated by Django 5.1 on 2024-08-23 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('deleted', 'Deleted'), ('waitingapproval', 'Waiting approval'), ('active', 'Active'), ('draft', 'Draft')], default='active', max_length=50),
        ),
    ]
# Generated by Django 5.1 on 2024-08-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='Default Product Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('deleted', 'Deleted'), ('active', 'Active'), ('waitingapproval', 'Waiting approval'), ('draft', 'Draft')], default='active', max_length=50),
        ),
    ]

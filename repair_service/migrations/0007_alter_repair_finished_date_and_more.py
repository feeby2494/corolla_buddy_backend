# Generated by Django 4.1.3 on 2022-11-28 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repair_service', '0006_work_order_delivery_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='finished_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='repair',
            name='received_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='repair',
            name='shipping_order',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repair_list', to='repair_service.shipping_order'),
        ),
    ]

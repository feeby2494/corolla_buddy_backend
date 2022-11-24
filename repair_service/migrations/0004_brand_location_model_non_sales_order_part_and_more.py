# Generated by Django 4.1.3 on 2022-11-22 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repair_service', '0003_alter_sales_order_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='model_list', to='repair_service.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Non_Sales_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_profit', models.FloatField(default=0.0)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Part_Repair_Type_Association',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_service.part')),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('serial', models.CharField(max_length=60)),
                ('completed', models.BooleanField(default=False)),
                ('received_date', models.DateTimeField()),
                ('finished_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Shipping_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=90)),
                ('tracking', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Repair_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_type_list', to='repair_service.model')),
                ('parts', models.ManyToManyField(through='repair_service.Part_Repair_Type_Association', to='repair_service.part')),
            ],
        ),
        migrations.CreateModel(
            name='Repair_Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosed_date', models.DateTimeField()),
                ('repair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_job_list', to='repair_service.repair')),
            ],
        ),
        migrations.AddField(
            model_name='repair',
            name='shipping_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_list', to='repair_service.shipping_order'),
        ),
        migrations.AddField(
            model_name='repair',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_list', to='repair_service.work_order'),
        ),
        migrations.AddField(
            model_name='part_repair_type_association',
            name='repair_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_service.repair_type'),
        ),
        migrations.CreateModel(
            name='Part_Instance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defective', models.BooleanField(default=False)),
                ('used', models.BooleanField(default=False)),
                ('broken_by_tech', models.BooleanField(default=False)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_instance_list', to='repair_service.part')),
                ('repair_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_used_list', to='repair_service.repair_job')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_list', to='repair_service.location')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_list', to='repair_service.part')),
            ],
        ),
    ]
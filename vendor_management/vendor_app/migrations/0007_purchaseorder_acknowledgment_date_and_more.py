# Generated by Django 4.2.3 on 2023-11-26 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0006_remove_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='items',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='quality_rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='quantity',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor_app.vendor'),
        ),
    ]

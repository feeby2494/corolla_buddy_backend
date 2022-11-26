from rest_framework import serializers

from .models import Work_Order, Repair, Sales_Order, Shipping_Order

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Order
        fields = (
            "id",
            "completed",
            "submitted_date",
            "sales_order",
            "slug",
            "repair_list",
        )

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Order
        fields = (
            "id",
            "total_profit",
            "slug",
            "work_order_list",
            "calculate_total",
            "get_absolute_url",
            
        )

class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Order
        fields = (
            "id",
            "brand",
            "model",
            "serial",
            "work_order",
            "completed",
            "received_date",
            "finished_date",
            "shipping_order",
            "submitted_date",
            "sales_order",
            "slug",
            "repair_job_list"
        )
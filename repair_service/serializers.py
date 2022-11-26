from rest_framework import serializers

from .models import Work_Order, Repair, Sales_Order, Shipping_Order, Repair_Job

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

# Have an issue with calling a serializer before it being defined
# these two serializers depend on each other, I might have to give
# up calling one.

class RepairJobSerializer(serializers.ModelSerializer):
    #repair = RepairSerializer() #Do I need something passed in here?
    class Meta:
        model = Repair_Job
        feilds = (
            "id",
            "name",
            "diagnosed_date"
            "repair"
        )

class RepairSerializer(serializers.ModelSerializer):
    repair_job_list = RepairJobSerializer(many=True)
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



class ShippingOrderSerializer(serializers.ModelSerializer):
    repair_list = RepairSerializer(many=True)
    class Meta:
        model: Shipping_Order
        fields = (
            "id",
            "service",
            "tracking",
            "repair_list"
        )
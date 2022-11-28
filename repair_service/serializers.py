from rest_framework import serializers

from .models import Work_Order, Repair, Sales_Order, Shipping_Order, Repair_Job, Expenditure_Item, Revenue_Item, CustomerAddress, CustomerContact

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
        def create(self, validated_data):
            return Repair.objects.create({
                'brand': validated_data.get['brand'],
                'model': validated_data.get['model'],
                'serial': validated_data.get['serial'],
                'work_order': validated_data.get['work_order'],
            })

        # def update(self, instance, validated_data):
        #     instance.content = validated_data.get('bran', instance.content)
        #     instance.created = validated_data.get('diagnosed_date', instance.created)
        #     instance.save()
        #     return instance

class WorkOrderSerializer(serializers.ModelSerializer):
    repair_list = RepairSerializer(many=True)

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
    
    def create(self, validated_data):
            return Work_Order.objects.create(**validated_data)

class ExpenditureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model: Expenditure_Item
        fields = (
            "id",
            "name",
            "description",
            "total",
            "sales_order"
        )

class RevenueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model: Revenue_Item
        fields = (
            "id",
            "name",
            "description",
            "total",
            "sales_order"
        )

class SalesOrderSerializer(serializers.ModelSerializer):
    work_order_list = WorkOrderSerializer(many=True)
    expenditure_item_list = ExpenditureItemSerializer(many=True)
    revenue_item_list = RevenueItemSerializer(many=True)

    class Meta:
        model = Work_Order
        fields = (
            "id",
            "total_profit",
            "slug",
            "work_order_list",
            "calculate_total",
            "get_absolute_url",
            "expenditure_item_list",
            "revenue_item_list",
            "expenditure_item_list",
            "revenue_item_list"
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

class CustomerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model: CustomerContact
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "work_order",
            "sales_order"
        )

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model: CustomerAddress
        fields = (
            "id",
            "street_line_one",
            "street_line_two",
            "city",
            "state",
            "zip",
            "work_order",
            "sales_order"
        )
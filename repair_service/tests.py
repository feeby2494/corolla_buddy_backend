from django.test import TestCase
from .models import *

# Testing the Back-Refs, and anything related to Sales_Order:
class Sales_Order_TestCase(TestCase):
    def setUp(self):

        # Create one SO, three work orders, rev_items, and exp_items connected 
        # to this SO: 
        Sales_Order.objects.create()
        so1 = Sales_Order.objects.filter(id=1).first()
        Work_Order.objects.create(sales_order = so1, slug = 1)
        Work_Order.objects.create(sales_order = so1, slug = 2)
        Work_Order.objects.create(sales_order = so1, slug = 3)
        Expenditure_Item.objects.create(
            sales_order = so1, 
            name = "iPhone LCD", 
            total = 45.07
        )
        Expenditure_Item.objects.create(
            sales_order = so1, 
            name = "iPhone Battery", 
            total = 11.88
        )
        Expenditure_Item.objects.create(
            sales_order = so1, 
            name = "iPhone Charging Port", 
            total = 2.37
        )
        Revenue_Item.objects.create(
            sales_order = so1, 
            name = "iPhone LCD Repair", 
            total = 75.99
        )
        Revenue_Item.objects.create(
            sales_order = so1, 
            name = "iPhone Battery Repair", 
            total = 45.99
        )
        Revenue_Item.objects.create(
            sales_order = so1, 
            name = "iPhone Charging Port Repair", 
            total = 65.99
        )

        Sales_Order.objects.create()
        so2 = Sales_Order.objects.filter(id=2).first()
        Work_Order.objects.create(sales_order = so2, slug = 4)
        Work_Order.objects.create(sales_order = so2, slug = 5)
        Work_Order.objects.create(sales_order = so2, slug = 6)
        Expenditure_Item.objects.create(
            sales_order = so2, 
            name = "iPhone OLED", 
            total = 130.87
        )
        Expenditure_Item.objects.create(
            sales_order = so2, 
            name = "iPhone Battery", 
            total = 15.99
        )
        Expenditure_Item.objects.create(
            sales_order = so2, 
            name = "iPhone Charging Port", 
            total = 5.99
        )
        Revenue_Item.objects.create(
            sales_order = so2, 
            name = "iPhone LCD Repair", 
            total = 180.99
        )
        Revenue_Item.objects.create(
            sales_order = so2, 
            name = "iPhone Battery Repair", 
            total = 80.55
        )
        Revenue_Item.objects.create(
            sales_order = so2, 
            name = "iPhone Charging Port Repair", 
            total = 95.99
        )

    def test_cal_total_for_sales_order(self):
        so1 = Sales_Order.objects.filter(id = 1).first()
        so2 = Sales_Order.objects.filter(id = 2).first()
        self.assertEqual(so1.calculate_total(), 128.65)
        self.assertEqual(so2.calculate_total(), 204.68)



########## Documentation Reference #####################
#     from django.test import TestCase
# from myapp.models import Animal

# class AnimalTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')
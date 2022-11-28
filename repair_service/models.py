from io import BytesIO
from PIL import Image

from django.conf import settings

from django.core.files import File
from django.db import models


# Individual Repair
class Repair(models.Model):
    # Do we need these tied to the Brand and Model tables?
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=60)
    work_order = models.ForeignKey(
        'Work_Order',
        related_name='repair_list',
        on_delete=models.CASCADE,
    )
    completed = models.BooleanField(default=False)
    #tech_id = will tie into user that has a tech role
    received_date = models.DateTimeField(null=True, blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    shipping_order = models.ForeignKey(
        'Shipping_Order',
        related_name='repair_list',
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        db_constraint=False
    )

    def __str__(self):
        return str(self.id)

################ Will Need To Intergrate with Detrack/Fedex/USPS later ######

# Not tied to work order or sales order; can have any repair on here
class Shipping_Order(models.Model):
    service = models.CharField(max_length=90)
    tracking = models.IntegerField()
    #repair_list
    

# Individual job that are on one individual repair
class Repair_Job(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    diagnosed_date = models.DateTimeField()
    repair = models.ForeignKey(
        'repair',
        related_name='repair_job_list',
        on_delete=models.CASCADE,
    )

########## Inventory System ###########################

# an intance of one single part that can be used on a repair
class Part_Instance(models.Model):
    part = models.ForeignKey(
        'Part',
        related_name='part_instance_list',
        on_delete=models.CASCADE,
    )
    defective = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    broken_by_tech = models.BooleanField(default=False)
    repair_job = models.ForeignKey(
        'Repair_Job',
        related_name='part_used_list',
        on_delete=models.CASCADE,
    )

class Part(models.Model):
    name = models.CharField(max_length=90)
    def __str__(self):
        return self.name

class Repair_Type(models.Model):
    name = models.CharField(max_length=90)
    parts = models.ManyToManyField(
        Part,
        through='Part_Repair_Type_Association'
    )
    model = models.ForeignKey(
        'Model',
        related_name='repair_type_list',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name

class Part_Repair_Type_Association(models.Model):
    repair_type = models.ForeignKey(
        Repair_Type,
        on_delete=models.CASCADE
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE
    )

class Inventory(models.Model):
    part = models.ForeignKey(
        'part',
        related_name='inventory_list',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        related_name='inventory_list',
        on_delete=models.CASCADE
    )
    count = models.IntegerField(default=0)

class Location(models.Model):
    name = models.CharField(max_length=90)

class Model(models.Model):
    name = models.CharField(max_length=90)
    brand = models.ForeignKey(
        'Brand',
        related_name='model_list',
        on_delete=models.CASCADE
    )

class Brand(models.Model):
    name = models.CharField(max_length=60)


# One order with one or more Repairs on it
class Work_Order(models.Model):
    completed = models.BooleanField(default=False)
    submitted_date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(max_length=90, default="local")
    #repair_list = 1-to-Many Back Ref: This back-ref should be defined by Django
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name='work_order_list',
    #     on_delete=models.CASCADE,
    # )
    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='work_order_list',
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        db_constraint=False
    )
    slug = models.SlugField()

    def ready(self):
        slug = self.id

    class Meta:
        ordering = ('submitted_date',)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f'/{self.slug}/'

############### Sales System ###################

# The invoice order for one or more work orders
class Sales_Order(models.Model):
    #revenue_item_list = 1-to-Many Back Ref
    #expenditure_item_list = 1-to-Many Back Ref
    #work_order_list = 1-to-Many Back Ref
    total_profit = models.FloatField(default=0.00)
    slug = models.SlugField(blank=True, null=True)

    def ready(self):
        slug = self.id

    def calculate_total(self):
        # This is how you can reference reverse relationships!
        total = 0.00
        for item in self.revenue_item_list.all():
            total += item.total
        for item in self.expenditure_item_list.all():
            total -= item.total
        total = round(total, 2)
        return total

    def __str__(self):
        return str(self.id)

    # Should I tie this in to work order's slug?
    def get_absolute_url(self):
        return f'/{self.slug}/'

### Should Rev_Items and Exp_Items be tied to a part instance and/or repair_job?


class Expenditure_Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    total = models.FloatField()

    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='expenditure_item_list',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Revenue_Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    total = models.FloatField()

    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='revenue_item_list',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

################# Accounting System: with Sales Orders and non-Sales Orders: ###


# Not tied to repair; Example: gas, food, supplies, monthly bill, etc
class Non_Sales_Order(models.Model):
    total_profit = models.FloatField(default=0.00)
    slug = models.SlugField(blank=True, null=True)

    def ready(self):
        slug = self.id

    def calculate_total(self):
        # This is how you can reference reverse relationships!
        total = 0.00
        for item in self.revenue_item_list.all():
            total += item.total
        for item in self.expenditure_item_list.all():
            total -= item.total
        total = round(total, 2)
        return total

    def __str__(self):
        return str(self.id)

    # Should I tie this in to work order's slug?
    def get_absolute_url(self):
        return f'/{self.slug}/'

################# Customer Contact: ###
class CustomerContact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    work_order = models.ForeignKey(
        'Work_Order',
        related_name='customer_contact_list',
        on_delete=models.CASCADE,
    )
    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='customer_contact_list',
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        db_constraint=False
    )

    def __str__(self):
        return str(self.email)

################# Customer Address: ###
class CustomerAddress(models.Model):
    street_line_one = models.CharField(max_length=60)
    street_line_two = models.CharField(max_length=10)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    work_order = models.ForeignKey(
        'Work_Order',
        related_name='customer_address_list',
        on_delete=models.CASCADE,
    )
    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='customer_address_list',
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        db_constraint=False
    )

    def __str__(self):
        return str(f"{self.street_line_one} {self.street_line_two} {self.city}")














# For Reference Only:


# class Person(models.Model):
#     SHIRT_SIZES = (
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#     )
#     name = models.CharField(max_length=60)
#     shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

# class Runner(models.Model):
#     MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
#     name = models.CharField(max_length=60)
#     medal = models.CharField(blank=True, choices=MedalType.choices, max_length=10)

# class Product(models.Model):
#     category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     slug = models.SlugField()
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-date_added',)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return f'/{self.category.slug}/{self.slug}/'

#     def get_image(self):
#         if self.image:
#             return 'http://127.0.0.1:8000' + self.image.url
#         else:
#             return ''
    
#     def get_thumbnail(self):
#         if self.thumbnail:
#             return 'http://127.0.0.1:8000' + self.thumbnail.url
#         else:
#             if self.image:
#                 self.thumbnail = self.make_thumbnail(self.image)
#                 self.save()

#                 return 'http://127.0.0.1:8000' + self.thumbnail.url
#             else:
#                 return ''

#     def make_thumbnail(self, image, size=(300, 200)):
#         img = Image.open(image)
#         img.convert('RGB')
#         img.thumbnail(size)

#         thumb_io = BytesIO()
#         img.save(thumb_io, 'JPEG', quality=85)

#         thumbnail = File(thumb_io, name=image.name)

#         return thumbnail

    
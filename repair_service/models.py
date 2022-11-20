from io import BytesIO
from PIL import Image

from django.contrib.auth.models import User

from django.core.files import File
from django.db import models

class Work_Order(models.Model):
    completed = models.BooleanField(default=False)
    submitted_date = models.DateTimeField(auto_now_add=True)

    #repair_list = 1-to-Many Back Ref: This back-ref should be defined by Django
    user = models.ForeignKey(
        User,
        related_name='work_orders',
        on_delete=models.CASCADE,
    )
    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='work_orders',
        on_delete=models.CASCADE,
    )
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Sales_Order(models.Model):
    #revenue_item_list = 1-to-Many Back Ref
    #expenditure_item_list = 1-to-Many Back Ref
    #work_order_list = 1-to-Many Back Ref
    total_profit = models.FloatField()
    slug = models.SlugField()

    def calculate_total(self):
        # Don't understand how we reference back relationships
        # total = 0.00
        # for item in revenue_item_list:
        #   total += item.total
        # for item in expenditure_item_list:
        #   total -= item.total
        #return total
        pass

    def __str__(self):
        return self.id

    # Should I tie this in to work order's slug?
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Expenditure_Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(blank=True, null=True)
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
    description = models.CharField(blank=True, null=True)
    total = models.FloatField()

    sales_order = models.ForeignKey(
        'Sales_Order',
        related_name='revenue_item_list',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

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

    
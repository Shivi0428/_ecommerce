from django.db import models
from django.contrib.auth.models import User

# Instance Model
class Instance(models.Model):
    type = models.CharField(max_length=100)
    vcpus = models.IntegerField()
    memory = models.DecimalField(max_digits=5, decimal_places=2)
    storage = models.CharField(max_length=100)
    network = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.type

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Instance, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.type} - {self.quantity}'

# State Choices for Customer Model
STATE_CHOICES = (
    ('Avon', 'Avon'),
    ('Bedfordshire', 'Bedfordshire'),
    ('Berkshire', 'Berkshire'),
    ('Buckinghamshire', 'Buckinghamshire'),
    ('Cambridgeshire', 'Cambridgeshire'),
    ('Cheshire', 'Cheshire'),
    ('Cleveland', 'Cleveland'),
    ('Cornwall', 'Cornwall'),
    ('Cumbria', 'Cumbria'),
    ('Derbyshire', 'Derbyshire'),
    ('Devon', 'Devon'),
    ('Dorset', 'Dorset'),
    ('Durham', 'Durham'),
    ('East Sussex', 'East Sussex'),
    ('Essex', 'Essex'),
    ('Gloucestershire', 'Gloucestershire'),
    ('Greater London', 'Greater London'),
    ('Greater Manchester', 'Greater Manchester'),
    ('Hampshire', 'Hampshire'),
    ('Herefordshire', 'Herefordshire'),
    ('Hertfordshire', 'Hertfordshire'),
    ('Humberside', 'Humberside'),
    ('Isle of Wight', 'Isle of Wight'),
    ('Kent', 'Kent'),
    ('Lancashire', 'Lancashire'),
    ('Leicestershire', 'Leicestershire'),
    ('Lincolnshire', 'Lincolnshire'),
    ('Merseyside', 'Merseyside'),
    ('Norfolk', 'Norfolk'),
    ('Northamptonshire', 'Northamptonshire'),
    ('Northumberland', 'Northumberland'),
    ('North Humberside', 'North Humberside'),
    ('North Yorkshire', 'North Yorkshire'),
    ('Nottinghamshire', 'Nottinghamshire'),
    ('Oxfordshire', 'Oxfordshire'),
    ('Shropshire', 'Shropshire'),
    ('Somerset', 'Somerset'),
    ('South Humberside', 'South Humberside'),
    ('South Yorkshire', 'South Yorkshire'),
    ('Staffordshire', 'Staffordshire'),
    ('Suffolk', 'Suffolk'),
    ('Surrey', 'Surrey'),
    ('Tyne and Wear', 'Tyne and Wear'),
    ('Warwickshire', 'Warwickshire'),
    ('West Midlands', 'West Midlands'),
    ('West Sussex', 'West Sussex'),
    ('West Yorkshire', 'West Yorkshire'),
    ('Wiltshire', 'Wiltshire'),
    ('Worcestershire', 'Worcestershire')
)

# Customer Model
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

# Category Choices for Product Model
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)

# Product Model
class Product(models.Model):
    title = models.CharField(max_length=100, default='')
    selling_price = models.FloatField(default=0.0)
    discounted_price = models.FloatField(default=0.0)
    description = models.TextField(default='')
    brand = models.CharField(max_length=100, default='')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='')
    product_image = models.ImageField(upload_to='productimg', default='productimg/default.jpg')
    code = models.CharField(max_length=10, default='')
    type = models.CharField(max_length=255, default='')
    vcpus = models.IntegerField(default=0)
    memory = models.FloatField(default=0.0)
    storage = models.CharField(max_length=255, default='')
    network = models.CharField(max_length=255, default='')
    price = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title

    @property
    def total_cost(self):
        return self.quantity * self.discounted_price

# Order Status Choices
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)

# OrderPlaced Model
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

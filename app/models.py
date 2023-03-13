from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

STATE_CHOICES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),
    ("Lakshadweep", "Lakshadweep"),
    ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
    ("Puducherry", "Puducherry"),
)

CATEGORY_CHOICES = (
    ("M", "Mobile"),
    ("L", "Laptop"),
    ("TV", "Television"),
    ("TW", "Top Wear"),
    ("BW", "Bottom Wear"),
    ("WW", "Wrist Watch"),
    ("SH", "Shoes"),

)

STATUS_CHOICES = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self) -> str:
        return str(self.id)  # type: ignore


class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self) -> str:
        return str(self.id)  # type: ignore


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)  # type: ignore

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class PlacedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    orered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Accepted")

    def __str__(self) -> str:
        return str(self.id)  # type: ignore

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
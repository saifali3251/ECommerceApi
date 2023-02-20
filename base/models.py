from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# User to Product is 1-* so Product has user field from User table as FK
class Product(models.Model):
    # setting on_delete=models.SET_NULL since we don't want to delete the actual Product 
    # if user delete it from there cart. We just set it to NULL. Also null=True means we are allowing 
    # Null value in DB
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # SET_NULL => bcs we dont want to delete the pdt. so using SET_NULL
    name = models.CharField(max_length=200, null=True, blank=True)
    # if the static field is not set initially, when we upload image, it is uploaded into backend folder by default
    # In order to change the default path, we need to add few thing in settings.py
    image = models.ImageField(null=True, blank=True,default='/placeholder.png')
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    # _id is default field auto created
    _id = models.AutoField(primary_key=True, editable=False)
    # we are using custom _id. so django will use this _id instead of default id

    def __str__(self):
        return self.name


# Product has 1-* with Review(product field)
# User has 1-* with Review(user field)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    # returning rating
    def __str__(self):
        return str(self.rating)


# Order contain the order made by which user and all details and status about the order
# User has 1-* with Order table(user field)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return "Order Id : "+str(self._id)+" : "+self.user.first_name+" Order date : "+str(self.createdAt)
        # return {"Order by "self.user+" Date : "+str(self.createdAt)}


# OrderItem contains the status of Items User has orders and complete status of Items
# Product has 1-* with OrderItem table(product field)
# Order has 1-* with OrderItem table(order field)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


# Order has 1-1 with ShippingAddress table(order field)
# on_Delete=models.CASCADE since we need to delete ShippingAddress if the Order is deleted
class ShippingAddress(models.Model):
  # one to one with Order model
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
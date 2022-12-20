from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.db.models.signals import post_save

from account.models import Account

class Product_Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Address_Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to="product_images")
    slug = models.SlugField(null=True, blank=True)
    product_desc = models.TextField()

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("product:add_to_cart", kwargs={
            "slug": self.slug
        })

    def get_remove_to_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    aparment_address = models.CharField(max_length=255)
    country = CountryField(multiple=True)
    zip_code = models.CharField(max_length=255)
    address_default = models.BooleanField(default=False)
    address_type = models.ForeignKey(Address_Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"

class Payment(models.Model):
    stripe_charge_id = models.CharField( max_length=50)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=255, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total = self.coupon.amount
        return total

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    product_refund_image = models.ImageField(upload_to="product_refund_images")
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = Account.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=Account)
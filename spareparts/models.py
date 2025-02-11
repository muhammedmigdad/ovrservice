from django.db import models
from users.models import User
from common.models import CommonModel
from customers.models import Customer

ORDER_STATUS = [
    ('IN', 'In Progress'),
    ('SH', 'Shipped'),
    ('DL', 'Delivered'),
    ('CN', 'Cancelled'),
]

class StoreUser(CommonModel):
    storeuser_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'storeusers_StoreUser'
        verbose_name = 'storeuser'
        verbose_name_plural = 'storeusers'
        ordering = ["-id"]

    def __str__(self):
        return f'{self.user.phone_number}-{self.user.email}'

class Store(CommonModel):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store', null=True, blank=True)

    class Meta:
        db_table = 'store'
        verbose_name = 'store'
        verbose_name_plural = 'stores'
        ordering = ('id',)

    def __str__(self):
        return self.name

class StoreCategory(CommonModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'store_category'
        verbose_name = 'store_category'
        verbose_name_plural = 'store_categories'
        ordering = ('id',)

    def __str__(self):
        return self.store.name

class Product(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = 'items_product'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('-id',)

    def __str__(self):
        return self.name

class ProductDetails(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'items_productdetail'
        verbose_name = 'productdetail'
        verbose_name_plural = 'productdetails'
        ordering = ('-id',)

    def __str__(self):
        return self.name

class Review(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ["-id"]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"



class OrderItem(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.FloatField(default=0)

    class Meta:
        db_table = 'customers_order_item'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        ordering = ["-id"]

    def __str__(self):
        return self.product.name

class CartTotal(models.Model):
    item_total = models.FloatField(default=0)
    total = models.FloatField(default=0)
    tax_charge = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Customer_CartTotal'
        verbose_name = 'carttotal'
        verbose_name_plural = 'carttotals'
        ordering = ['-id']

    def __str__(self):
        return self.customer.user.email

class Order(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=35)
    items = models.ManyToManyField(OrderItem)
    sub_total = models.FloatField(default=0)
    tax_charge = models.FloatField(default=0)
    total = models.FloatField(default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    order_status = models.CharField(max_length=25, choices=ORDER_STATUS, default='IN')
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    pincode = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'customers_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ["-id"]

    def __str__(self):
        return self.order_id
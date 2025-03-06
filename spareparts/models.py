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
    image = models.ImageField(upload_to='review', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = 'items_product'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('-id',)

    def __str__(self):
        return self.name

class ProductDetails(CommonModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='review', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'items_productdetail'
        verbose_name = 'productdetail'
        verbose_name_plural = 'productdetails'
        ordering = ('-id',)

    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='review', blank=True, null=True)
    rating = models.FloatField(default=0)

    class Meta:
        db_table = 'customers_review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ["-id"]

    def __str__(self):
        return self.name

class CartItem(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()  # Save the price at the time of adding to cart

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def total_price(self):
        return self.price * self.quantity
    


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
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('net_banking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    ]

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
    
    # ✅ Add this field
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')

    class Meta:
        db_table = 'customers_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ["-id"]

    def __str__(self):
        return self.order_id

    
    
class Service(CommonModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title

class ServiceRequest(CommonModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    details = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_service_request'
        verbose_name = 'service_request'
        verbose_name_plural = 'service_requests'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.service.title}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:30]}..."
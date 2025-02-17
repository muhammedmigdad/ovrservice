from django.db import models
from users.models import User
from common.models import CommonModel


class Customer(CommonModel):
    customer_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customers_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ["-id"]

    def __str__(self):

        return f'{self.user.phone_number}-{self.user.email}'
    
    

    





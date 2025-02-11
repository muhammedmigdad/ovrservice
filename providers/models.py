from django.db import models
from users.models import User
from common.models import CommonModel
from customers.models import Customer


class ProviderUser(CommonModel):
    provideruser_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'provideruser'
        verbose_name = 'provideruser'
        verbose_name_plural = 'providerusers'
        ordering = ["-id"]


    def __str__(self):
        return f'{self.user.phone_number}-{self.user.email}'
    

    
    
class Service(CommonModel):
    title = models.CharField(max_length=255)
    provider = models.ForeignKey(ProviderUser, on_delete=models.CASCADE)
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
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_service_request'
        verbose_name = 'service_request'
        verbose_name_plural = 'service_requests'
        ordering = ["-id"]

    def __str__(self):
        return self.service.title
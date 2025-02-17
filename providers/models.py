from django.db import models
from users.models import User
from common.models import CommonModel
from customers.models import Customer


class ProviderUser(CommonModel):
    provideruser_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'provideruser'
        verbose_name = 'Provider User'
        verbose_name_plural = 'Provider Users'
        ordering = ["-id"]

    def __str__(self):
        return f'{self.user.phone_number}-{self.user.email}'

class ProviderService(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProviderServiceRequest(CommonModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE)
    provider_user = models.ForeignKey(ProviderUser, on_delete=models.CASCADE, related_name="service_requests")
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.service.name} ({self.status})'

    
    
    
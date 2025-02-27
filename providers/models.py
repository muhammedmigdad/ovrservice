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
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE)
    provider_user = models.ForeignKey(ProviderUser, on_delete=models.CASCADE, related_name="service_requests")
    details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return f"{self.name} - {self.status}"
    
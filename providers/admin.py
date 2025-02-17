from django.contrib import admin
from providers.models import *

admin.site.register(ProviderUser)
admin.site.register(ProviderService)
admin.site.register(ProviderServiceRequest)


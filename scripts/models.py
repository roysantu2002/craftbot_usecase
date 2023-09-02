from django.db import models

# Create your models here

from django.db import models

class NetworkDeviceInfo(models.Model):
    ip_address = models.GenericIPAddressField()
    host_name = models.CharField(max_length=255)
    info = models.TextField()

    def __str__(self):
        return f"{self.host_name} ({self.ip_address})"


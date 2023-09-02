from django.db import models

# Create your models here

from django.db import models

class NetworkDeviceInfo(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    host_name = models.CharField(max_length=255)
    info = models.TextField()

    def __str__(self):
        return f"{self.host_name} ({self.ip_address})"


class NetworkDeviceLog(models.Model):
    device = models.ForeignKey(NetworkDeviceInfo, on_delete=models.CASCADE)
    log_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.device.host_name} ({self.device.ip_address})"

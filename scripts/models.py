from django.db import models # Import your NetworkKeyword model

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    # Add more choices as needed
)

# Define the choices for the 'level' field
SUPPORT_CHOICES = [
    ('L1', 'Level 1'),
    ('L2', 'Level 2'),
    ('L3', 'Level 3'),
    # Add more choices as needed
]


class ScriptInfo(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the script
    description = models.TextField(blank=True, null=True)  # Description of the script (optional)
    script_file = models.FileField(upload_to='scripts/', blank=True)  # Store the script file
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the record was created
    last_modified = models.DateTimeField(auto_now=True)  # Timestamp for when the record was last modified
    author = models.CharField(max_length=255)  # Author of the script
    version = models.CharField(max_length=50, blank=True)  # Version number of the script
    arguments = models.TextField(blank=True)  # Arguments required by the script
    execution_frequency = models.CharField(max_length=50, blank=True)  # How often the script runs
    level = models.CharField(max_length=20, choices=SUPPORT_CHOICES, default='L1')
    info = models.TextField()

    def __str__(self):
        return self.name
    
class NetworkKeyword(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=SUPPORT_CHOICES, default='L1')
    script_info = models.ForeignKey(ScriptInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword


class NetworkDeviceInfo(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    host_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    info = models.TextField()

    def __str__(self):
        return f"{self.host_name} ({self.ip_address})"


class NetworkDeviceLog(models.Model):
    device = models.ForeignKey(NetworkDeviceInfo, on_delete=models.CASCADE)
    log_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.device.host_name} ({self.device.ip_address})"

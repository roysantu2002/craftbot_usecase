from django.core.management.base import Base
from django.utils import timezone
from script.models import NetworkDeviceLog

class Command(BaseCommand):
    help = 'Cleanup old log entries'

    def handle(self, *args, **kwargs):
        # Calculate the date five days ago
        five_days_ago = timezone.now() - timezone.timedelta(days=5)

        # Delete log entries older than five days
        NetworkDeviceLog.objects.filter(created_at__lt=five_days_ago).delete()

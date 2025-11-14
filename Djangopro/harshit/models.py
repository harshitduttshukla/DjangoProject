from django.db import models
from django.utils import timezone

# Create your models here.
class ChaiVarity(models.Model):
    CHAI_TYPES = [
        ('ML','Masala'),
        ('GR','Ginger'),
        ('TL','Tulsi'),
        ('LV','Lavender'),
        ('OT','Other'),
    ]
    name=models.CharField(max_length=100)
    image = models.ImageField(upload_to='chais/')
    date_added=models.DateTimeField(default=timezone.now)
    type=models.CharField(max_length=2, choices=CHAI_TYPES)
    description=models.TextField(default='')

    def __str__(self):
        return self.name
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class EmergencyRequest(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.ForeignKey(City,on_delete=models.CASCADE,default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} @ {self.timestamp} in {self.city or 'Unknown'}"
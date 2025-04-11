from django.db import models
from django.contrib.auth.models import User

class State(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.name

class Categories(models.Model):
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
    cat = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} @ {self.timestamp} in {self.city or 'Unknown'}"
    
class Paymentplatforms(models.Model):
    name = models.CharField(max_length=100, blank=True)
    types = models.CharField(max_length=100, blank=True)
    #qr = models.ImageField(upload_to=media, default='Null',blank=True,null=True,storage=LocalStorage())

class Currentlocations():
    groupname = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class HelpCentres(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)

    city = models.ForeignKey(City,on_delete=models.CASCADE,default=1)
    cat = models.ManyToManyField(Categories)


    def __str__(self):
        return f"{self.phone} @ {self.timestamp} in {self.city or 'Unknown'}"
    

class Suppliers(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.ForeignKey(City,on_delete=models.CASCADE,default=1)
    cat = models.ManyToManyField(Categories)
    timestamp = models.DateTimeField(auto_now_add=True)

class Blogpost(models.Model):

    class  BlogCategory(models.TextChoices):
        GENERAL = 'general', 'General'
        WARNING = 'warning', 'Warning'
        UPDATE = 'update', 'Update'
        RESOURCE = 'resource', 'Resource'
        SAFETY = 'safety', 'Safety'

    category = models.CharField(max_length=10, choices=BlogCategory.choices, default=BlogCategory.GENERAL)
    author = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

#As there are multiple images per blogpost, they're their own model
class BlogpostImage(models.Model):
    blogpost = models.ForeignKey(Blogpost, on_delete=models.CASCADE, related_name='blog_images') 
    #related_name lets you refer to all the image objects by blogpost.blog_images.all()

    image_reference = models.ImageField(upload_to='blog_images/')

    def blogpost_image_absolute_filepath(self):
        if self.image_reference and hasattr(self.image_reference, 'path'):
            return self.image_reference.path
        return None




    
    
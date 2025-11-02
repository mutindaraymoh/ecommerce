from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
      return self.name


class Category(models.Model):
    image = models.ImageField(upload_to="product/")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
      return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)

    def _str_(self):
        return self.user.username
      


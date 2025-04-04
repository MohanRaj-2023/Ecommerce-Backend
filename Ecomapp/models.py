from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(null=False,blank=False)
    productinfo = models.TextField(null=True,blank=True)
    status = models.BooleanField(default=False,help_text='0-show,1-hide')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#Size moel
class Size(models.Model):
    SIZE_TYPE_CHOICES = [
        ("numeric","Numeric"),
        ('label',"Label")
    ]
    name = models.CharField(max_length=10,unique=True)
    size_type = models.CharField(max_length=50,choices=SIZE_TYPE_CHOICES) 
    
    def __str__(self):
        return f"{self.name} - {self.size_type}"
    
#Color model
class Color(models.Model):
    name = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    productname = models.CharField(max_length=150)
    image = models.ImageField(null=True,blank=True)
    vendor = models.CharField(max_length=150,null=False,blank=False)
    productinfo = models.TextField(null=True,blank=True)
    rating = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    orginal_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    selling_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    status = models.BooleanField(default=False,help_text='0-show,1-hide')
    trending = models.BooleanField(default=False,help_text='0-defauly,1-trending')
    created_at = models.DateTimeField(auto_now_add=True)

    GENDER_CHOICES = [
        ("boy","Boy"),
        ("girl","Girl"),
        ("men","Men"),
        ("women","Women"),
        ("unisex","Unisex")
        ]
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=True)

    def __str__(self):
        return f"{self.productname} -{self.category}- {self.get_gender_display()}"
    

#product variant
class ProductVariant(models.Model):
    products = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="variant")
    size = models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    stockcount = models.IntegerField(null=True,blank=True,default=0)
     
    def __str__(self):
        return f"{self.products.productname} - {self.color} - {self.size} - {self.stockcount}" 
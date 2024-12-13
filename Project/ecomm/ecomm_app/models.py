from django.db import models
from django.contrib.auth.models import User

class product(models.Model):
    CAT=(1,'Mobile'),(2,'Shoes'),(3,'Clothes')
    name=models.CharField(max_length=50, verbose_name="Product_name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=1000, verbose_name="Product_details")
    cat=models.IntegerField()
    is_active=models.BooleanField(default=True, verbose_name="Available")
    pimage=models.ImageField(upload_to='image')
    
    # def __str__(self):
    #     return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    
    
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    
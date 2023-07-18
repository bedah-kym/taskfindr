
from django.db import models

# Create your models here.
class Paymentobject(models.Model):  
	CustomerNumber = models.IntegerField()
	MerchantRequestID = models.CharField(max_length=50)   
	CheckoutRequestID = models.CharField(max_length=50)    
	ResponseCode = models.IntegerField()   
	ResponseDescription = models.CharField(max_length=50)    
	CustomerMessage = models.CharField(max_length=50) 
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
	   return self.CustomerNumber


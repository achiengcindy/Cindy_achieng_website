from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
	address =  models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)

	




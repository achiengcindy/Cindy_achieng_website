from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)


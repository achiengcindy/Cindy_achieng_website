from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# class CustomUser(AbstractUser):
# 	email = models.EmailField(unique=True)
# 	date_of_birth = models.DateField(blank=True, null=True)
# 	photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
# 	address =  models.CharField(max_length=250)
# 	postal_code = models.CharField(max_length=20)
# 	city = models.CharField(max_length=100, default='')
# 	Estate = models.CharField(max_length=100,default='')
# 	phone = models.CharField(max_length=20, default='')


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	birth_date = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)

	#shipping information
	physical_address =  models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	Estate = models.CharField(max_length=100)

	# contact info
	phone = models.CharField(max_length=20)


	
	def __str__(self):
		return 'Profile of user: {}'.format(self.user.username)

#create a user profile  when user is created
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)



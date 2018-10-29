from django.conf import settings
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# see https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username

class EmailAuthBackend:
	def authenticate(self, username=None, password=None):
		try:
			user = CustomUser.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except CustomUser.DoesNotExist:
			return None
	def get_user(self, user_id):
		try:
			return CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			return None

			
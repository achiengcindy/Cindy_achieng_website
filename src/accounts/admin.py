from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'photo', 'physical_address', 'phone', 'Estate' ]
admin.site.register(Profile, ProfileAdmin)





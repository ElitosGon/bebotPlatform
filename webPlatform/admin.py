from django.contrib import admin
from webPlatform import models

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']


admin.site.register(models.Profile, ProfileAdmin)
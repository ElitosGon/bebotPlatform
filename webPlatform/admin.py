from django.contrib import admin
from webPlatform import models

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class TypeTagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class TagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class ProviderAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class SourceAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	list_filter = ['created_at', 'updated_at']

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.TypeTag, TypeTagAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Project, ProjectAdmin)

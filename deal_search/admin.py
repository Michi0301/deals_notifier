from django.contrib import admin
from deal_search.models import Notification, Branch

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  pass

@admin.register(Branch)
class NotificationAdmin(admin.ModelAdmin):
  pass
from django.contrib import admin
from deal_search.models import SearchRequest

# Register your models here.
@admin.register(SearchRequest)
class SearchRequestAdmin(admin.ModelAdmin):
  pass


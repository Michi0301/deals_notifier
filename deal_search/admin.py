from django.contrib import admin
from deal_search.models import SearchRequest, Branch

# Register your models here.
@admin.register(SearchRequest)
class SearchRequestAdmin(admin.ModelAdmin):
  pass

@admin.register(Branch)
class SearchRequestAdmin(admin.ModelAdmin):
  pass
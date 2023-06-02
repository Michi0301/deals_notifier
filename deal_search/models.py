from django.db import models
from users.models import User

class SearchRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=10)
    product_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    search_type = models.CharField(max_length=10)

class Branch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=10)
    branch_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

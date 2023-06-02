from django.db import models
from users.models import User

class SearchRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    provider = models.CharField(max_length=10)
    product_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

class Branch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=10)
    branch_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

from django.db import models
from api.models import User

class Order(models.Model):
    product_name = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'order_model'
        db_table = 'order_table'
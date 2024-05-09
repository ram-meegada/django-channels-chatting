from django.db import models

# Create your models here.
class ReviewAndRatingsModel(models.Model):
    artist = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    
    def __str__(self):
        return f"{self.artist} - {self.client}"
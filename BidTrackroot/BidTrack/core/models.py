from django.db import models
from django.contrib.auth.models import User

class Bidet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=1000)
    handicap_friendly = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name
#This is the bidet model it tracks the data needed for our bidet databases    


class Review(models.Model):
    bidet = models.ForeignKey(Bidet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  #Limited to 5 nearest can make more
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review by {self.user.username} for {self.bidet.name}'
#This is the Review model, it tracks the data for the reviews found in the specific bidets pages    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    needs_handicap_access = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile of {self.user.username}'
#This is the userprofile model also helps with the handicap access tracking
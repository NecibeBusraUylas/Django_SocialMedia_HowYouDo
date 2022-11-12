from django.db import models
from django.contrib.auth import get_user_model
 
# to get to model of current user who is authenticated 
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE) # use user model as foreign key to get the information of current user
    id_user = models.IntegerField() # id of the user who has this profile (user models's id) 
    about = models.TextField(blank=True)
    profileImage = models.ImageField(upload_to='profile_images', default='default_profile_image.png')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def validate_egyptian_phone(value):
     
    if value and value.strip():   
         
        if len(value) != 11:
            raise ValidationError('Phone must be exactly 11 digits')
        
         
        if not value.isdigit():
            raise ValidationError('Phone must contain only Numbers')
        
         
        valid_starts = ['010', '011', '012', '015']
        if not any(value.startswith(start) for start in valid_starts):
            raise ValidationError('Phone must be Egyptian number')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.CharField(
        max_length=11, 
        blank=True, 
        null=True,
        validators=[validate_egyptian_phone]
    )
    
    def __str__(self):
        return f"{self.user.username} Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.CharField(max_length=500, blank=True)
    image_file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    target_amount = models.FloatField(default=0)
    current_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.title
    
    def get_youtube_id(self):
        if not self.video_url:
            return None
        
         
        regex = r'(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})'
        
        match = re.search(regex, self.video_url)
        if match:
            return match.group(1)
        return None

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Each user gets one profile
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Only resize if the image file exists
        if self.image and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.image.path)
            except Exception as e:
                # Log or print for debugging
                print(f"Image processing error: {e}")


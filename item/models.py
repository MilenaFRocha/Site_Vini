from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=225)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            target_width = 800
            target_height = 600

            width, height = img.size
            aspect_ratio = width / float(height)

            if aspect_ratio > target_width / float(target_height):
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                new_width = int(target_height * aspect_ratio)
                new_height = target_height

            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Crop the center of the image to the target size
            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2

            img = img.crop((left, top, right, bottom))

            img.save(self.image.path)

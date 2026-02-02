# from django.db import models


# # Create your models here.
# class Image(models.Model):
#     CATEGORIES = [("C", "Cat"), ("D", "Dog"), ("B", "Boy")]
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="apis/")
#     category = models.CharField(max_length=3, choices=CATEGORIES, default="C")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


from django.db import models


# Create your models here.
class Image(models.Model):
    CATEGORIES = [("C", "Cat"), ("D", "Dog"), ("B", "Boy"), ("G", "Girl")]

    name = models.CharField(max_length=100, blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="apis/", blank=True, null=True)
    category = models.CharField(max_length=3, choices=CATEGORIES, default="C")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or self.caption or "Image"

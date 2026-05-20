from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='products/')

    description = models.TextField()

    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        default='default.png'
    )

    full_name = models.CharField(
        max_length=200,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username
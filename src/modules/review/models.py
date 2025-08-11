from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from modules.hotel.models import Hotel, Room, Service
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# Прописати у сіреалайзері валідацію для перевірки чи hotel або room заповнений
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('10.0'))]
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uptated_at = models.DateTimeField(auto_now=True)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="hotel_reviews",
        null=True,
        blank=True
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="room_reviews",
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.comment[:50]
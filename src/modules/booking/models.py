import uuid

from django.db import models
from django.contrib.auth import get_user_model
from modules.hotel.models import Hotel, Room, Service

User = get_user_model()

# Create your models here.
class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_bookings")
    service = models.ManyToManyField(Service, related_name='service_booking')

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.email}"
    
class Payment(models.Model):
    class PaymentMethodChoice(models.TextChoices):
        CARD = 'Card'
        CASH = 'Cash'
    
    class StatusChoice(models.TextChoices):
        PAID = 'Paid'
        PENDING = 'Pending'
        FAILED = 'Failed'

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='booking_payment')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=5,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.CASH
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.id}" # type: ignore

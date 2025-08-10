from django.db import models
from django.core.validators import RegexValidator

# Create your models here. 
# 
# Додати необовязкові поля   
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Номер телефону має бути у форматі +380123456789 (від 10 до 15 цифр)"
            )
        ]
    )

    def __str__(self):
        return self.name

class RoomType(models.Model):
    class TypeChoice(models.TextChoices):
        STD = 'STD'
        SUPERIOR = 'Superior'
        DELUXE = 'Deluxe'
        JUNIOR_SUITE = 'Junior Suite'
        SUITE = 'Suite'
        FAMILY_ROOM = 'Family room'

    room_type = models.CharField(
        max_length=20,
        choices=TypeChoice.choices,
        default=TypeChoice.STD
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.room_type

class Room(models.Model):
    class StatusChoice(models.TextChoices):
        RESERVED = 'Reserved'
        VACANT = 'Vacant'
    
    name = models.CharField(max_length=100)
    room_number = models.PositiveIntegerField()
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoice.choices,
        default=StatusChoice.VACANT
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_rooms")
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='type_room_rooms')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
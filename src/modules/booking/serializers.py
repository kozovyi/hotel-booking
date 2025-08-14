from rest_framework import serializers

from modules.booking.models import Booking

class BookingSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Booking
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        extra_kwargs = {
            'user': {'read_only': True},
            'pk': {'read_only': True},
            
        }
        fields = ['pk', 'user','check_in','check_out','room','service']

class BookingSerializerСompactly(BookingSerializerBase):
    class Meta(BookingSerializerBase.Meta):
        fields = ['pk', 'user','check_in','check_out','room']
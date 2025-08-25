import logging
from datetime import timedelta

from rest_framework import serializers

from modules.booking.models import Booking
from modules.booking.services import BookingService

logger = logging.getLogger(__name__)


class BookingSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Booking
        extra_kwargs = {
            "user": {"read_only": True},
            "pk": {"read_only": True},
        }
        fields = ["pk", "user", "check_in", "check_out", "room", "service"]

    def validate(self, data):
        return BookingService.validate_date_range(self, data)


class BookingSerializerСompactly(BookingSerializerBase):
    room_name = serializers.CharField(source="room.name")

    class Meta(BookingSerializerBase.Meta):
        fields = ["pk", "user", "check_in", "check_out", "room_name"]


class BookingStatisticsSerializer(serializers.Serializer):
    bookings_number = serializers.IntegerField()
    total_amount_of_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_length_of_stay = serializers.DurationField()


class AvailableRoomSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    city = serializers.CharField(max_length=100)

    def validate(self, data):
        return BookingService.validate_date_range(self, data)

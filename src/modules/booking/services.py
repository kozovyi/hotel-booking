import logging
from datetime import datetime, date, timezone
from rest_framework.serializers import Serializer
from typing import Type

from modules.hotel.models import Room
from modules.booking.models import Booking
from modules.booking.exceprions import (
    InvalidCheckInDate,
    InvalidDataProvided,
    InvalidDateRange,
    RoomUnavailable,
)


logger = logging.getLogger(__name__)


class BookingService:

    @classmethod
    def is_room_available(cls, room_id: int, check_in: date, check_out: date) -> bool:
        return not Booking.objects.filter(
            room_id=room_id, check_in__lt=check_out, check_out__gt=check_in
        ).exists()

    @classmethod
    def validate_booking(
        cls, room_id: int, check_in: date, check_out: date, user
    ) -> None:
        if not cls.is_room_available(room_id, check_in, check_out):
            logger.warning(
                f"User {user} tried to book room {room_id}, but it's not available"
            )
            raise RoomUnavailable()

    @classmethod
    def validate_date_range(cls, instance, data):
        if data["check_in"] < datetime.now().date():
            logger.warning(
                f"User <{instance.context['request'].user}> tried invalid check-in date: <{data['check_in']}>"
            )
            raise InvalidCheckInDate()
        if data["check_in"] >= data["check_out"]:
            logger.warning(
                f"User <{instance.context['request'].user}> tried invalid date range: <{data['check_in']} - {data['check_out']}>"
            )
            raise InvalidDateRange()
        return data

    @classmethod
    def validate_by_serializer(
        cls, SerializerClass: Type[Serializer], context, data=None
    ):
        request = context.get("request")
        user = "anonymous" if not request.user else request.user
        data = (
            data
            if data is not None
            else getattr(request, "data", {}) if request else {}
        )
        
        serializer = SerializerClass(data=data, context=context)
        if serializer.is_valid():
            validated_data = serializer.validated_data
        else:
            logger.info(f"User: <{user}>  provided invalid data: <{serializer.errors}>")
            raise InvalidDataProvided(
                detail=f"User: <{user}>  provided invalid data: <{serializer.errors}>"
            )
        return validated_data

    @classmethod
    def get_available_rooms(cls, check_in: date, check_out: date, city: str):
        return Room.objects.filter(hotel__city__iexact=city).exclude(
            booking__check_in__lt=check_out, booking__check_out__gt=check_in
        )

import logging
from datetime import datetime, date

from modules.booking.models import Booking
from modules.booking.exceprions import InvalidDateRange, RoomUnavailable

logger = logging.getLogger(__name__)

class BookingService():

    @classmethod
    def is_room_available(cls, room_id: int, check_in: date, check_out: date) -> bool:
        return not Booking.objects.filter(
            room_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()
    
    @classmethod
    def validate_booking(cls, room_id: int, check_in: date, check_out: date, user) -> None:
        if check_in >= check_out:
            logger.warning(f"User {user} tried invalid date range: {check_in} - {check_out}")
            raise InvalidDateRange()
        if not cls.is_room_available(room_id, check_in, check_out):
            logger.warning(f"User {user} tried to book room {room_id}, but it's not available")
            raise RoomUnavailable()
        
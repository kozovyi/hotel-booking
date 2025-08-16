from rest_framework.exceptions import APIException
from rest_framework import status


class RoomUnavailable(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Room is not available for the selected dates."
    default_code = "room_unavailable"


class InvalidDateRange(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Check-in date must be before check-out date."
    default_code = "invalid_date_range"


class InvalidCheckInDate(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The check-in date cannot be past."
    default_code = "invalid_check_in_date"


class InvalidDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid data provided."
    default_code = "invalid_data"

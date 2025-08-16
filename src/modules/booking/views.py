import datetime
import logging

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, response

from modules.booking.models import Booking
from modules.booking.serializers import (
    AvailableRoomSerializer,
    BookingSerializerBase,
    BookingSerializerСompactly,
)
from modules.booking.permissions import IsAdminOrOwner, IsOwner
from modules.booking.services import BookingService
from modules.booking.exceprions import InvalidDateRange, RoomUnavailable

from modules.hotel.serializers import RoomSerializerBase


logger = logging.getLogger(__name__)


@extend_schema(tags=["Booking"])
class BookingViewSetAdmin(ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return BookingSerializerСompactly
        return BookingSerializerBase

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        room_id = serializer.validated_data.get("room").id
        check_in = serializer.validated_data.get("check_in")
        check_out = serializer.validated_data.get("check_out")
        user = self.request.user

        BookingService.validate_booking(room_id, check_in, check_out, user)
        serializer.save(user=user)
        logger.info(
            f"User: {user} booked room: {room_id} date({check_in} - {check_out})"
        )


@extend_schema_view(
    post=extend_schema(
        tags=["Booking-Rooms"],
        summary="Отримати доступні кімнати",
        description="Повертає список доступних кімнат за фільтрами",
        request=AvailableRoomSerializer,
        responses=RoomSerializerBase(many=True),
    ),
)
class AvailableRoomsView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request):
        validated_data = BookingService().validate_by_serializer(
            AvailableRoomSerializer, context={"request": request}
        )
        rooms = BookingService().get_available_rooms(validated_data.get("check_in"), validated_data.get("check_out"), validated_data.get("city"))  # type: ignore
        result_data = RoomSerializerBase(rooms, many=True).data
        return response.Response(data=result_data, status=status.HTTP_200_OK)

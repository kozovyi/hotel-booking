import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from modules.booking.models import Booking
from modules.booking.permissions import IsOwner
from modules.booking.serializers import (
    AvailableRoomSerializer,
    BookingSerializerBase,
    BookingSerializerСompactly,
    BookingStatisticsSerializer,
)
from modules.booking.services import BookingService
from modules.hotel.models import Room
from modules.hotel.serializers import RoomSerializerBase

logger = logging.getLogger(__name__)


@extend_schema(tags=["Booking"])
class BookingViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.action in ["list"]:
            return Booking.objects.select_related("room").all()
        return Booking.objects.select_related("room").prefetch_related("service").all()

    def get_serializer_class(self):
        if self.action in ["list"]:
            return BookingSerializerСompactly
        return BookingSerializerBase

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

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

    @extend_schema(
        summary="Analytics of user bookings", responses=BookingStatisticsSerializer
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def analytics(self, request):
        analytitcs = BookingService.get_user_analytics(request.user)
        validated = BookingService.validate_by_serializer(
            BookingStatisticsSerializer, context={}, data=analytitcs
        )
        return response.Response(data=validated, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=["Booking-Rooms"],
        summary="Отримати доступні кімнати",
        description="Повертає список доступних кімнат за фільтрами",
        request=AvailableRoomSerializer,
        responses=RoomSerializerBase(many=True),
        parameters=[
            OpenApiParameter(
                "search",
                str,
                OpenApiParameter.QUERY,
                description="Search by hotel name, room name or type",
            ),
            OpenApiParameter(
                "ordering",
                str,
                OpenApiParameter.QUERY,
                description="Order by price or capacity",
            ),
            OpenApiParameter(
                "",
                str,
                OpenApiParameter.QUERY,
                description="Order by price or capacity",
            ),
        ],
    ),
)
class AvailableRoomsView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]
    queryset = Room.objects.none()
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ["hotel__name", "name", "room_type__room_type"]
    filterset_fields = ["name", "hotel__name", "room_type__room_type"]
    ordering_fields = ["room_type__price", "room_type__capacity", "name"]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def post(self, request):
        validated_data = BookingService().validate_by_serializer(
            AvailableRoomSerializer, context={"request": request}
        )
        rooms = BookingService().get_available_rooms(
            validated_data.get("check_in"),  # type: ignore
            validated_data.get("check_out"),  # type: ignore
            validated_data.get("city"),  # type: ignore
        )
        rooms = self.filter_queryset(rooms)
        result_data = RoomSerializerBase(rooms, many=True).data
        return response.Response(data=result_data, status=status.HTTP_200_OK)

    # add pagination

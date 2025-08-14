from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
import logging

from modules.booking.models import Booking
from modules.booking.serializers import BookingSerializerBase, BookingSerializerСompactly
from modules.booking.permissions import IsAdminOrOwner, IsOwner
from modules.booking.services import BookingService
from modules.booking.exceprions import InvalidDateRange, RoomUnavailable


logger = logging.getLogger(__name__)

class BookingViewSetAdmin(ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return BookingSerializerСompactly
        return BookingSerializerBase
    

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
            
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        room_id=serializer.validated_data.get('room').id
        check_in=serializer.validated_data.get('check_in')
        check_out=serializer.validated_data.get('check_out')
        user = self.request.user

        BookingService.validate_booking(room_id, check_in, check_out, user)
        serializer.save(user=user)
        logger.info(f"User: {user} booked room: {room_id} date({check_in} - {check_out})")




        
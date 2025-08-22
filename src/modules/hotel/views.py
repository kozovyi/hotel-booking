from rest_framework import viewsets, status
from modules.hotel.models import Hotel, Room, RoomType, Service
from modules.booking.models import Booking
from modules.hotel.serializers import (
    HotelSerializer, RoomSerializer, 
    HotelListSerializer, ServiceSerializer, 
    RoomTypeSerializer, ValidateAvailableRoomsSerializer,
    AvailableRoomSerializer, ValidateRoomAvailabilitySerializer
)
from modules.review.serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from rest_framework.filters import SearchFilter, OrderingFilter

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]

    # текстовий пошук
    search_fields = ["name", "description", "address", "phone_number"]

    ordering_fields = ["name", "id", "address"]
    ordering = ["name"]   # дефолт

    def get_serializer_class(self):
        if self.action == 'list':
            return HotelListSerializer
        elif self.action in ['available_rooms']:
            return ValidateAvailableRoomsSerializer
        return HotelSerializer

    @action(detail=True, methods=['get'])
    def rooms(self, request, pk=None):
        """
        Отримати всі кімнати конкретного готелю
        """
        hotel = self.get_object()
        rooms = hotel.hotel_rooms.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Отримати всі відгуки конкретного готелю
        """
        hotel = self.get_object()
        reviews = hotel.hotel_reviews.all().select_related("user", "room")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def available_rooms(self, request, pk=None):
        """
        Отримати доступні кімнати готелю на конкретні дати
        """
        hotel = self.get_object()
        serializer = ValidateAvailableRoomsSerializer(data=request.data)
        
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']
            capacity = serializer.validated_data.get('capacity')
            room_type = serializer.validated_data.get('room_type')
            
            # Базова перевірка
            available_rooms = hotel.hotel_rooms.filter(status='Vacant')
            
            # Фільтрація за місткістю
            if capacity:
                available_rooms = available_rooms.filter(room_type__capacity__gte=capacity)
            
            # Фільтрація за типом кімнати
            if room_type:
                available_rooms = available_rooms.filter(room_type__room_type=room_type)
            
            # Виключаємо зайняті кімнати
            overlapping_bookings = Booking.objects.filter(
                room__hotel=hotel, 
                check_in__lt=check_out,
                check_out__gt=check_in
            ).values_list('room_id', flat=True)
            
            available_rooms = available_rooms.exclude(id__in=overlapping_bookings)
            
            room_serializer = AvailableRoomSerializer(available_rooms, many=True)
            
            return Response({
                'check_in': check_in,
                'check_out': check_out,
                'available_rooms': room_serializer.data,
                'total_count': available_rooms.count()
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = [
        "name", 
        "description",
        "hotel__name",
        "room_type__room_type",
    ]

    ordering_fields = [
        "room_number",
        "room_type__price",
        "room_type__capacity",
        "name",
        "hotel__name",
        "status",
        "id",
    ]
    ordering = ["room_type__room_type"]   # дефолт

    def get_serializer_class(self):
        if self.action == 'check_availability':
            return ValidateRoomAvailabilitySerializer
        return RoomSerializer

    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """
        Перевірити доступність конкретної кімнати на певні дати
        """
        room = self.get_object()
        serializer = ValidateRoomAvailabilitySerializer(data=request.data)
        
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']
            
            # Перевіряємо чи кімната доступна загалом
            if room.status != 'Vacant':
                return Response({
                    'available': False,
                    'reason': 'Кімната технічно недоступна'
                })
            
            # Перевіряємо чи немає бронювань
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exists()
            
            if overlapping_bookings:
                return Response({
                    'available': False,
                    'reason': 'Кімната заброньована на ці дати'
                })
            
            return Response({
                'available': True,
                'room': RoomSerializer(room).data,
                'check_in': check_in,
                'check_out': check_out
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class AvailableRoomsGlobalViewSet(viewsets.GenericViewSet):
    """
    Глобальний пошук доступних кімнат по всіх готелях
    """
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'rooms':
            return ValidateAvailableRoomsSerializer
        return RoomSerializer
    
    @action(detail=False, methods=['post'])
    def rooms(self, request):
        serializer = ValidateAvailableRoomsSerializer(data=request.data)
        
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']
            capacity = serializer.validated_data.get('capacity')
            room_type = serializer.validated_data.get('room_type')
            
            # Базова перевірка
            available_rooms = Room.objects.filter(status='Vacant')
            
            # Фільтрація за місткістю
            if capacity:
                available_rooms = available_rooms.filter(room_type__capacity__gte=capacity)
            
            # Фільтрація за типом
            if room_type:
                available_rooms = available_rooms.filter(room_type__room_type=room_type)
            
            # Виключаємо кімнати, які зайняті
            overlapping_bookings = Booking.objects.filter(
                Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
            ).values_list('room_id', flat=True)
            
            available_rooms = available_rooms.exclude(id__in=overlapping_bookings)
            
            # Групуємо результати по готелях
            hotels_with_rooms = {}
            for room in available_rooms:
                hotel_id = room.hotel.id
                if hotel_id not in hotels_with_rooms:
                    hotels_with_rooms[hotel_id] = {
                        'hotel': HotelListSerializer(room.hotel).data,
                        'rooms': []
                    }
                hotels_with_rooms[hotel_id]['rooms'].append(
                    AvailableRoomSerializer(room).data
                )
            
            return Response({
                'check_in': check_in,
                'check_out': check_out,
                'results': list(hotels_with_rooms.values()),
                'total_hotels': len(hotels_with_rooms),
                'total_rooms': available_rooms.count()
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import serializers
from modules.hotel.models import Hotel, Room, Service, RoomType
from datetime import datetime

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_number', 'description', 'status', 
                 'room_type', 'hotel']
        read_only_fields = ['id']

class HotelSerializer(serializers.ModelSerializer):
    hotel_rooms = RoomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'hotel_rooms']
        read_only_fields = ['id']


class HotelListSerializer(serializers.ModelSerializer):
    """Спрощений серіалізатор для списку готелів"""
    ready_rooms_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'ready_rooms_count']
        read_only_fields = ['id']
    
    def get_ready_rooms_count(self, obj):
        return obj.hotel_rooms.filter(status='Vacant').count()

class ValidateAvailableRoomsSerializer(serializers.Serializer):
    """Серіалізатор для пошуку доступних кімнат"""
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    capacity = serializers.IntegerField(required=False)
    room_type = serializers.ChoiceField(
        choices=RoomType.TypeChoice.choices, 
        required=False
    )
    
    def validate(self, attrs):
        self._validate_dates(attrs)
        return attrs

    def _validate_dates(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError("Дата виїзду повинна бути пізніше дати заїзду")
            if check_in < datetime.now().date():
                raise serializers.ValidationError("Дата заїзду не може бути в минулому")
    
class ValidateRoomAvailabilitySerializer(serializers.Serializer):
    """Для перевірки конкретної кімнати"""
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    # логіка повторюється
    def validate(self, attrs):
        ValidateAvailableRoomsSerializer()._validate_dates(attrs)
        return attrs

class AvailableRoomSerializer(serializers.ModelSerializer):
    """Серіалізатор для відображення доступних кімнат з інформацією про тип"""
    room_type = RoomTypeSerializer(read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_number', 'description', 
                 'room_type', 'hotel_name', 'hotel']
        read_only_fields = ['id']

class RoomSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Room
        extra_kwargs = {
            "pk": {"read_only": True},
        }
        fields = [
            "pk",
            "name",
            "room_number",
            "description",
            "status",
            "hotel",
            "room_type",
        ]
from rest_framework.serializers import ModelSerializer

from modules.hotel.models import Room


class RoomSerializerBase(ModelSerializer):
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

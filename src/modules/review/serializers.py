from rest_framework import serializers
from modules.review.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'rating',
            'comment',
            'created_at',
            'hotel',
            'room',
        )

        #Валідація принадлежності до готелю або номеру при створенні через API
        def validate(self, attrs):
            hotel = attrs.get('hotel')
            room = attrs.get('room')

            if not hotel and not room:
                raise serializers.ValidationError(
                    "Потрібно вказати або готель, або номер."
                )
            return attrs

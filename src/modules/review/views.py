from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from modules.review.models import Review
from modules.review.serializers import ReviewSerializer
from modules.hotel.models import Hotel, Room
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для роботи з відгуками.
    """
    queryset = Review.objects.all().select_related("hotel", "room", "user")
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]

    # пошук по тексту коментаря і юзернейму
    search_fields = ['comment', 'user__username']

    # сортування по рейтингу і даті створення
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']  # дефолт

    @action(detail=False, methods=['get'], url_path='by-hotel/(?P<hotel_id>[^/.]+)')
    def reviews_by_hotel(self, request, hotel_id=None):
        """
        Отримати всі відгуки для конкретного готелю
        """
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        reviews = hotel.hotel_reviews.all()
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-room/(?P<room_id>[^/.]+)')
    def reviews_by_room(self, request, room_id=None):
        """
        Отримати всі відгуки для конкретної кімнати
        """
        room = get_object_or_404(Room, pk=room_id)
        reviews = room.room_reviews.all()
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Отримати найновіші відгуки
        """
        reviews = Review.objects.order_by("-created_at")[:5]
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """
        Отримати відгуки з рейтингом
        """
        reviews = Review.objects.filter(rating__gte=8).order_by("-rating")
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

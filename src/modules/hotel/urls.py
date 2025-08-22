from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.hotel.views import HotelViewSet, RoomViewSet, RoomTypeViewSet, ServiceViewSet, AvailableRoomsGlobalViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'room-types', RoomTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'search', AvailableRoomsGlobalViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
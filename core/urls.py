from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('rsvps', RSVPViewSet, basename='rsvp')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]

from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer


# 1️ Event ViewSet
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'organizer__username']  # search by title, location, organizer
    ordering_fields = ['start_time', 'end_time', 'created_at']

    def perform_create(self, serializer):
        # Set the current user as the organizer when creating an event
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        # Show public events only unless user is organizer
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.filter(is_public=True) | Event.objects.filter(organizer=user)
        return Event.objects.filter(is_public=True)


# 2️ RSVP ViewSet
class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 3️ Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


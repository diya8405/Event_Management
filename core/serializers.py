# core/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Event, RSVP, Review


# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ------------------------
# UserProfile Serializer
# ------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'full_name', 'bio', 'location', 'profile_picture']


# ------------------------
# Event Serializer
# ------------------------
class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer',
            'location', 'start_time', 'end_time',
            'is_public', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        """Automatically set the logged-in user as the event organizer"""
        user = self.context['request'].user
        event = Event.objects.create(organizer=user, **validated_data)
        return event


# ------------------------
# RSVP Serializer
# ------------------------
class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        event = self.context['event']
        return RSVP.objects.create(user=user, event=event, **validated_data)


# ------------------------
# Review Serializer
# ------------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        event = self.context['event']
        return Review.objects.create(user=user, event=event, **validated_data)

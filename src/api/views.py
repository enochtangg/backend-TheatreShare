from django.shortcuts import render
from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import TheatreSerializer
from .models import Theatre

# Create your views here.


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""

    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(owner=self.request.user)  # Add owner=self.request.user


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)



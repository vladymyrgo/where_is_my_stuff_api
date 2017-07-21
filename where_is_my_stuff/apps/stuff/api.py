from rest_framework import generics

from stuff.serializers import StuffUpdateSerializer, StuffCreateSerializer
from stuff.models import Stuff


class StuffListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StuffCreateSerializer

    def get_queryset(self):
        if self.request.user.id:
            return Stuff.objects.filter(user=self.request.user)
        else:
            return Stuff.objects.none()


class StuffUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StuffUpdateSerializer

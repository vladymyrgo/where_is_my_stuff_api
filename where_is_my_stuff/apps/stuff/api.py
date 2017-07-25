from django.http import Http404
from rest_framework import generics

from stuff.serializers import StuffUpdateSerializer, StuffCreateSerializer
from stuff.models import Stuff


class StuffListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StuffCreateSerializer

    def get_queryset(self):
        return Stuff.objects.filter(user=self.request.user)


class StuffUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StuffUpdateSerializer


class StuffDestroyAPIView(generics.DestroyAPIView):

    def get_object(self):
        pk = self.kwargs.get('pk')
        stuff = Stuff.objects.filter(pk=pk, user=self.request.user).first()
        if stuff:
            return stuff
        else:
            raise Http404

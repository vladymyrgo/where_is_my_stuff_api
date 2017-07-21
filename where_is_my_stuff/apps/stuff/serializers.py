from rest_framework import serializers

from stuff.models import Stuff


class StuffUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stuff
        fields = ['title', 'photo', 'location']


class StuffCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stuff
        fields = ['id', 'title', 'photo', 'location']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        validated_data.update({'user': user})
        return super().create(validated_data)

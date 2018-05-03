from rest_framework import serializers
from .models import Theatre


class TheatreSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Theatre
        fields = ('id', 'name', 'owner', 'date_created', 'date_modified', 'youtube_url')
        read_only_fields = ('date_created', 'date_modified')

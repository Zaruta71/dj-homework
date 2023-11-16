from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from advertisements.models import *

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if Advertisement.objects.filter(creator_id=self.context['request'].user.id, status="OPEN").count() >= 10:
            if data.get("status") == "OPEN":
                raise serializers.ValidationError(detail=f"User open advertisements no more than 10", )
        return data


class AdvertisementGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class FavoritesSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['user', 'advertisement']

    def create(self, validated_data):
        if Favorites.objects.filter(
                Q(advertisement_id=self.data['advertisement']) &
                Q(user_id=self.data['user'])
        ).exists():
            raise serializers.ValidationError(
                {'status': "You have this favorite advertisement"}
            )
        return super().create(validated_data)


class FavoritesSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementGETSerializer()

    class Meta:
        model = Favorites
        fields = ['user', 'advertisement']

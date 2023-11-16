from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrAdminOrReadOnly
from advertisements.serializers import *


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", ]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdminOrReadOnly()]
        return []

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def set_favorite(self, request, *args, **kwargs):
        advertisement = get_object_or_404(self.queryset, **kwargs)
        favorite_object = {
            'user': request.user.id,
            'advertisement': advertisement.pk
        }
        if advertisement.creator_id != request.user.id and advertisement.status != 'DRAFT':
            serializer = FavoritesSetSerializer(data=favorite_object)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'favorite set'})
        elif advertisement.creator_id == request.user.id:
            return Response({'status': "It's your advertisement"})
        return Response({'status': "Access denied"})

    def get_queryset(self):
        queryset = Advertisement.objects.filter(
            Q(creator_id=self.request.user.id) | ~Q(status="DRAFT")
        )
        return queryset

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='favorites')
    def get_favorites(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Advertisement.objects.filter(
                ~Q(creator_id=request.user.id) &
                Q(favorites__user_id=request.user.id) &
                ~Q(status='DRAFT')
            ).select_related().all()
        )
        ids = [a.id for a in queryset]
        queryset = Favorites.objects.filter(advertisement__in=ids)
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data)

# class FavoritesViewSet(ModelViewSet):
#     queryset = Favorites.objects.all()
#     serializer_class = FavoritesSerializer
#     filter_backends = [DjangoFilterBackend, ]
#     filterset_fields = ['user']
#     permission_classes = [IsAuthenticated]
#
#     @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
#     def get_favorites(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(Favorites.objects.filter(
#             Q(user_id=request.user.id) |
#             ~Q(advertisement__creator=request.user.id) & ~Q(advertisement__status='DRAFT')
#         ))
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

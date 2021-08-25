from django_filters import rest_framework as filters

from rest_framework import viewsets, mixins, permissions
from .filters import OrderFilter
from .models import Order

from .serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
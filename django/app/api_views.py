from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from .models import Supermarket, Section, Employee, Product, Warehouse, Distributor, Client, Purchase, Order
from .serializers import (
    SupermarketSerializer, SectionSerializer, EmployeeSerializer,
    ProductSerializer, WarehouseSerializer, DistributorSerializer,
    ClientSerializer, PurchaseSerializer, OrderSerializer, MeSerializer,
)

def _is_ceo(user):
    return user.groups.filter(name='CEO').exists()

class SupermarketViewSet(viewsets.ModelViewSet):
    serializer_class = SupermarketSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Supermarket.objects.prefetch_related('sections').all()
        return Supermarket.objects.prefetch_related('sections').filter(id=self.request.user.supermarket_id)

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Section.objects.all()

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Employee.objects.select_related('supermarket', 'supervisor').all()
        return Employee.objects.select_related('supermarket', 'supervisor').filter(
            supermarket=self.request.user.supermarket
        )

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        if not _is_ceo(request.user) and target.groups.filter(name='CEO').exists():
            return Response({'detail': 'Permission denied.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        target = self.get_object()
        if not _is_ceo(request.user) and target.groups.filter(name='CEO').exists():
            return Response({'detail': 'Permission denied.'}, status=403)
        return super().destroy(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Product.objects.select_related('section_name').all()

class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Warehouse.objects.select_related('supermarket').prefetch_related('warehstock_set__product').all()
        return Warehouse.objects.select_related('supermarket').prefetch_related('warehstock_set__product').filter(
            supermarket=self.request.user.supermarket
        )

class DistributorViewSet(viewsets.ModelViewSet):
    serializer_class = DistributorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Distributor.objects.all()

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Client.objects.all()

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Purchase.objects.select_related('supermarket', 'client').all()
        return Purchase.objects.select_related('supermarket', 'client').filter(
            supermarket=self.request.user.supermarket
        )

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Order.objects.select_related('supermarket', 'distributor').all()
        return Order.objects.select_related('supermarket', 'distributor').filter(
            supermarket=self.request.user.supermarket
        )

class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
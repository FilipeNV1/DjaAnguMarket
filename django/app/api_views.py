from urllib.parse import unquote
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import DjangoModelPermissionsWithView as DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Supermarket, Section, Employee, Product, Warehouse, Distributor, Client, Purchase, Order
from .serializers import (
    SupermarketSerializer, SectionSerializer, EmployeeSerializer,
    ProductSerializer, WarehouseSerializer, DistributorSerializer,
    ClientSerializer, PurchaseSerializer, OrderSerializer, MeSerializer,
)

def _is_ceo(user):
    return user.groups.filter(name='CEO').exists()

class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'status': 'ok', 'service': 'DjanGoMarket API'})

class SupermarketViewSet(viewsets.ModelViewSet):
    serializer_class = SupermarketSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['location']
    ordering_fields = ['id', 'location']
    ordering = ['id']

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Supermarket.objects.prefetch_related('sections').all()
        return Supermarket.objects.prefetch_related('sections').filter(id=self.request.user.supermarket_id)

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Section.objects.all()
    lookup_field = 'sname'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sname', 'department']
    ordering_fields = ['sname', 'department']
    ordering = ['sname']

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'enumber'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'role', 'contact']
    ordering_fields = ['enumber', 'name', 'salary']
    ordering = ['enumber']

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
    lookup_field = 'prodid'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'section_name__sname']
    ordering_fields = ['prodid', 'name', 'price', 'brand']
    ordering = ['name']

class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'wnumber'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['area', 'supermarket__location']
    ordering_fields = ['wnumber', 'area']
    ordering = ['wnumber']

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
    lookup_field = 'email'
    lookup_value_regex = r'[^/]+'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'contact']
    ordering_fields = ['name', 'email']
    ordering = ['name']

    def get_object(self):
        self.kwargs['email'] = unquote(self.kwargs['email'])
        return super().get_object()

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Client.objects.all()
    lookup_field = 'nif'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'nif', 'contact', 'address']
    ordering_fields = ['nif', 'name', 'fidelity']
    ordering = ['name']

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'purchid'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['purchid', 'client__name', 'supermarket__location']
    ordering_fields = ['purchid', 'date']
    ordering = ['-date']

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Purchase.objects.select_related('supermarket', 'client').all()
        return Purchase.objects.select_related('supermarket', 'client').filter(
            supermarket=self.request.user.supermarket
        )

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'orderid'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['orderid', 'distributor__name', 'supermarket__location']
    ordering_fields = ['orderid', 'ord_date']
    ordering = ['-ord_date']

    def get_queryset(self):
        if _is_ceo(self.request.user):
            return Order.objects.select_related('supermarket', 'distributor').all()
        return Order.objects.select_related('supermarket', 'distributor').filter(
            supermarket=self.request.user.supermarket
        )

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    """Allow the logged-in user to change their own password."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {'detail': 'Both old_password and new_password are required.'}, status=400
            )
        if not user.check_password(old_password):
            return Response({'old_password': ['Current password is incorrect.']}, status=400)
        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            return Response({'new_password': list(e.messages)}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password updated successfully.'})
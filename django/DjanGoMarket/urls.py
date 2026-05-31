from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from app import api_views
from app.jwt_views import EmployeeTokenObtainPairView

router = DefaultRouter()
router.register(r'supermarkets', api_views.SupermarketViewSet, basename='api-supermarket')
router.register(r'sections', api_views.SectionViewSet, basename='api-section')
router.register(r'employees', api_views.EmployeeViewSet, basename='api-employee')
router.register(r'products', api_views.ProductViewSet, basename='api-product')
router.register(r'warehouses', api_views.WarehouseViewSet, basename='api-warehouse')
router.register(r'distributors', api_views.DistributorViewSet, basename='api-distributor')
router.register(r'clients', api_views.ClientViewSet, basename='api-client')
router.register(r'purchases', api_views.PurchaseViewSet, basename='api-purchase')
router.register(r'orders', api_views.OrderViewSet, basename='api-order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', api_views.HealthView.as_view(), name='api_health'),
    path('api/', include(router.urls)),
    path('api/token/', EmployeeTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', api_views.MeView.as_view(), name='api_me'),
    path('api/me/password/', api_views.ChangePasswordView.as_view(), name='api_change_password'),
]

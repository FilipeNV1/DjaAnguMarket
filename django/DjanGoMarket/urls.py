from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from app import views, api_views
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
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.home, name='home'),
    path('supermarkets/', views.supermarket_list, name='supermarket_list'),
    path('sections/', views.section_list, name='section_list'),
    path('employees/', views.employee_list, name='employee_list'),
    path('products/', views.product_list, name='product_list'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('distributors/', views.distributor_list, name='distributor_list'),
    path('clients/', views.client_list, name='client_list'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('orders/', views.order_list, name='order_list'),

    path('supermarkets/add/', views.supermarket_create, name='supermarket_create'),
    path('sections/add/', views.section_create, name='section_create'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('products/add/', views.product_create, name='product_create'),
    path('warehouses/add/', views.warehouse_create, name='warehouse_create'),
    path('distributors/add/', views.distributor_create, name='distributor_create'),
    path('clients/add/', views.client_create, name='client_create'),
    path('purchases/add/', views.purchase_create, name='purchase_create'),
    path('orders/add/', views.order_create, name='order_create'),

    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('sections/<str:pk>/', views.section_detail, name='section_detail'),
    path('supermarkets/<int:pk>/', views.supermarket_detail, name='supermarket_detail'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('distributors/<str:pk>/', views.distributor_detail, name='distributor_detail'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('purchases/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    path('supermarkets/<int:pk>/edit/', views.supermarket_edit, name='supermarket_edit'),
    path('sections/<str:pk>/edit/', views.section_edit, name='section_edit'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('warehouses/<int:pk>/edit/', views.warehouse_edit, name='warehouse_edit'),
    path('distributors/<str:pk>/edit/', views.distributor_edit, name='distributor_edit'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('purchases/<int:pk>/edit/', views.purchase_edit, name='purchase_edit'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),

    path('supermarkets/<int:pk>/delete/', views.supermarket_delete, name='supermarket_delete'),
    path('sections/<str:pk>/delete/', views.section_delete, name='section_delete'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('warehouses/<int:pk>/delete/', views.warehouse_delete, name='warehouse_delete'),
    path('distributors/<str:pk>/delete/', views.distributor_delete, name='distributor_delete'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('purchases/<int:pk>/delete/', views.purchase_delete, name='purchase_delete'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # REST API
    path('api/health/', api_views.HealthView.as_view(), name='api_health'),
    path('api/', include(router.urls)),
    path('api/token/', EmployeeTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', api_views.MeView.as_view(), name='api_me'),
    path('api/me/password/', api_views.ChangePasswordView.as_view(), name='api_change_password'),
]

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('prihod/', views.prihod, name='prihod'),
    path('rashod/', views.rashod, name='rashod'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', views.products_view, name='products'),
    path('products/search/', views.search_products, name='search_products'),
    path('get_products_by_operation/<int:operation_id>/', views.get_products_by_operation, name='get_products_by_operation'),
    path('add_product/', views.add_product, name='add_product'),
    path('generate_report/', views.report_form, name='generate_report_form'),
]

